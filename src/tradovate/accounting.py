from .client import TOClient


class Accounting(TOClient):

    def account_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of Account type related to User entity."""
        return self._get(f"/account/deps?masterid={master_id}")

    def account_find(self, name: str) -> dict:
        """Retrieves an entity of Account type by its name."""
        return self._get(f"/account/find?name={name}")

    def account_item(self, id: int) -> dict:
        """Retrieves an entity of Account type by its id."""
        return self._get(f"/account/item?id={id}")

    def account_items(self, ids: []) -> dict:
        """Retrieves an entity of Account type by its ids."""
        return self._get(f"/account/items?ids={','.join([str(id) for id in ids])}")

    def account_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of Account type related to multiple entities of User type"""
        return self._get(f"/account/deps?masterid={','.join([str(id) for id in master_ids])}")

    def account_list(self) -> dict:
        """Retrieves all entities of Account type."""
        return self._get("/account/list")


    def account_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of Account type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/account/suggest?t={text}&l={n_entities}")

    def cash_balance_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of CashBalance type related to Account entity."""
        return self._get(f"/cashBalance/deps?masterid={master_id}")

    def cash_balance_snapshot(self, account_id: int) -> dict:
        """Get a snapshot of an account's current cash balance."""
        return self._post(
            url="/cashBalance/getcashbalancesnapshot",
            payload={"accountId": account_id},
        )

    def cash_balance_item(self, id: int) -> dict:
        """Retrieves an entity of CashBalance type by its id."""
        return self._get(f"/cashBalance/item?id={id}")

    def cash_balance_items(self, ids: []) -> dict:
        """Retrieves multiple entities of CashBalance type by its ids."""
        return self._get(f"/cashBalance/items?ids={','.join([str(id) for id in ids])}")

    def cash_balance_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of CashBalance type related to multiple entities of Account type."""
        return self._get(f"/cashBalance/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def cash_balance_list(self) -> dict:
        """Retrieves all entities of CashBalance type."""
        return self._get("/cashBalance/list")

    def cash_balance_log_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of CashBalanceLog type related to Account entity."""
        return self._get(f"/cashBalanceLog/deps?masterid={master_id}")

    def cash_balance_log_item(self, id: int) -> dict:
        """Retrieves an entity of CashBalanceLog type by its id."""
        return self._get(f"/cashBalanceLog/item?id={id}")

    def cash_balance_log_items(self, ids: []) -> dict:
        """Retrieves an entity of CashBalanceLog type by its id."""
        return self._get(f"/cashBalanceLog/item?ids={','.join(str(id) for id in ids)}")

    def cash_balance_log_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of CashBalanceLog type related to multiple entities of Account type."""
        return self._get(f"/cashBalanceLog/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def margin_snapshot_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of MarginSnapshot type related to Account entity."""
        return self._get(f"/marginSnapshot/deps?masterid={master_id}")

    def margin_snapshot_item(self, id: int) -> dict:
        """Retrieves an entity of MarginSnapshot type by its id."""
        return self._get(f"/marginSnapshot/item?id={id}")

    def margin_snapshot_items(self, ids: []) -> dict:
        """Retrieves multiple entities of MarginSnapshot type by its ids."""
        return self._get(f"/marginSnapshot/items?ids={','.join(str(id) for id in ids)}")

    def margin_snapshot_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of MarginSnapshot type related to multiple entities of Account type."""
        return self._get(f"/marginSnapshot/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def margin_snapshot_list(self) -> dict:
        """Retrieves all entities of MarginSnapshot type."""
        return self._get("/marginSnapshot/list")

    def permission_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of TradingPermission type related to User entity."""
        return self._get(f"/tradingPermission/deps?masterid={master_id}")

    def permission_item(self, id: int) -> dict:
        """Retrieves an entity of TradingPermission type by its id."""
        return self._get(f"/tradingPermission/item?id={id}")

    def permission_items(self, ids: []) -> dict:
        """Retrieves multiple entities of TradingPermission type by its ids."""
        return self._get(f"/tradingPermission/items?ids={','.join([str(id) for id in ids])}")

    def permission_L_Dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of TradingPermission type related to multiple entities of User type."""
        return self._get(f"/tradingPermission/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def permission_list(self) -> dict:
        """Retrieves all entities of TradingPermission type."""
        return self._get("/tradingPermission/list")
