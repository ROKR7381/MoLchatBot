# tests/test_container.py
"""
Tests for the container utility functions.
"""
import pytest

from utils.container import (
    extract_container_number,
    extract_po_number,
    extract_ocean_bl_number,
)


class TestExtractContainerNumber:
    """Test cases for extract_container_number function."""

    def test_extracts_standard_container_number(self):
        """Test extraction of standard container number format."""
        result = extract_container_number("container ABCD1234567")
        assert result == "ABCD1234567"

    def test_extracts_raw_container_number(self):
        """Test extraction without 'container' prefix."""
        result = extract_container_number("WXYZ9876543")
        assert result == "WXYZ9876543"

    def test_extracts_lowercase_container_number(self):
        """Test extraction and uppercase conversion."""
        result = extract_container_number("container abcd1234567")
        assert result == "ABCD1234567"

    def test_extracts_from_sentence(self):
        """Test extraction from a full sentence."""
        result = extract_container_number("What is the ETA for container MNOP5555555?")
        assert result == "MNOP5555555"

    def test_returns_none_for_no_match(self):
        """Test returns None when no container number found."""
        result = extract_container_number("no shipment data")
        assert result is None

    def test_handles_empty_string(self):
        """Test handles empty string input."""
        result = extract_container_number("")
        assert result is None


class TestExtractPoNumber:
    """Test cases for extract_po_number function."""

    def test_extracts_po_with_prefix(self):
        """Test extraction with 'PO' prefix."""
        result = extract_po_number("PO 123456")
        assert result == "123456"

    def test_extracts_purchase_order(self):
        """Test extraction with 'purchase order' phrase."""
        result = extract_po_number("purchase order 789012345")
        assert result == "789012345"

    def test_extracts_raw_number(self):
        """Test extraction of raw number (6+ digits)."""
        result = extract_po_number("order 1234567890")
        assert result == "1234567890"

    def test_returns_none_for_short_number(self):
        """Test returns None for numbers less than 6 digits."""
        result = extract_po_number("12345")
        assert result is None


class TestExtractOceanBlNumber:
    """Test cases for extract_ocean_bl_number function."""

    def test_extracts_ocean_bl(self):
        """Test extraction with 'ocean bl' prefix."""
        result = extract_ocean_bl_number("ocean bl 123456789")
        assert result == "123456789"

    def test_extracts_bill_of_lading(self):
        """Test extraction with 'bill of lading' phrase."""
        result = extract_ocean_bl_number("bill of lading 987654321")
        assert result == "987654321"
