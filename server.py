import asyncio
import logging
from typing import Optional

logger = logging.getLogger("LoadBalancer")


class ServerCapacityExceededError(Exception):
    """Raised when a server has reached its maximum connection capacity."""
    pass


class Server:
    """
    Represents an HTTPS backend server with a defined capacity limit,
    active connection tracking, and CPU load monitoring/alerting.
    """

    def __init__(
        self,
        server_id: str,
        url: str,
        capacity: int = 20,
        alert_threshold_pct: float = 80.0,
    ):
        """
        :param server_id: Unique identifier for the server (e.g. 'server-1')
        :param url: HTTPS URL representing the backend server endpoint
        :param capacity: Maximum concurrent connections/requests the server can handle
        :param alert_threshold_pct: Percentage threshold for triggering CPU load alert
        """
        if not url.startswith("https://"):
            raise ValueError(f"Server URL must use HTTPS protocol: {url}")
        if capacity <= 0:
            raise ValueError("Capacity limit must be greater than 0")

        self.server_id = server_id
        self.url = url
        self.capacity = capacity
        self.alert_threshold_pct = alert_threshold_pct
        self.active_connections = 0
        self.total_requests_processed = 0
        self._lock = asyncio.Lock()

    @property
    def cpu_load(self) -> float:
        """
        Calculates the current CPU load percentage based on active connections
        relative to the server capacity limit.
        """
        return min(100.0, (self.active_connections / self.capacity) * 100.0)

    @property
    def is_available(self) -> bool:
        """Returns True if the server can accept more connections."""
        return self.active_connections < self.capacity

    def check_cpu_alert(self) -> Optional[str]:
        """
        Checks if the server CPU load is approaching 100% (exceeding alert_threshold_pct).
        Returns an alert message if threshold is reached or exceeded, else None.
        """
        current_load = self.cpu_load
        if current_load >= self.alert_threshold_pct:
            alert_msg = (
                f"[ALERT] Server {self.server_id} ({self.url}) is approaching 100% CPU load! "
                f"Current CPU: {current_load:.1f}% ({self.active_connections}/{self.capacity} active connections)"
            )
            logger.warning(alert_msg)
            return alert_msg
        return None

    async def handle_request(self, request_id: int, processing_time: float) -> dict:
        """
        Simulates processing an incoming HTTPS request on this server.

        :param request_id: Identifier of the request
        :param processing_time: Simulated processing time in seconds
        :return: Response dictionary containing execution metadata
        """
        async with self._lock:
            if not self.is_available:
                raise ServerCapacityExceededError(
                    f"Server {self.server_id} capacity limit of {self.capacity} reached."
                )
            self.active_connections += 1
            logger.info(
                f"[TRAFFIC] Request #{request_id} assigned to {self.server_id} "
                f"(Active: {self.active_connections}/{self.capacity}, CPU: {self.cpu_load:.1f}%)"
            )
            self.check_cpu_alert()

        try:
            # Simulate request processing
            await asyncio.sleep(processing_time)
            return {
                "request_id": request_id,
                "server_id": self.server_id,
                "url": self.url,
                "processing_time": processing_time,
                "status": 200,
            }
        finally:
            async with self._lock:
                self.active_connections -= 1
                self.total_requests_processed += 1
                logger.info(
                    f"[TRAFFIC] Request #{request_id} completed on {self.server_id} "
                    f"in {processing_time:.2f}s (Active: {self.active_connections}/{self.capacity}, CPU: {self.cpu_load:.1f}%)"
                )

    def __repr__(self) -> str:
        return (
            f"<Server id={self.server_id} url={self.url} "
            f"active={self.active_connections}/{self.capacity} cpu={self.cpu_load:.1f}%>"
        )
