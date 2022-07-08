from .client import TOClient


class Risk(TOClient):

    def account_risk_status_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of AccountRiskStatus type related to Account entity."""
        return self._get(f"/accountRiskStatus/deps?masterid={master_id}")

    def account_risk_status_item(self, id: int) -> dict:
        """Retrieves an entity of AccountRiskStatus type by its id."""
        return self._get(f"/accountRiskStatus/id={id}")

    def account_risk_status_items(self, ids: []) -> dict:
        """Retrieves multiple entities of AccountRiskStatus type by its ids."""
        return self._get(f"/accountRiskStatus/items?ids={','.join([str(id) for id in ids])}")

    def account_risk_status_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of AccountRiskStatus type related to multiple entities of Account type."""
        return self._get(f"/accountRiskStatus/ldeps?masterids={''.join([str(id) for id in master_ids])}")

    def account_risk_status_list(self) -> dict:
        """Retrieves all entities of AccountRiskStatus type."""
        return self._get("/accountRiskStatus/list")

    def contract_margin_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of ContractMargin type related to Contract entity."""
        return self._get(f"/contractMargin/deps?masterid={master_id}")

    def contract_margin_item(self, id: int) -> dict:
        """Retrieves an entity of ContractMargin type by its id."""
        return self._get(f"/contractMargin/item?id={id}")

    def contract_margin_items(self, ids: []) -> dict:
        """Retrieves multiple entities of ContractMargin type by its ids."""
        return self._get(f"/contractMargin/items?ids={','.join([str(id) for id in ids])}")

    def contract_margin_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of ContractMargin type related to multiple entities of Contract type."""
        return self._get(f"/contractMargin/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def product_margin_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of ProductMargin type related to Product entity."""
        return self._get(f"/productMargin/deps?masterid={master_id}")

    def product_margin_item(self, id: int) -> dict:
        """Retrieves an entity of ProductMargin type by its id."""
        return self._get(f"/productMargin/item?id={id}")

    def product_margin_items(self, ids: []) -> dict:
        """Retrieves multiple entities of ProductMargin type by its ids."""
        return self._get(f"/productMargin/items?ids={','.join([str(id) for id in ids])}")

    def product_margin_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of ProductMargin type related to multiple entities of Product type."""
        return self._get(f"/productMargin/ldeps?masterids={master_ids}")

    def product_margin_list(self) -> dict:
        """Retrieves all entities of ProductMargin type."""
        return self._get("/productMargin/list")

    def user_account_auto_liq_create(self,
                                           id: int,
                                           changes_locked: bool,
                                           margin_percent_alert: int,
                                           daily_loss_percent_alert: int,
                                           daily_loss_alert: int,
                                           margin_percent_liq_only: int,
                                           daily_loss_percent_liq_only: int,
                                           daily_loss_liq_only: int,
                                           margin_percent_auto_liq: int,
                                           daily_loss_percent_auto_liq: int,
                                           daily_loss_auto_liq: int,
                                           weekly_loss_auto_liq: int,
                                           flatten_timestamp: str,
                                           trailing_max_drawdown: int,
                                           trailing_max_drawdown_limit: int,
                                           daily_profit_auto_liq: int,
                                           weekly_profit_auto_liq: int) -> dict:
        """Creates a new entity of UserAccountAutoLiq."""
        return self._post(
            url="/userAccountAutoLiq/create",
            payload={
                "id": id,
                "changesLocked": changes_locked,
                "marginPercentageAlert": margin_percent_alert,
                "dailyLossPercentageAlert": daily_loss_percent_alert,
                "dailyLossAlert": daily_loss_alert,
                "marginPercentageLiqOnly": margin_percent_liq_only,
                "dailyLossPercentageLiqOnly": daily_loss_percent_liq_only,
                "dailyLossLiqOnly": daily_loss_liq_only,
                "marginPercentageAutoLiq": margin_percent_auto_liq,
                "dailyLossPercentageAutoLiq": daily_loss_percent_auto_liq,
                "dailyLossAutoLiq": daily_loss_auto_liq,
                "weeklyLossAutoLiq": weekly_loss_auto_liq,
                "flattenTimestamp": flatten_timestamp,
                "trailingMaxDrawdown": trailing_max_drawdown,
                "trailingMaxDrawdownLimit": trailing_max_drawdown_limit,
                "dailyProfitAutoLiq": daily_profit_auto_liq,
                "weeklyProfitAutoLiq": weekly_profit_auto_liq,
            },
        )

    def user_account_auto_liq_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of UserAccountAutoLiq type related to Account entity."""
        return self._get(f"/userAccountAutoLiq/deps?masterid={master_id}")

    def user_account_auto_liq_item(self, id: int) -> dict:
        """Retrieves an entity of UserAccountAutoLiq type by its id."""
        return self._get(f"/userAccountAutoLiq/item?id={id}")

    def user_account_auto_liq_items(self, ids: []) -> dict:
        """Retrieves multiple entities of UserAccountAutoLiq type by its ids."""
        return self._get(f"/userAccountAutoLiq/item?ids={','.join([str(id) for id in ids])}")

    def user_account_auto_liq_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of UserAccountAutoLiq type related to multiple entities of Account type."""
        return self._get(f"/userAccountAutoLiq/deps?masterid={','.join([str(id) for id in master_ids])}")

    def user_account_auto_liq_list(self) -> dict:
        """Retrieves all entities of UserAccountAutoLiq type."""
        return self._get("/userAccountAutoLiq/list")

    def user_account_auto_liq_update(self,
                                           id: int,
                                           changes_locked: bool,
                                           margin_percent_alert: int,
                                           daily_loss_percent_alert: int,
                                           daily_loss_alert: int,
                                           margin_percent_liq_only: int,
                                           daily_loss_percent_liq_only: int,
                                           daily_loss_liq_only: int,
                                           margin_percent_auto_liq: int,
                                           daily_loss_percent_auto_liq: int,
                                           daily_loss_auto_liq: int,
                                           weekly_loss_auto_liq: int,
                                           flatten_timestamp: str,
                                           trailing_max_drawdown: int,
                                           trailing_max_drawdown_limit: int,
                                           daily_profit_auto_liq: int,
                                           weekly_profit_auto_liq: int) -> dict:
        """Updates an existing entity of UserAccountAutoLiq."""
        return self._post(
            url="/userAccountAutoLiq/update",
            payload={
                "id": id,
                "changesLocked": changes_locked,
                "marginPercentageAlert": margin_percent_alert,
                "dailyLossPercentageAlert": daily_loss_percent_alert,
                "dailyLossAlert": daily_loss_alert,
                "marginPercentageLiqOnly": margin_percent_liq_only,
                "dailyLossPercentageLiqOnly": daily_loss_percent_liq_only,
                "dailyLossLiqOnly": daily_loss_liq_only,
                "marginPercentageAutoLiq": margin_percent_auto_liq,
                "dailyLossPercentageAutoLiq": daily_loss_percent_auto_liq,
                "dailyLossAutoLiq": daily_loss_auto_liq,
                "weeklyLossAutoLiq": weekly_loss_auto_liq,
                "flattenTimestamp": flatten_timestamp,
                "trailingMaxDrawdown": trailing_max_drawdown,
                "trailingMaxDrawdownLimit": trailing_max_drawdown_limit,
                "dailyProfitAutoLiq": daily_profit_auto_liq,
                "weeklyProfitAutoLiq": weekly_profit_auto_liq,
            },
        )

    def user_account_positions_limit(self,
                                           account_id: int,
                                           active: bool,
                                           total_by: str,
                                           id: int = None,
                                           contract_id: int = None,
                                           product_id: int = None,
                                           exchange_id: int = None,
                                           product_type: str = None,
                                           risk_discount_contract_group_id: int = None,
                                           product_verification_status: str = None,
                                           contract_group_id: int = None,
                                           risk_time_period_id: int = None,
                                           short_limit: int = None,
                                           long_limit: int = None,
                                           exposed_limit: int = None,
                                           description: str = None) -> dict:
        """Creates a new entity of UserAccountPositionLimit."""
        return self._post(
            url="/userAccountPositionLimit/create",
            payload={
                "id": id,
                "contractId": contract_id,
                "productId": product_id,
                "exchangeId": exchange_id,
                "productType": product_type,
                "riskDiscountContractGroupId": risk_discount_contract_group_id,
                "productVerificationStatus": product_verification_status,
                "contractGroupId": contract_group_id,
                "active": active,
                "riskTimePeriodId": risk_time_period_id,
                "totalBy": total_by,
                "shortLimit": short_limit,
                "longLimit": long_limit,
                "exposedLimit": exposed_limit,
                "description": description,
                "accountId": account_id,
            },
        )

    def delete_user_account_position_limit(self, user_position_limit_id: int) -> dict:
        """Remove an account position limit for a user."""
        return self._post(
            url="/userAccountPositionLimit/deleteuseraccountpositionlimit",
            payload={"userAccountPositionLimitId": user_position_limit_id},
        )

    def delete_user_account_risk_parameter(self, user_account_risk_parameter_id: int) -> dict:
        """Remove a Risk Setting parameter."""
        return self._post(
            url="/userAccountPositionLimit/deleteuseraccountriskparameter",
            payload={"userAccountRiskParameterId": user_account_risk_parameter_id},
        )

    def user_account_position_limit_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of UserAccountPositionLimit type related to Account entity."""
        return self._get(f"/userAccountPositionLimit/deps?masterid={master_id}")

    def user_account_position_limit_item(self, id: int) -> dict:
        """Retrieves an entity of UserAccountPositionLimit type by its id."""
        return self._get(f"/userAccountPositionLimit/item?id={id}")

    def user_account_position_limit_items(self, ids: []) -> dict:
        """Retrieves multiple entities of UserAccountPositionLimit type by its ids."""
        return self._get(f"/userAccountPositionLimit/item?id={','.join([str(id) for id in ids])}")

    def user_account_position_limit_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of UserAccountPositionLimit type related to multiple entities of Account type."""
        return self._get(f"/userAccountPositionLimit/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def user_account_position_limit_update(self,
                                                 account_id: int,
                                                 active: bool,
                                                 total_by: str,
                                                 id: int = None,
                                                 contract_id: int = None,
                                                 product_id: int = None,
                                                 exchange_id: int = None,
                                                 product_type: str = None,
                                                 risk_discount_contract_group_id: int = None,
                                                 product_verification_status: str = None,
                                                 contract_group_id: int = None,
                                                 risk_time_period_id: int = None,
                                                 short_limit: int = None,
                                                 long_limit: int = None,
                                                 exposed_limit: int = None,
                                                 description: str = None) -> dict:
        """Updates an existing entity of UserAccountPositionLimit."""
        return self._post(
            url="/userAccountPositionLimit/update",
            payload={
                "id": id,
                "contractId": contract_id,
                "productId": product_id,
                "exchangeId": exchange_id,
                "productType": product_type,
                "riskDiscountContractGroupId": risk_discount_contract_group_id,
                "productVerificationStatus": product_verification_status,
                "contractGroupId": contract_group_id,
                "active": active,
                "riskTimePeriodId": risk_time_period_id,
                "totalBy": total_by,
                "shortLimit": short_limit,
                "longLimit": long_limit,
                "exposedLimit": exposed_limit,
                "description": description,
                "accountId": account_id,
            },
        )

    def user_account_risk_parameter_create(self,
                                                 user_account_position_limit_id: int,
                                                 id: int = None,
                                                 contract_id: int = None,
                                                 product_id: int = None,
                                                 exchange_id: int = None,
                                                 product_type: str = None,
                                                 risk_discount_contract_group_id: int = None,
                                                 product_verification_status: str = None,
                                                 contract_group_id: int = None,
                                                 max_opening_order_qty: int = None,
                                                 max_closing_order_qty: int = None,
                                                 max_back_month: int = None,
                                                 pre_expiration_days: int = None,
                                                 margin_percentage: int = None,
                                                 margin_dollar_value: int = None,
                                                 hard_limit: bool = None) -> dict:
        """Creates a new entity of UserAccountRiskParameter."""
        return self._post(
            url="/userAccountRiskParameter/create",
            payload={
                "id": id,
                "contractId": contract_id,
                "productId": product_id,
                "exchangeId": exchange_id,
                "productType": product_type,
                "riskDiscountContractGroupId": risk_discount_contract_group_id,
                "productVerificationStatus": product_verification_status,
                "contractGroupId": contract_group_id,
                "maxOpeningOrderQty": max_opening_order_qty,
                "maxClosingOrderQty": max_closing_order_qty,
                "maxBackMonth": max_back_month,
                "preExpirationDays": pre_expiration_days,
                "marginPercentage": margin_percentage,
                "marginDollarValue": margin_dollar_value,
                "hardLimit": hard_limit,
                "userAccountPositionLimitId": user_account_position_limit_id,
            },
        )

    def user_account_risk_parameter_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of UserAccountRiskParameter type related to UserAccountPositionLimit entity."""
        return self._get(f"/userAccountRiskParameter/deps?masterid={master_id}")

    def user_account_risk_parameter_item(self, id: int) -> dict:
        """Retrieves an entity of UserAccountRiskParameter type by its id."""
        return self._get(f"/userAccountRiskParameter/item?id={id}")

    def user_account_risk_parameter_items(self, ids: []) -> dict:
        """Retrieves multiple entities of UserAccountRiskParameter type by its ids."""
        return self._get(
            f"/userAccountRiskParameter/item?id={','.join([str(id) for id in ids])}",
        )

    def user_account_risk_parameter_L_dependents(self, master_ids: []) -> dict:
        """
        Retrieves all entities of UserAccountRiskParameter type related to multiple entities of
        UserAccountPositionLimit type.
        """
        return self._get(
            f"/userAccountRiskParameter/ldeps?masterids={','.join([str(id) for id in master_ids])}",
        )

    def user_account_risk_parameter_update(self,
                                                 user_account_position_limit_id: int,
                                                 id: int = None,
                                                 contract_id: int = None,
                                                 product_id: int = None,
                                                 exchange_id: int = None,
                                                 product_type: str = None,
                                                 risk_discount_contract_group_id: int = None,
                                                 product_verification_status: str = None,
                                                 contract_group_id: int = None,
                                                 max_opening_order_qty: int = None,
                                                 max_closing_order_qty: int = None,
                                                 max_back_month: int = None,
                                                 pre_expiration_days: int = None,
                                                 margin_percentage: int = None,
                                                 margin_dollar_value: int = None,
                                                 hard_limit: bool = None) -> dict:
        """Updates an existing entity of UserAccountRiskParameter."""
        return self._post(
            url="/userAccountRiskParameter/update",
            payload={
                "id": id,
                "contractId": contract_id,
                "productId": product_id,
                "exchangeId": exchange_id,
                "productType": product_type,
                "riskDiscountContractGroupId": risk_discount_contract_group_id,
                "productVerificationStatus": product_verification_status,
                "contractGroupId": contract_group_id,
                "maxOpeningOrderQty": max_opening_order_qty,
                "maxClosingOrderQty": max_closing_order_qty,
                "maxBackMonth": max_back_month,
                "preExpirationDays": pre_expiration_days,
                "marginPercentage": margin_percentage,
                "marginDollarValue": margin_dollar_value,
                "hardLimit": hard_limit,
                "userAccountPositionLimitId": user_account_position_limit_id,
            },
        )
