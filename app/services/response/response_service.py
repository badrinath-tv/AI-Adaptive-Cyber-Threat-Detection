from __future__ import annotations


class ResponseService:
    """
    Determines a safe, simulated response based
    on the calculated risk level.
    """

    POLICIES = {
        "LOW": [
            "LOG_EVENT",
        ],
        "MEDIUM": [
            "LOG_EVENT",
            "ALERT_ANALYST",
        ],
        "HIGH": [
            "LOG_EVENT",
            "CREATE_INCIDENT",
            "SIMULATE_CONTAINMENT",
        ],
    }

    def generate_response(
        self,
        risk_level: str,
    ) -> dict:
        """
        Generate response actions without executing
        real-world network containment.
        """

        risk_level = risk_level.upper()

        if risk_level not in self.POLICIES:
            raise ValueError(
                f"Unknown risk level: {risk_level}"
            )

        actions = self.POLICIES[risk_level]

        return {
            "risk_level": risk_level,
            "actions": actions,
            "executed": False,
            "simulation": True,
        }