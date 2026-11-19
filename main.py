import asyncio
import logging
import random
import sys
from load_balancer import LoadBalancer
from server import Server

# Configure structured logging with timestamp and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger("LoadBalancer")


async def generate_requests(
    load_balancer: LoadBalancer,
    num_requests: int = 50,
    min_time: float = 0.5,
    max_time: float = 2.0,
    arrival_interval: float = 0.05,
):
    """
    Generates concurrent HTTPS requests with random processing times.
    Dispatches them dynamically to the Load Balancer using Least Connections.
    """
    logger.info("=" * 70)
    logger.info(f"Starting simulation: Generating {num_requests} concurrent HTTPS requests...")
    logger.info("=" * 70)

    tasks = []

    for req_id in range(1, num_requests + 1):
        # Random processing time between min_time and max_time
        processing_time = round(random.uniform(min_time, max_time), 2)
        task = asyncio.create_task(load_balancer.route_request(req_id, processing_time))
        tasks.append(task)
        # Small delay between incoming arrivals to create realistic concurrent burst
        await asyncio.sleep(arrival_interval)

    # Wait for all requests to finish
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def main():
    # Define 3 backend servers with HTTPS URLs and capacity limit
    # Capacity is set to 18 per server so 50 concurrent requests will approach/exceed 80% CPU load
    servers = [
        Server(server_id="server-alpha", url="https://backend-1.internal.net", capacity=18, alert_threshold_pct=80.0),
        Server(server_id="server-beta", url="https://backend-2.internal.net", capacity=18, alert_threshold_pct=80.0),
        Server(server_id="server-gamma", url="https://backend-3.internal.net", capacity=18, alert_threshold_pct=80.0),
    ]

    lb = LoadBalancer(servers=servers)

    # Generate 50 concurrent requests
    results = await generate_requests(lb, num_requests=50, min_time=0.8, max_time=2.5, arrival_interval=0.03)

    successful = sum(1 for r in results if isinstance(r, dict) and r.get("status") == 200)
    errors = sum(1 for r in results if isinstance(r, Exception))

    logger.info("=" * 70)
    logger.info("SIMULATION COMPLETE - FINAL CLUSTER REPORT")
    logger.info("=" * 70)
    logger.info(f"Total Requests Dispatched: {len(results)} | Successful: {successful} | Failed: {errors}")
    for status in lb.get_cluster_status():
        logger.info(
            f"Server {status['server_id']} ({status['url']}): "
            f"Processed: {status['total_processed']} | "
            f"Active: {status['active_connections']}/{status['capacity']} | "
            f"Final CPU Load: {status['cpu_load_pct']}%"
        )
    logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
