# utils/misc.py
import re
import pandas as pd
from typing import Iterable


def to_datetime(series: pd.Series) -> pd.Series:
    """Safe conversion – errors become NaT."""
    return pd.to_datetime(series, errors="coerce")


def clean_container_number(num: str) -> str:
    """Strip everything that isn’t alphanumeric and upper‑case."""
    return re.sub(r'[^A-Z0-9]', '', num.upper())
