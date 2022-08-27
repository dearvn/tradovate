## Imports
from __future__ import annotations
import asyncio,redis,logging,json,os,requests,pytz,time

from datetime import datetime,timedelta
import numpy as np

from .profile import Profile
from .profile.session import Session, WebSocket
from .utils import urls
from .utils.typing import CredentialAuthDict
from typing import Sequence
from numbers import Number

import pandas_ta as pd

## Constants
log = logging.getLogger(__name__)
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            decode_responses=True)


## Classes
class Client(Profile):
    """Tradovate Client"""

    # -Constructor
    def __init__(self) -> Client:
        self.id: int = 0
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._session: Session = Session(loop=self._loop)
        self._handle_auto_renewal: asyncio.TimerHandle | None = None
        self._live: WebSocket | None = None
        self._demo: WebSocket | None = None
        self._mdlive: WebSocket | None = None
        self._mddemo: WebSocket | None = None
        self._mdreplay: WebSocket | None = None
        self._support: float | None = None
        self._datas: dict | None = None
        self._chart_id: int | None = None
        self._order: dict | None = None
        self._trend: int | None = None
        self._bigdrop = 0
        self._bottomsupport = 0
        self._order: dict | None = None
        self._time_order: int | None = None
        # can change this setting from redis or config
        self._start_times = "1:00".split(":")
        self._end_times = "23:30".split(":")
        self._exit_times = "23:00".split(":")
        self._point_in = 3
        self._point_out = 5
        self._stoploss_point = 7
        self._gain_point = 5
        self._time_candle: int | None = None

    # -Instance Methods: Private
    def _dispatch(self, event: str, *args, **kwargs) -> None:
        '''Dispatch task for event name'''
        log.debug(f"Client event '{event}'")

        method = "on_" + event
        try:
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            self._loop.create_task(coro(*args, **kwargs))

    async def _renewal(self) -> None:
        '''Task for Session authorization renewal loop'''
        while self._session.authenticated.is_set():
            time = self._session.token_duration - timedelta(minutes=10)
            await asyncio.sleep(time.total_seconds())
            await self._session.renew_access_token()

    async def _subcribe(
        self, auth: CredentialAuthDict, auto_renew: bool,
        ticker, interval,
        live: bool, demo: bool, mdlive: bool
    ) -> None:
        '''Private client loop run method'''
        await self.create_websockets(live, demo, mdlive)
        await self.authorize(auth, auto_renew)
        await self.authorizion_hold()
        await self.sync_websockets()
        for websocket in self._websockets:
            self._loop.create_task(self.process_subcribe(websocket, ticker=ticker, interval=interval))

        self._dispatch('subcribe', ticker=ticker, interval=interval)

    async def _unsubcribe(
        self, auth: CredentialAuthDict, auto_renew: bool,
        ticker,
        live: bool, demo: bool, mdlive: bool
    ) -> None:
        '''Private client loop run method'''
        await self.create_websockets(live, demo, mdlive)
        await self.authorize(auth, auto_renew)
        await self.authorizion_hold()
        await self.sync_websockets()
        for websocket in self._websockets:
            self._loop.create_task(self.process_message(websocket))

        self._dispatch('unsubcribe', ticker=ticker)

    # -Instance Methods: Public
    async def authorize(
        self, auth: CredentialAuthDict, auto_renew: bool = True
    ) -> None:
        '''Initialize Client authorization and auto-renewal'''
        self.id = await self._session.request_access_token(
            auth, account_websockets=self._websockets_account,
            market_websockets=self._websockets_market
        )
        if auto_renew:
            self._loop.create_task(self._renewal(), name="client-renewal")

    async def authorizion_hold(self) -> None:
        '''Wait for all authentication setup to be finished'''
        await self._session.authenticated.wait()
        for websocket in self._websockets:
            await websocket.authenticated.wait()

    async def close(self) -> None:
        for websocket in self._websockets:
            await websocket.close()
        await self._session.close()

    async def create_websockets(self, live: bool, demo: bool, mdlive: bool) -> None:
        '''Initialize Client WebSockets'''
        self._live = (
            await WebSocket.from_session(urls.wss_base_live, self._session)
            if live else None
        )
        self._demo = (
            await WebSocket.from_session(urls.wss_base_demo, self._session)
            if demo else None
        )
        self._mdlive = (
            await WebSocket.from_session(urls.wss_base_market, self._session)
            if mdlive else None
        )

    async def process_message(self, websocket: WebSocket, interval) -> None:
        '''Task for WebSocket loop'''
        while websocket.connected.is_set():
            msgs = (await websocket.poll_message())
            if not msgs:
                continue

    async def process_subcribe(self, websocket: WebSocket, ticker, interval) -> None:
        '''Task for WebSocket loop'''
        while websocket.connected.is_set():
            msgs = (await websocket.poll_message(ticker, interval))

            now = datetime.now(pytz.timezone("America/Los_Angeles"))
            d = now.day
            h = now.hour
            m = now.minute
            if h == 23 and m == 59:
                if self._datas and len(self._datas) > 240:
                    self._datas = self._datas[-240:]

            if not msgs:
                continue
            msg = msgs[0]

            if not msg:
                continue

            if not msg or not msg.get('e') or msg.get('e') != 'chart' or not msg.get('d'):
                continue

            d = msg.get('d')

            if not d.get('charts'):
                continue

            charts = d.get('charts')

            for chart in charts:
                bars = chart.get('bars')
                self._chart_id = chart.get('id')
                if not bars:
                    continue

                self._datas = self._save_data_redis(id, self._datas, bars, ticker, interval)

                # I use this logic to test trading demo on Tradovate
                if len(self._datas) >= 240:
                    print(">>>>>Last data", self._datas[len(self._datas)-1])
                    self.logic_call_put(self._datas, self._support, ticker=ticker, interval=interval)

    def _save_data_redis(self, id, datas, bars, ticker, interval):
        if datas:
            items = datas

            l = len(items)

            if (len(bars) == 240 - l):
                datas = bars + items
                if (len(datas) == 240):
                    self._support = self.f_calcFractalDownZone(datas[-1]['low'], datas, 0, 12)
            else:
                dt = int(datetime.strptime(items[l - 1]['timestamp'], '%Y-%m-%dT%H:%M%z').strftime("%s"))
                for bar in bars:
                    dt2 = int(datetime.strptime(bar['timestamp'], '%Y-%m-%dT%H:%M%z').strftime("%s"))

                    if dt == dt2:
                        items[l-1] = bar
                    elif dt < dt2:
                        items.append(bar)

                datas = items
        else:
            datas = bars

        return datas

    def run_subcribe(
        self, auth: CredentialAuthDict, *, auto_renew: bool = True,
        ticker, interval,
        live_websocket: bool = True, demo_websocket: bool = False,
        mdlive_websocket: bool = True
    ) -> None:
        '''Public client loop run method'''
        self._loop.run_until_complete(self._subcribe(
            auth, auto_renew, ticker, interval, live_websocket,
            demo_websocket, mdlive_websocket
        ))
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            for task in asyncio.all_tasks(loop=self._loop):
                task.cancel()
            self._loop.run_until_complete(self.close())
            self._loop.close()

    def run_unsubcribe(
        self, auth: CredentialAuthDict, *, auto_renew: bool = True,
        ticker,
        live_websocket: bool = True, demo_websocket: bool = False,
        mdlive_websocket: bool = True
    ) -> None:
        '''Public client loop run method'''
        self._loop.run_until_complete(self._unsubcribe(
            auth, auto_renew, ticker, live_websocket,
            demo_websocket, mdlive_websocket
        ))
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            for task in asyncio.all_tasks(loop=self._loop):
                task.cancel()
            self._loop.run_until_complete(self.close())
            self._loop.close()

    async def subscribe_symbol(
        self, id_: int | str, *, interval: int, total: int
    ) -> None:
        '''Add symbol to market subscription'''
        if self._mdlive:
            # -Market
            await self._mdlive.request(urls.wss_market_sub, body={"symbol": id_})

        # -Chart
        await self._mdlive.request(urls.wss_market_chart_sub,
           body={"symbol": id_,
                "chartDescription": {
                    "underlyingType": 'MinuteBar',
                    "elementSize": interval,
                    "elementSizeUnit": 'UnderlyingUnits',
                    "withHistogram": False,
                },
                "timeRange": {
                    "asMuchAsElements": total
                }
        })

    async def sync_websockets(self) -> None:
        for websocket in self._websockets_account:
            await websocket.request(urls.wss_user_sync, body={'users': [self.id]})

    async def unsubscribe_symbol(self, id_: int | str) -> None:
        '''Remove symbol from market subscription'''
        await self._mdlive.request(urls.wss_market_usub, body={"symbol": id_})
        await self._mdlive.request(urls.wss_market_dom_usub, body={"symbol": id_})
        await self._mdlive.request(urls.wss_market_histogram_usub, body={"symbol": id_})
        await self._mdlive.request(urls.wss_market_chart_usub, body={"symbol": id_})

    # -Properties: Private
    @property
    def _websockets(self) -> tuple[WebSocket]:
        websockets = []
        if self._live:
            websockets.append(self._live)
        if self._demo:
            websockets.append(self._demo)
        if self._mdlive:
            websockets.append(self._mdlive)
        if self._mddemo:
            websockets.append(self._mddemo)
        if self._mdreplay:
            websockets.append(self._mdreplay)
        if websockets:
            return tuple(websockets)
        return None

    @property
    def _websockets_account(self) -> tuple[WebSocket]:
        websockets = []
        if self._live:
            websockets.append(self._live)
        if self._demo:
            websockets.append(self._demo)
        if websockets:
            return tuple(websockets)
        return None

    @property
    def _websockets_market(self) -> tuple[WebSocket]:
        websockets = []
        if self._mdlive:
            websockets.append(self._mdlive)
        if self._mddemo:
            websockets.append(self._mddemo)
        if self._mdreplay:
            websockets.append(self._mdreplay)
        if websockets:
            return tuple(websockets)
        return None

    # -Properties: Authenticated
    @property
    def authenticated(self) -> bool:
        if not self._session.authenticated.is_set():
            return False
        for websocket in self._websockets:
            if not websocket.authenticated.is_set():
                return False
        return True

    '''
    This is example logic to trading on tradovate
    '''
    def logic_call_put(self, datas, support, ticker, interval):
        l_datas = len(datas)
        if l_datas < 200:
            return

        now = datetime.now(pytz.timezone("America/Los_Angeles"))
        h = now.hour
        m = now.minute
        s = now.second

        is_last_time = m % interval == 0 and s < 30
        is_last_second = m % interval == 4 and s > 55

        start_times = self._start_times
        end_times = self._end_times
        exit_times = self._exit_times

        point_in = self._point_in
        point_out = self._point_out
        stoploss_point = self._stoploss_point
        gain_point = self._gain_point

        is_exit_all = False
        is_order = False
        if int(exit_times[0]) == h and int(exit_times[1]) > m:
            is_exit_all = True
        if (int(start_times[0]) < h or int(start_times[0]) == h and int(start_times[1]) < m) and (
                int(end_times[0]) > h or int(end_times[0]) == h and int(end_times[1]) > m):
            is_order = True

        last11 = datas[l_datas - 12]
        last5 = datas[l_datas - 6]
        last4 = datas[l_datas - 5]
        last3 = datas[l_datas - 4]
        last2 = datas[l_datas - 3]
        last1 = datas[l_datas - 2]
        last = datas[l_datas - 1]
        close1 = last1['close']
        close = last['close']
        low = last['low']
        high = last['high']
        hl = (high + low) / 2
        low1 = last1['low']
        high1 = last1['high']
        hl1 = (low1 + high1) / 2
        low2 = last2['low']
        high2 = last2['high']
        hl2 = (low2 + high2) / 2
        is_increase = hl > hl1 or hl > hl2
        is_decrease = hl < hl1 or hl < hl2
        is_strong_market = close >= last11['close']
        is_weak_market = close < last11['close']

        df = pd.DataFrame.from_records(datas, index=['timestamp'])
        wma200 = df.ta.wma(length=200)
        wma48 = df.ta.wma(length=48)
        wma13 = df.ta.wma(length=13)

        crossUpWMA13_48 = crossover(wma13, wma48)
        crossDownWMA13_48 = crossunder(wma13, wma48)
        crossUpWMA48_200 = crossover(wma48, wma200)
        crossDownWMA48_200 = crossunder(wma48, wma200)
        if crossUpWMA13_48:
            self._trend = 1
        elif crossUpWMA48_200:
            self._trend = 2
        elif crossDownWMA13_48:
            self._trend = -1
        elif crossDownWMA48_200:
            self._trend = -2

        trend = self._trend
        if trend:
            trend = int(trend)
        else:
            trend = 0

        rsi = df.ta.rsi(length=9)
        l_200 = wma200.size
        l_48 = wma48.size
        l_rsi = rsi.size

        point5 = last5['close'] - wma200.iloc[l_200 - 6]
        point2 = last2['close'] - wma200.iloc[l_200 - 3]
        point1 = last1['close'] - wma200.iloc[l_200 - 2]
        point = last['close'] - wma200.iloc[l_200 - 1]

        is_sideway = False
        if -5 <= point2 and 5 >= point2 and -5 <= point1 and 5 >= point1 and -5 <= point and 5 >= point:
            is_sideway = True

        support_zone = self.f_calcFractalDownZone(support, datas, 0, 0)
        if not support_zone:
            support_zone = low

        AWAY_EMA200 = point
        EMA_CHANGE_CALL = point - point1 >= point_in
        EMA_CHANGE_PUT = point - point1 <= -1 * point_in
        BIGDROP = rsi.iloc[l_rsi - 1] + 8 < rsi.iloc[l_rsi - 2] and close > wma48.iloc[l_48 - 1]
        if BIGDROP:
            self._bigdrop = 1
            self._bottomsupport = 0

        BOTTOMSUPPORT = close > support_zone and close > close1 and rsi.iloc[l_rsi - 1] > rsi.iloc[l_rsi - 2] + 10
        if BOTTOMSUPPORT:
            self._bigdrop = 0
            self._bottomsupport = 1

        # CALL:
        if not self._order:
            es_order = redis_client.get("es_order_" + ticker + "_" + str(interval))
            if es_order:
                self._order = json.loads(es_order)
                self._time_candle = now.hour*60 + (now.minute - now.minute%interval)

        enter_order = self._order

        print(">>>>Order", enter_order)

        entry_in = point - point1 >= point_in or point - point2 >= point_in
        entry_out = point1 - point >= point_out or point2 - point >= point_out
        if not is_sideway and not enter_order and not BIGDROP and is_order:
            call_order = {'ticker': ticker, 'interval': interval, 'type': 'Buy Long',
                          'stop_loss': close - stoploss_point,
                          'close': close, 'number_share': 1, 'signal': 'TO', 'source': 'TradOvate', 'time': time.time()}

            if entry_in:
                call_order['logic'] = 'CALL'
                call_order['number_share'] = 1
                call_order['pre_order'] = True
                self._order = call_order

        if self._order and 'pre_order' in self._order and self._order['type'] == 'Buy Long' and self._order['pre_order'] and is_last_second and close > self._order['close']:
            self._time_order = time.time()
            self._order['stop_loss'] = close - stoploss_point
            self._order['close'] = close
            self._time_candle = now.hour*60 + (now.minute - now.minute%interval)

            del self._order['pre_order']

            redis_client.set("es_order_" + ticker + "_" + str(interval), json.dumps(self._order))
            redis_client.set("time_order_" + ticker + "_" + str(interval), self._time_order)

            # CALL Order
            print(">>>> CALL ORDER")

        # PUT
        if not is_sideway and not enter_order and not BOTTOMSUPPORT and is_order:
            put_order = {'ticker': ticker, 'interval': interval, 'type': 'Sell Short',
                         'stop_loss': close + stoploss_point,
                         'close': close, 'number_share': 1, 'signal': 'TO', 'source': 'TradOvate', 'time': time.time()}

            if entry_out:
                put_order['logic'] = 'PUT Logic'
                put_order['number_share'] = 1
                put_order['pre_order'] = True
                self._order = put_order

        if self._order and 'pre_order' in self._order and self._order['type'] == 'Sell Short' and self._order['pre_order'] and is_last_second and close < self._order['close']:
            self._time_order = time.time()
            del self._order['pre_order']
            self._order['stop_loss'] = close + stoploss_point
            self._order['close'] = close

            self._time_candle = now.hour*60 + (now.minute - now.minute%interval)

            redis_client.set("order_" + ticker + "_" + str(interval), json.dumps(self._order))
            redis_client.set("time_order_" + ticker + "_" + str(interval), self._time_order)

            # PUT ORDER
            print(">>>> PUT ORDER")

        if enter_order and 'pre_order' not in self._order:
            order = self._order

            pre_candle = self._time_candle
            cur_candle = now.hour*60 + (now.minute - now.minute%interval)

            if order['type'] == 'Buy Long' and not entry_in and round(point) < round(point1):

                keep = False
                if cur_candle > pre_candle:
                    if entry_in or close > order['close']and cur_candle == pre_candle + 5 or cur_candle > pre_candle + 5 and close > close1:
                        keep = True

                if is_exit_all or close <= order['stop_loss'] or entry_out and is_last_second or round(point) <= round(point5):
                    # Stoploss
                    gain = close - order['close']
                    order['close'] = close
                    order['type'] = 'Exit Buy Long'
                    order['gain'] = gain

                    self._order = None
                    self._time_order = time.time()

                    redis_client.delete("order_" + ticker + "_" + str(interval))
                    redis_client.set("time_order_" + ticker + "_" + str(interval), self._time_order)

                    # PUT ORDER
                    print(">>>>> PUT ORDER")

                if (keep and close - order['close'] >= 2) or (close - order['close'] >= 5.5 and is_increase):
                    # EXIT When OUT Logic
                    gain = close - order['close']
                    order['close'] = close
                    order['type'] = 'Exit Buy Long'
                    order['gain'] = gain

                    self._order = None
                    self._time_order = time.time()

                    redis_client.delete("order_" + ticker + "_" + str(interval))
                    redis_client.set("time_order_" + ticker + "_" + str(interval), self._time_order)

                    # PUT ORDER
                    print(">>>>> PUT ORDER")


            elif order['type'] == 'Sell Short' and not entry_out and round(point) > round(point1):
                keep = False
                if cur_candle > pre_candle:
                    if entry_out or close < order['close'] and cur_candle == pre_candle + 5 or cur_candle > pre_candle + 5 and close < close1:
                        keep = True
                if is_exit_all or trend > 0 or close >= order['stop_loss'] or entry_in and is_last_second or round(point) >= round(point5):
                    # STOPLOSS
                    gain = order['close'] - close
                    order['close'] = close
                    order['type'] = 'Exit Sell Short'
                    order['gain'] = gain

                    self._order = None
                    self._time_order = time.time()
                    redis_client.delete("order_" + ticker + "_" + str(interval))
                    redis_client.set("time_order_" + ticker + "_" + str(interval), self._time_order)

                    # CALL ORDER
                    print(">>>> CALL ORDER")

                if (keep and order['close'] - close >= 1.5) or (order['close'] - close >= 4.5 and is_decrease):
                    # EXIT When IN Logic
                    gain = order['close'] - close
                    order['close'] = close
                    order['type'] = 'Exit Sell Short'
                    order['gain'] = gain

                    self._order = None
                    self._time_order = time.time()
                    redis_client.delete("order_" + ticker + "_" + str(interval))
                    redis_client.set("time_order_" + ticker + "_" + str(interval), self._time_order)

                    # CALL Order
                    print(">>>>CALL ORDER")


    def f_calcFractalDownZone(self, support, datas, cnt = 0, max_count = 12):
        df = pd.DataFrame.from_records(datas, index=['timestamp'])
        wmaVol = df.ta.wma(length=6, close="offerVolume")

        l_datas = len(datas)
        down = datas[l_datas - 4]['low'] < datas[l_datas - 5]['low'] and datas[l_datas - 5]['low'] < datas[l_datas - 6]['low'] and datas[l_datas - 3]['low'] > datas[l_datas - 4]['low'] and datas[l_datas - 2]['low'] > datas[l_datas - 3]['low'] and datas[l_datas - 4]['offerVolume'] > wmaVol[wmaVol.size - 4]

        if down and datas[l_datas - 4]['close'] >= datas[l_datas - 4]['open']:
            return datas[l_datas - 4]['open']
        else:
            if down and datas[l_datas - 4]['close'] < datas[l_datas - 4]['open']:
                return datas[l_datas - 4]['close']
            else:
                cnt = cnt + 1
                if cnt < max_count:
                    return self.f_calcFractalDownZone(support, datas[:-1], cnt, max_count)
                else:
                    return support

def crossover(series1: Sequence, series2: Sequence) -> bool:
    series1 = (
        series1.values if isinstance(series1, pd.Series) else
        (series1, series1) if isinstance(series1, Number) else
        series1)
    series2 = (
        series2.values if isinstance(series2, pd.Series) else
        (series2, series2) if isinstance(series2, Number) else
        series2)
    try:
        return series1[-2] < series2[-2] and series1[-1] > series2[-1]
    except IndexError:
        return False

def crossunder(series1: Sequence, series2: Sequence) -> bool:
    series1 = (
        series1.values if isinstance(series1, pd.Series) else
        (series1, series1) if isinstance(series1, Number) else
        series1)
    series2 = (
        series2.values if isinstance(series2, pd.Series) else
        (series2, series2) if isinstance(series2, Number) else
        series2)
    try:
        return series1[-2] > series2[-2] and series1[-1] < series2[-1]
    except IndexError:
        return False

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_)):
            return int(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)