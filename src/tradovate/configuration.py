from .client import TOClient


class Configuration(TOClient):

    def admin_alert_find(self, name: str) -> dict:
        """Retrieves an entity of AdminAlert type by its name."""
        return self._get(f"/adminAlert/find?name={name}")

    def admin_alert_item(self, id: int) -> dict:
        """Retrieves an entity of AdminAlert type by its id."""
        return self._get(f"/adminAlert/item?id={id}")

    def admin_alert_items(self, ids: []) -> dict:
        """Retrieves multiple entities of AdminAlert type by its ids."""
        return self._get(
            f"/adminAlert/items?ids={','.join([str(id) for id in ids])}",
        )

    def admin_alert_list(self) -> dict:
        """Retrieves all entities of AdminAlert type."""
        return self._get("/adminAlert/list")

    def admin_alert_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of AdminAlert type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/adminAlert/suggest?t={text}&l={n_entities}")

    def clearing_house_find(self, name: str) -> dict:
        """Retrieves an entity of ClearingHouse type by its name."""
        return self._get(f"/clearingHouse/find?name={name}")

    def clearing_house_item(self, id: int) -> dict:
        """Retrieves an entity of ClearingHouse type by its id."""
        return self._get(f"/clearingHouse/item?id={id}")

    def clearing_house_items(self, ids: []) -> dict:
        """Retrieves multiple entities of ClearingHouse type by its ids."""
        return self._get(
            f"/clearingHouse/items?ids={','.join([str(id) for id in ids])}",
        )

    def clearing_house_list(self) -> dict:
        """Retrieves all entities of ClearingHouse type."""
        return self._get("/clearingHouse/list")

    def clearing_house_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of ClearingHouse type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/clearingHouse/suggest?t={text}&l={n_entities}")

    def entitlement_item(self, id: int) -> dict:
        """Retrieves an entity of Entitlement type by its id."""
        return self._get(f"/entitlement/item?id={id}")

    def entitlement_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Entitlement type by its ids."""
        return self._get(f"/entitlement/items?ids={','.join([str(id) for id in ids])}")

    def entitlement_list(self) -> dict:
        """Retrieves all entities of Entitlement type."""
        return self._get("/entitlement/list")

    def order_strategy_type_find(self, name: str) -> dict:
        """Retrieves an entity of OrderStrategyType type by its name."""
        return self._get(f"/OrderStrategyType/find?name={name}")

    def order_strategy_type_item(self, id: int) -> dict:
        """Retrieves an entity of OrderStrategyType type by its id."""
        return self._get(f"/orderStrategyType/item?id={id}")

    def order_strategy_type_items(self, ids: []) -> dict:
        """Retrieves multiple entities of OrderStrategyType type by its ids."""
        return self._get(f"/orderStrategyType/items?ids={','.join([str(id) for id in ids])}")

    def order_strategy_type_list(self) -> dict:
        """Retrieves all entities of OrderStrategyType type."""
        return self._get("/orderStrategyType/list")

    def order_strategy_type_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of OrderStrategyType type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/orderStrategyType/suggest?t={text}&l={n_entities}")

    def property_find(self, name: str) -> dict:
        """Retrieves an entity of Property type by its name."""
        return self._get(f"/property/find?name={name}")

    def property_item(self, id: int) -> dict:
        """Retrieves an entity of Property type by its id."""
        return self._get(f"/property/item?id={id}")

    def property_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Property type by its ids."""
        return self._get(
            f"/property/items?ids={','.join([str(id) for id in ids])}",
        )

    def property_list(self) -> dict:
        """Retrieves all entities of Property type."""
        return self._get("/property/list")

    def property_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of Property type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/property/suggest?t={text}&l={n_entities}")
