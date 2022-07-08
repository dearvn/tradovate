from .client import TOClient


class Alerts(TOClient):

    def complete_alert_signal(self, admin_alert_signal_id: int) -> dict:
        """An "Incomplete" notification is one that has not yet been viewed by a user.
           Once a user has interacted with a notification it should be "completed"."""
        return self._post(
            url="/adminAlertSignal/completealertsignal",
            payload={"adminAlertSignalId": admin_alert_signal_id},
        )

    def admin_alert_signal_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of AdminAlertSignal type related to AdminAlert entity."""
        return self._get(f"/adminAlertSignal/deps?master_id={master_id}")

    def admin_alert_signal_item(self, id: int) -> dict:
        """Retrieves an entity of AdminAlertSignal type by its id."""
        return self._get(f"/adminAlertSignal/item?id={id}")

    def admin_alert_signal_items(self, ids: []) -> dict:
        """Retrieves multiple entities of AdminAlertSignal type by its ids."""
        return self._get(f"/adminAlertSignal/items?ids={','.join([str(id) for id in ids])}")

    def admin_alert_signal_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of AdminAlertSignal type related to multiple entities of AdminAlert type."""
        return self._get(f"/adminAlertSignal/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def admin_alert_signal_list(self) -> dict:
        """Retrieves all entities of AdminAlertSignal type."""
        return self._get("/adminAlertSignal/list")

    def take_alert_signal_ownership(self, admin_alert_signal_id: int) -> dict:
        """Internal. Can be used by B2B partners to mark an adminAlertSignal entity for further handling."""
        return self._post(
            url="/adminAlertSignal/takealertsignalownership",
            payload={"adminAlertSignalId": admin_alert_signal_id},
        )

    def create_alert(self,
                           expression: str,
                           valid_until: str,
                           trigger_limits: int,
                           message: str) -> dict:
        """Create an alert entity associated with the user."""
        return self._post(
            url="/alert/createalert",
            payload={
                "expression": expression,
                "validUntil": valid_until,
                "triggerLimits": trigger_limits,
                "message": message,
            },
        )

    def delete_alert(self, alert_id: int) -> dict:
        """Remove an alert entity associated with the user."""
        return self._post(
            url="/alert/deletealert",
            payload={"alertId": alert_id},
        )

    def alert_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of Alert type related to User entity."""
        return self._get(f"/alert/deps?master_id={master_id}")

    def dismiss_alert(self, alert_id: int) -> dict:
        """Dismiss an alert for a user."""
        return self._post(
            url="/alert/dismissalert",
            payload={"alertId": alert_id},
        )

    def alert_item(self, id: int) -> dict:
        """Retrieves an entity of Alert type by its id."""
        return self._get(f"/alert/item?id={id}")

    def alert_items(self, ids: []) -> dict:
        """Retrieves multiple entities of Alert type by its ids."""
        return self._get(f"/alert/items?ids={','.join([str(id) for id in ids])}")

    def alert_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of Alert type related to multiple entities of User type."""
        return self._get(f"/alert/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def alert_list(self) -> dict:
        """Retrieves all entities of Alert type."""
        return self._get("/alert/list")

    def mark_read_alert_signal(self, alert_id: int, alert_signal_id: int) -> dict:
        """Mark an alert entity as 'read' for a user."""
        return self._post(
            url="/alert/markreadalertsignal",
            payload={
                "alertId": alert_id,
                "alertSignalId": alert_signal_id,
            },
        )

    def modify_alert(self,
                           alert_id: int,
                           expression: str,
                           valid_until: str = None,
                           trigger_limits: int = None,
                           message: str = "") -> dict:
        """Change the parameters of an existing alert."""
        payload = {
            "alertId": alert_id,
            "expression": expression,
        }
        if valid_until is not None:
            payload["validUntil"] = valid_until
        if trigger_limits is not None:
            payload["triggerLimits"] = trigger_limits
        if message is not None:
            payload["message"] = message

        return self._post(
            url="/alert/modifyalert",
            payload=payload,
        )

    def reset_alert(self, alert_id: int) -> dict:
        """
            Resets an alert.
            You can use this method after an alert has been triggered
            to keep the alert and wait for the alert to be triggered again.
        """
        return self._post(
            url="/alert/resetalert",
            payload={"alertId": alert_id},
        )

    def alert_signal_dependents(self, master_id: int) -> dict:
        """Retrieves all entities of AlertSignal type related to Alert entity."""
        return self._get(f"/alertSignal/deps?masterid={master_id}")

    def alert_signal_item(self, id: int) -> dict:
        """Retrieves an entity of AlertSignal type by its id."""
        return self._get(f"/alertSignal/item?id={id}")

    def alert_signal_items(self, ids: []) -> dict:
        """Retrieves multiple entities of AlertSignal type by its ids."""
        return self._get(f"/alertSignal/items?ids={','.join([str(id) for id in ids])}")

    def alert_signal_L_dependents(self, master_ids: []) -> dict:
        """Retrieves all entities of AlertSignal type related to multiple entities of Alert type."""
        return self._get(f"/alertSignal/ldeps?masterids={','.join([str(id) for id in master_ids])}")

    def alert_signal_list(self) -> dict:
        """Retrieves all entities of AlertSignal type."""
        return self._get("/alertSignal/list")
