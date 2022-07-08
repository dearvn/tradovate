from .client import TOClient


class Contract_Library(TOClient):

    def conteract_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of Contract type related to ContractMaturity entity."""
        return self._get(f"/contract/deps?masterid={master_id}")

    def conteract_find(self, name: str) -> dict:
        """Retrieves an entity of Contract type by its name."""
        return self._get(f"/contract/find?name={name}")

    def contract_item(self, id: int) -> dict:
        """Retrieves an entity of Contract type by its id."""
        return self._get(f"/contract/item?id={id}")

    def contract_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Contract type by its ids."""
        return self._get(f"/contract/items?ids={','.join([str(id) for id in ids])}")

    def product_fee_params(self, product_ids: []) -> dict:
        """Query the a product's fee parameters."""
        return self._post(
            url="/contract/getproductfeeparams",
            payload={"productIds": [id for id in product_ids]},
        )

    def contract_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of Contract type related to multiple entities of ContractMaturity type."""
        return self._get(f"/contract/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def roll_contract(self, name: str, forward: bool, ifExpired: bool) -> dict:
        """Request the best upcoming maturity date for a given contract."""
        return self._post(
            url="/contract/rollcontract",
            payload={
                "name": name,
                "forward": forward,
                "ifExpired": ifExpired,
            },
        )

    def contract_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of Contract type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/contract/suggest?t={text}&l={n_entities}")

    def contract_group_find(self, name: str) -> dict:
        """Retrieves an entity of ContractGroup type by its name."""
        return self._get(f"/contractGroup/find?name={name}")

    def contract_group_item(self, id: int) -> dict:
        """Retrieves an entity of ContractGroup type by its id."""
        return self._get(f"/contractGroup/item?id={id}")

    def contract_group_items(self, ids: []) -> dict:
        """Retrieves multiple entities of ContractGroup type by its ids."""
        return self._get(f"/contractGroup/items?ids={','.join([str(id) for id in ids])}")

    def contract_group_list(self) -> dict:
        """Retrieves all entities of ContractGroup type."""
        return self._get("/contractGroup/list")

    def contract_group_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of ContractGroup type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/contractGroup/suggest?t={text}&l={n_entities}")

    def contract_maturity_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of ContractMaturity type related to Product entity."""
        return self._get(f"/ContractMaturity/deps?master_id={master_id}")

    def contract_maturity_item(self, id: int) -> dict:
        """Retrieves an entity of ContractMaturity type by its id."""
        return self._get(f"/ContractMaturity/item?id={id}")

    def contract_maturity_items(self, ids: []) -> dict:
        """Retrieves multiple entities of ContractMaturity type by its ids."""
        return self._get(f"/ContractMaturity/items?ids={','.join([str(id) for id in ids])}")

    def contract_maturity_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of ContractMaturity type related to multiple entities of Product type."""
        return self._get(f"/contractMaturity/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def currency_find(self, name: str) -> dict:
        """Retrieves an entity of Currency type by its name."""
        return self._get(f"/currency/find?name={name}")

    def currency_item(self, id: int) -> dict:
        """Retrieves an entity of Currency type by its id."""
        return self._get(f"/currency/item?id={id}")

    def currency_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Currency type by its ids."""
        return self._get(f"/currency/items?ids={','.join([str(id) for id in ids])}")

    def currency_list(self) -> dict:
        """Retrieves all entities of Currency type."""
        return self._get("/currency/list")

    def currency_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of Currency type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/currency/suggest?t={text}&l={n_entities}")

    def currency_rate_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of CurrencyRate type related to Currency entity."""
        return self._get(f"/currencyRate/deps?masterid={master_id}")

    def currency_rate_item(self, id: int) -> dict:
        """Retrieves an entity of CurrencyRate type by its id."""
        return self._get(f"/currencyRate/item?id={id}")

    def currency_rate_items(self, ids: []) -> dict:
        """Retrieves multiple entities of CurrencyRate type by its ids."""
        return self._get(f"/currencyRate/items?ids={','.join([str(id) for id in ids])}")

    def currency_rate_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of CurrencyRate type related to multiple entities of Currency type."""
        return self._get(f"/currencyRate/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def currency_rate_list(self) -> dict:
        """Retrieves all entities of CurrencyRate type."""
        return self._get("/currencyRate/list")

    def exchange_find(self, name: str) -> dict:
        """Retrieves an entity of Exchange type by its name."""
        return self._get(f"/exchange/find?name={name}")

    def exchange_item(self, id: int) -> dict:
        """Retrieves an entity of Exchange type by its id."""
        return self._get(f"/exchange/item?id={id}")

    def exchange_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Exchange type by its ids."""
        return self._get(f"/exchange/items?ids={','.join([str(id) for id in ids])}")

    def exchange_list(self) -> dict:
        """Retrieves all entities of Exchange type."""
        return self._get("/exchange/list")

    def exchange_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of Exchange type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/exchange/suggest?t={text}&l={n_entities}")

    def product_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of Product type related to Exchange entity."""
        return self._get(f"/product/deps?masterid={master_id}")

    def product_find(self, name: str) -> dict:
        """Retrieves an entity of Product type by its name."""
        return self._get(f"/product/find?name={name}")

    def product_item(self, id: int) -> dict:
        """Retrieves an entity of Product type by its id."""
        return self._get(f"/product/id={id}")

    def product_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Product type by its ids."""
        return self._get(f"/product/items?ids={','.join(str(id) for id in ids)}")

    def product_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of Product type related to multiple entities of Exchange type."""
        return self._get(f"/product/ldeps?masterid={','.join([str(id) for id in master_ids])}")

    def product_list(self) -> dict:
        """Retrieves all entities of Product type."""
        return self._get("/product/list")

    def product_suggest(self, text: str, n_entities: int) -> dict:
        """Retrieves entities of Product type filtered by an occurrence of a text in one of its fields."""
        return self._get(f"/product/suggest?t={text}&l={n_entities}")

    def product_sess_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of ProductSession type related to Product entity."""
        return self._get(f"/productSession/deps?masterid={master_id}")

    def product_sess_item(self, id: int) -> dict:
        """Retrieves an entity of ProductSession type by its id."""
        return self._get(f"/productSession/item?id={id}")

    def product_session_items(self, ids: []) -> dict:
        """Retrieves multiple entities of ProductSession type by its ids."""
        return self._get(f"/productSession/items?ids={','.join([str(id) for id in ids])}")

    def product_session_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of ProductSession type related to multiple entities of Product type."""
        return self._get(f"/productSession/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def spread_definition_item(self, id: int) -> dict:
        """Retrieves an entity of SpreadDefinition type by its id."""
        return self._get(f"/SpreadDefinition/item?id={id}")

    def spread_definition_items(self, ids: []) -> dict:
        """Retrieves multiple entities of SpreadDefinition type by its ids."""
        return self._get(f"/SpreadDefinition/items?ids={','.join([str(id) for id in ids])}")
