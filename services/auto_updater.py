# services/auto_updater.py
"""
Background poller that refreshes the cached blob DataFrame at a configurable interval.
The FastAPI app starts this task automatically on startup; the CLI can also start it on demand.
"""
import asyncio
import logging
from typing import Optional

logger = logging.getLogger("shipping_chatbot")

# Default refresh interval (seconds) if not set in config
DEFAULT_REFRESH_INTERVAL = 300


class BlobAutoUpdater:
    """
    A background task that periodically refreshes the shipment data from Azure Blob.
    Thread-safe and can be started/stopped cleanly.
    """

    def __init__(self, interval_seconds: int = DEFAULT_REFRESH_INTERVAL):
        self.interval_seconds = interval_seconds
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def _refresh_loop(self) -> None:
        """Internal loop that periodically refreshes the blob data."""
        from .azure_blob import download_shipment_csv
        from .preprocess import preprocess_data
        import services.azure_blob as azure_blob_module

        logger.info(
            f"BlobAutoUpdater started – refreshing every {self.interval_seconds}s"
        )

        while self._running:
            try:
                await asyncio.sleep(self.interval_seconds)

                if not self._running:
                    break

                logger.info("BlobAutoUpdater: Checking for blob updates...")

                # Download and preprocess the data
                raw_df = download_shipment_csv()
                processed_df = preprocess_data(raw_df)

                # Update the cached DataFrame
                azure_blob_module._cached_df = processed_df

                logger.info(
                    f"BlobAutoUpdater: Refreshed cache with {len(processed_df)} rows"
                )

            except asyncio.CancelledError:
                logger.info("BlobAutoUpdater: Task cancelled")
                break
            except Exception as exc:
                logger.error(f"BlobAutoUpdater: Error during refresh: {exc}")
                # Continue running; will retry on next interval

        logger.info("BlobAutoUpdater stopped")

    def start(self) -> None:
        """Start the background refresh task."""
        if self._running:
            logger.warning("BlobAutoUpdater is already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._refresh_loop())
        logger.info("BlobAutoUpdater task created")

    async def stop(self) -> None:
        """Stop the background refresh task gracefully."""
        if not self._running:
            return

        self._running = False

        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

        logger.info("BlobAutoUpdater stopped")

    @property
    def is_running(self) -> bool:
        """Check if the updater is currently running."""
        return self._running


# Singleton instance for the app
_auto_updater: Optional[BlobAutoUpdater] = None


def get_auto_updater(interval_seconds: int = DEFAULT_REFRESH_INTERVAL) -> BlobAutoUpdater:
    """Get or create the singleton BlobAutoUpdater instance."""
    global _auto_updater
    if _auto_updater is None:
        _auto_updater = BlobAutoUpdater(interval_seconds)
    return _auto_updater
