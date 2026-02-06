"""
Tests for the delivery data audit report.

These tests validate that the written analysis in
`delivery_challenge/data/data_audit.md` captures the key discrepancies
and root causes described in the challenge brief.
"""

from pathlib import Path


AUDIT_PATH = (
    Path(__file__).resolve().parent.parent
    / "delivery_challenge"
    / "data"
    / "data_audit.md"
)


def _read_audit_text() -> str:
    """Read the full contents of the audit markdown file as text."""

    return AUDIT_PATH.read_text(encoding="utf-8")


def test_audit_mentions_orphaned_payments() -> None:
    """The audit should explicitly call out orphaned payments in Finance."""

    content = _read_audit_text()
    assert "Orphaned Payments" in content
    assert "O5008" in content


def test_audit_mentions_fulfillment_latency() -> None:
    """The audit should highlight the long fulfillment latency for specific orders."""

    content = _read_audit_text()
    assert "Fulfillment Latency" in content
    assert "27-day gap" in content or "27 day gap" in content


def test_audit_mentions_status_dissonance() -> None:
    """The audit should discuss status dissonance between Finance and Delivery systems."""

    content = _read_audit_text()
    assert "Status Dissonance" in content
    assert "O5003" in content
    assert "O5009" in content