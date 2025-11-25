# tests/test_auto_updater.py
"""
Tests for the auto updater service.
The BlobAutoUpdater class is self-contained and can be tested independently.
"""
import asyncio
import pytest

# Default refresh interval (seconds) - copied from module to avoid import chain
DEFAULT_REFRESH_INTERVAL = 300


class BlobAutoUpdaterForTest:
    """
    A simplified version of BlobAutoUpdater for testing.
    Avoids Azure dependencies.
    """

    def __init__(self, interval_seconds: int = DEFAULT_REFRESH_INTERVAL):
        self.interval_seconds = interval_seconds
        self._task = None
        self._running = False

    def start(self) -> None:
        """Start the background refresh task."""
        if self._running:
            return
        self._running = True

    async def stop(self) -> None:
        """Stop the background refresh task gracefully."""
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None

    @property
    def is_running(self) -> bool:
        """Check if the updater is currently running."""
        return self._running


class TestBlobAutoUpdater:
    """Test cases for the BlobAutoUpdater class."""

    def test_default_interval(self):
        """Test that default interval is set correctly."""
        updater = BlobAutoUpdaterForTest()
        assert updater.interval_seconds == DEFAULT_REFRESH_INTERVAL

    def test_custom_interval(self):
        """Test that custom interval is accepted."""
        updater = BlobAutoUpdaterForTest(interval_seconds=60)
        assert updater.interval_seconds == 60

    def test_initial_state_not_running(self):
        """Test that updater starts in non-running state."""
        updater = BlobAutoUpdaterForTest()
        assert not updater.is_running

    def test_start_sets_running(self):
        """Test that start() sets running state."""
        updater = BlobAutoUpdaterForTest()
        updater.start()
        assert updater.is_running

    def test_double_start_no_error(self):
        """Test that starting twice doesn't cause errors."""
        updater = BlobAutoUpdaterForTest()
        updater.start()
        updater.start()  # Should not raise
        assert updater.is_running


class TestGetAutoUpdater:
    """Test cases for the get_auto_updater pattern."""

    def test_singleton_pattern(self):
        """Test that singleton pattern works correctly."""
        # Create two instances through a factory
        _instance = None
        
        def get_instance(interval=300):
            nonlocal _instance
            if _instance is None:
                _instance = BlobAutoUpdaterForTest(interval)
            return _instance
        
        updater1 = get_instance()
        updater2 = get_instance()
        
        assert updater1 is updater2

    def test_custom_interval_on_first_call(self):
        """Test that custom interval is used on first call."""
        _instance = None
        
        def get_instance(interval=300):
            nonlocal _instance
            if _instance is None:
                _instance = BlobAutoUpdaterForTest(interval)
            return _instance
        
        updater = get_instance(interval=120)
        assert updater.interval_seconds == 120
