# tests/conftest.py
"""
Pytest configuration and shared fixtures for the shipping chatbot tests.
Note: These fixtures require Azure dependencies to be installed and configured.
For unit tests without Azure dependencies, see individual test files.
"""
import pandas as pd
import pytest


@pytest.fixture
def sample_shipment_df() -> pd.DataFrame:
    """
    Create a sample shipment DataFrame for testing.
    This fixture provides mock data that matches the expected schema.
    """
    data = {
        "container_number": ["ABCD1234567", "WXYZ9876543", "MNOP5555555", "TEST1111111"],
        "consignee_code_multiple": ["CUST001", "CUST002", "CUST001,CUST003", "CUST002"],
        "po_number_multiple": ["PO123456", "PO789012", "PO345678", "PO901234"],
        "booking_number_multiple": ["BKG001", "BKG002", "BKG003", "BKG004"],
        "ocean_bl_no_multiple": ["BL001", "BL002", "BL003", "BL004"],
        "load_port": ["Shanghai", "Busan", "Singapore", "Rotterdam"],
        "discharge_port": ["Los Angeles", "Long Beach", "Seattle", "New York"],
        "final_destination": ["Chicago", "Denver", "Portland", "Boston"],
        "first_vessel_name": ["Ever Given", "MSC Maya", "CMA CGM", "Maersk Line"],
        "first_vessel_code": ["EVGV", "MSCM", "CMAC", "MAER"],
        "first_voyage_code": ["V001", "V002", "V003", "V004"],
        "final_vessel_name": ["Ever Given", "MSC Maya", "CMA CGM", "Maersk Line"],
        "final_vessel_code": ["EVGV", "MSCM", "CMAC", "MAER"],
        "final_voyage_code": ["V001", "V002", "V003", "V004"],
        "etd_lp": pd.to_datetime(["2025-01-01", "2025-01-05", "2025-01-10", "2025-01-15"]),
        "eta_dp": pd.to_datetime(["2025-01-20", "2025-01-25", "2025-01-30", "2025-02-05"]),
        "ata_dp": pd.to_datetime(["2025-01-22", "2025-01-28", None, None]),
        "eta_fd": pd.to_datetime(["2025-01-25", "2025-01-30", "2025-02-05", "2025-02-10"]),
        "revised_eta": pd.to_datetime(["2025-01-21", None, "2025-02-01", None]),
        "predictive_eta": pd.to_datetime([None, "2025-01-26", None, "2025-02-06"]),
        "container_type": ["40HC", "20GP", "40HC", "20GP"],
        "delay_days": [2, 3, None, None],
    }
    return pd.DataFrame(data)
