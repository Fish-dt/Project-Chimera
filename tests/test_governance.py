import pathlib
import sys

import pytest


# Ensure the project root (which contains the `skills` package) is on sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from skills.wallet import WalletManager

def test_spending_limit_enforcement():
    """
    GOAL: Verify that the Governor blocks any transaction exceeding the daily limit.
    EXPECTED: This test will fail (ImportError) until the Wallet Skill is implemented.
    """
    governor = WalletManager(daily_limit=5.0)
    # Attempt to spend 10 USDC
    with pytest.raises(PermissionError):
        governor.execute_transaction(amount=10.0, target="API_CREDITS")