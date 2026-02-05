"""
Wallet management skill.

Implements the `WalletManager` contract defined in `specs/technical.md`.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List

from pydantic import BaseModel, Field, PositiveFloat, ValidationError, field_validator


class TransactionModel(BaseModel):
    """Pydantic model used to validate transaction inputs."""

    amount: PositiveFloat = Field(..., description="Amount to spend in USDC.")
    target: str = Field(..., description="Spending target identifier (e.g., API_CREDITS).")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the transaction was created.",
    )

    @field_validator("target")
    @classmethod
    def _validate_target(cls, value: str) -> str:
        """Ensure that target is a non-empty, stripped string."""

        stripped = value.strip()
        if not stripped:
            raise ValueError("target must be a non-empty string")
        return stripped


class WalletConfig(BaseModel):
    """Configuration for the wallet governor."""

    daily_limit: PositiveFloat = Field(
        ..., description="Maximum total spend permitted per 24h window, in USDC."
    )


class WalletManager:
    """
    Enforces a daily spend limit for AgentKit transactions.

    The actual signing / blockchain interaction is intentionally left as a stub
    to keep this component focused on governance logic.
    """

    def __init__(self, daily_limit: float) -> None:
        """
        Initialize a new `WalletManager`.

        Parameters
        ----------
        daily_limit:
            Maximum total spend allowed per 24h window, in USDC.
        """

        # Validate configuration via Pydantic
        self._config = WalletConfig(daily_limit=daily_limit)
        self._transactions: List[TransactionModel] = []

    @property
    def daily_limit(self) -> float:
        """Return the configured daily limit."""

        return float(self._config.daily_limit)

    def _spent_last_24h(self, now: datetime | None = None) -> float:
        """
        Compute the total amount spent in the last 24 hours.

        This method is primarily used to support future extensions where
        multiple transactions are executed over time.
        """

        if now is None:
            now = datetime.now(timezone.utc)
        window_start = now - timedelta(hours=24)
        return float(
            sum(t.amount for t in self._transactions if t.created_at >= window_start)
        )

    def execute_transaction(self, amount: float, target: str) -> None:
        """
        Validate and execute a governed transaction.

        Raises
        ------
        PermissionError
            If the requested `amount` exceeds the configured `daily_limit`.
        RuntimeError
            If a downstream AgentKit / signing failure occurs (stubbed).
        ValidationError
            If inputs fail Pydantic validation (e.g. non-positive amount).
        """

        # Validate inputs using Pydantic
        try:
            tx = TransactionModel(amount=amount, target=target)
        except ValidationError as exc:  # surface Pydantic errors directly
            raise exc

        # Enforce daily limit based on the spec: any single transaction
        # exceeding the limit must be blocked with PermissionError.
        if tx.amount > self._config.daily_limit:
            raise PermissionError("DAILY_LIMIT_EXCEEDED")

        # Record transaction locally; persistence / AgentKit integration is stubbed.
        self._transactions.append(tx)

        # Stubbed downstream call – in a real implementation this would
        # delegate to Coinbase AgentKit and wrap failures as RuntimeError.
        try:
            self._sign_and_broadcast(tx)
        except Exception as exc:  # pragma: no cover - placeholder for real integration
            raise RuntimeError("AGENTKIT_TRANSACTION_FAILED") from exc

    def _sign_and_broadcast(self, tx: TransactionModel) -> None:
        """
        Placeholder for integration with Coinbase AgentKit.

        This method intentionally performs no real network I/O to keep
        unit tests fast and deterministic.
        """

        # No-op stub: in production we would interface with AgentKit here.
        return None

