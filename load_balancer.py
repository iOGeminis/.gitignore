import asyncio
import logging
from typing import List, Optional
from server import Server

logger = logging.getLogger("LoadBalancer")


class NoAvailableServerException(Exception):
    """Raised when no backend server is available to handle a request."""
    pass


class LoadBalancer:
    """
    Load Balancer that distributes HTTPS traffic across backend servers
    using the 'Least Connections' algorithm dynamically.
    """

    def __init__(self, servers: Optional[List[Server]] = None):
        if servers is None:
            # Default to 3 backend HTTPS servers as specified
            self.servers: List[Server] = [
                Server(server_id="server-1", url="https://backend1.internal.net", capacity=20, alert_threshold_pct=80.0),
                Server(server_id="server-2", url="https://backend2.internal.net", capacity=20, alert_threshold_pct=80.0),
                Server(server_id="server-3", url="https://backend3.internal.net", capacity=20, alert_threshold_pct=80.0),
            ]
        else:
            self.servers = servers

        self._selection_lock = asyncio.Lock()
        logger.info(f"Load Balancer initialized with {len(self.servers)} backend servers:")
        for s in self.servers:
            logger.info(f" - {s.server_id} @ {s.url} (Capacity: {s.capacity}, Alert threshold: {s.alert_threshold_pct}%)")

    def select_server(self) -> Server:
        """
        Implements 'Least Connections' algorithm:
        Finds the available server with the fewest active connections.
        In case of a tie, selects the one with the lowest CPU load / first available.
        """
        available_servers = [s for s in self.servers if s.is_available]
        if not available_servers:
            raise NoAvailableServerException("All backend servers are at maximum capacity!")

        # Sort primarily by active connections, secondarily by current cpu_load
        selected = min(available_servers, key=lambda s: (s.active_connections, s.cpu_load))
        return selected

    async def route_request(self, request_id: int, processing_time: float) -> dict:
        """
        Dynamically routes an HTTPS request to the server chosen by Least Connections.

        :param request_id: Unique request identifier
        :param processing_time: Processing duration
        :return: Response dictionary from backend server
        """
        async with self._selection_lock:
            server = self.select_server()
            logger.info(
                f"[ROUTING] Incoming HTTPS request #{request_id} -> routing to {server.server_id} "
                f"(current active connections: {server.active_connections})"
            )

        # Dispatch the request to the chosen server
        return await server.handle_request(request_id, processing_time)

    def get_cluster_status(self) -> List[dict]:
        """Returns the current state and metrics of all backend servers."""
        return [
            {
                "server_id": s.server_id,
                "url": s.url,
                "active_connections": s.active_connections,
                "capacity": s.capacity,
                "cpu_load_pct": round(s.cpu_load, 2),
                "total_processed": s.total_requests_processed,
            }
            for s in self.servers
        ]
