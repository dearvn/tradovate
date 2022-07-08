from .client import TOClient


class Positions(TOClient):

    def fill_pair_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of FillPair type related to Position entity."""
        return self._get(f"fillPair/deps?id={master_id}")

    def fill_pair_item(self, id: int) -> dict:
        """Retrieves an entity of FillPair type by its id."""
        return self._get(f"/fillPair/item?id={id}")

    def fill_pair_items(self, ids: []) -> dict:
        """Retrieves multiple entities of FillPair type by its ids."""
        return self._get(f"/fillPair/items?ids{','.join([str(id) for id in ids])}")

    def fill_pair_l_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of FillPair type related to multiple entities of Position type."""
        return self._get(f"/fillPair/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def fill_pair_list(self) -> dict:
        """Retrieves all entities of FillPair type."""
        return self._get("/fillPair/list")

    def position_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of Position type related to Account entity."""
        return self._get(f"/postion/deps?masterid={master_id}")

    def position_find(self, name: str) -> dict:
        """Retrieves an entity of Position type by its name."""
        return self._get(f"/position/find?name={name}")

    def position_item(self, id: int) -> dict:
        """Retrieves an entity of Position type by its id."""
        return self._get(f"/position/item?id={id}")

    def position_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Position type by its ids."""
        return self._get(f"/position/items?ids={','.join([str(id) for id in ids])}")

    def position_l_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of Position type related to multiple entities of Account type."""
        return self._get(f"/postion/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def position_list(self) -> dict:
        """Retrieves all entities of Position type."""
        return self._get("/position/list")
