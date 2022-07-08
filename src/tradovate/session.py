import requests,os,redis,time,datetime,json, pytz
from . import auth

redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            decode_responses=True)

class TOSession(requests.Session):
    def __init__(self, user_id=1):
        super().__init__()
        self._accessToken = {
            "token": "",
            "md_token": "",
            "expiration_time": None,
        }  # Set to -1 so that it gets refreshed immediately and its age tracked.
        self._user_id = user_id
        self._headers = {}

    def _set_header_auth(self):
        self._headers.update({"Authorization": "Bearer " + self._accessToken["token"]})

    def request(self, *args, **kwargs):
        self._token_if_invalid(self._user_id)
        return super().request(headers=self._headers, *args, **kwargs)

    def _token_if_invalid(self, user_id):
        # Expire the token one minute before its expiration time to be safe
        if self._is_token_invalid(user_id):
            token = auth.access_token()

            access_token = {
                "access_token": token['accessToken'],
                "md_access_token": token['mdAccessToken'],
                "expiration_time": token['expirationTime'],
            }
            redis_client.set('TO_TOKEN_'+str(user_id), json.dumps(access_token))

            self._set_access_token(access_token)

    def _is_token_invalid(self, user_id):
        self._get_access_token(user_id)

        if ( self._accessToken == None or
            not self._accessToken["token"]
            or self._access_token_expired()
        ):
            return True
        else:
            return False

    def _get_access_token(self, user_id):
        token = redis_client.get('TO_TOKEN_'+str(user_id))
        if token != None:
            self._set_access_token(json.loads(token))

    def _set_access_token(self, token):
        self._accessToken["token"] = token["access_token"]
        self._accessToken["md_token"] = token["md_access_token"]
        self._accessToken["expiration_time"] = token['expiration_time']
        self._set_header_auth()

    def _access_token_expired(self):
        expiration_time = self._accessToken["expiration_time"]
        dt = int(datetime.datetime.now(tz=pytz.UTC).strftime("%s"))
        dt2 = int(datetime.datetime.strptime(expiration_time, '%Y-%m-%dT%H:%M:%S.%f%z').strftime("%s"))
        age_secs = dt2 - dt
        print("******************************************************age_secs:", age_secs)
        return True if age_secs < 60 else False
