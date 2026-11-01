import asyncio
import unittest
from server import Server, ServerCapacityExceededError
from load_balancer import LoadBalancer, NoAvailableServerException


class TestServer(unittest.IsolatedAsyncioTestCase):
    def test_https_validation(self):
        with self.assertRaises(ValueError):
            Server("s1", "http://insecure.net", capacity=10)

        with self.assertRaises(ValueError):
            Server("s1", "ftp://invalid.net", capacity=10)

        # Valid HTTPS server
        server = Server("s1", "https://secure.net", capacity=10)
        self.assertEqual(server.server_id, "s1")
        self.assertEqual(server.url, "https://secure.net")
        self.assertEqual(server.capacity, 10)

    def test_capacity_validation(self):
        with self.assertRaises(ValueError):
            Server("s1", "https://secure.net", capacity=0)
        with self.assertRaises(ValueError):
            Server("s1", "https://secure.net", capacity=-5)

    def test_cpu_load_calculation(self):
        server = Server("s1", "https://secure.net", capacity=10)
        self.assertEqual(server.cpu_load, 0.0)

        server.active_connections = 5
        self.assertEqual(server.cpu_load, 50.0)

        server.active_connections = 10
        self.assertEqual(server.cpu_load, 100.0)

    def test_cpu_alert(self):
        server = Server("s1", "https://secure.net", capacity=10, alert_threshold_pct=80.0)
        server.active_connections = 7  # 70%
        self.assertIsNone(server.check_cpu_alert())

        server.active_connections = 8  # 80% - approaching 100%
        alert = server.check_cpu_alert()
        self.assertIsNotNone(alert)
        self.assertIn("approaching 100% CPU load", alert)

        server.active_connections = 9  # 90%
        alert = server.check_cpu_alert()
        self.assertIsNotNone(alert)
        self.assertIn("90.0%", alert)

    async def test_handle_request(self):
        server = Server("s1", "https://secure.net", capacity=2)
        res = await server.handle_request(1, 0.05)
        self.assertEqual(res["status"], 200)
        self.assertEqual(res["request_id"], 1)
        self.assertEqual(server.total_requests_processed, 1)
        self.assertEqual(server.active_connections, 0)

    async def test_capacity_exceeded(self):
        server = Server("s1", "https://secure.net", capacity=1)
        server.active_connections = 1
        with self.assertRaises(ServerCapacityExceededError):
            await server.handle_request(2, 0.05)


class TestLoadBalancer(unittest.IsolatedAsyncioTestCase):
    def test_default_initialization(self):
        lb = LoadBalancer()
        self.assertEqual(len(lb.servers), 3)
        for s in lb.servers:
            self.assertTrue(s.url.startswith("https://"))

    def test_least_connections_selection(self):
        s1 = Server("s1", "https://s1.internal", capacity=10)
        s2 = Server("s2", "https://s2.internal", capacity=10)
        s3 = Server("s3", "https://s3.internal", capacity=10)

        lb = LoadBalancer(servers=[s1, s2, s3])

        # Initially all have 0 connections, selects first
        chosen = lb.select_server()
        self.assertEqual(chosen.server_id, "s1")

        s1.active_connections = 3
        s2.active_connections = 1
        s3.active_connections = 2

        # Least connections should pick s2
        chosen = lb.select_server()
        self.assertEqual(chosen.server_id, "s2")

        # Now s2 gets busy
        s2.active_connections = 4
        # Least connections should pick s3 (2 connections)
        chosen = lb.select_server()
        self.assertEqual(chosen.server_id, "s3")

    def test_no_available_server_exception(self):
        s1 = Server("s1", "https://s1.internal", capacity=1)
        s2 = Server("s2", "https://s2.internal", capacity=1)
        s3 = Server("s3", "https://s3.internal", capacity=1)

        s1.active_connections = 1
        s2.active_connections = 1
        s3.active_connections = 1

        lb = LoadBalancer(servers=[s1, s2, s3])
        with self.assertRaises(NoAvailableServerException):
            lb.select_server()

    async def test_concurrent_50_requests(self):
        # 3 backend servers with capacity 20 each (total capacity 60 > 50)
        servers = [
            Server("s1", "https://s1.net", capacity=25, alert_threshold_pct=75.0),
            Server("s2", "https://s2.net", capacity=25, alert_threshold_pct=75.0),
            Server("s3", "https://s3.net", capacity=25, alert_threshold_pct=75.0),
        ]
        lb = LoadBalancer(servers=servers)

        tasks = [
            asyncio.create_task(lb.route_request(request_id=i, processing_time=0.05))
            for i in range(1, 51)
        ]

        results = await asyncio.gather(*tasks)
        self.assertEqual(len(results), 50)
        for r in results:
            self.assertEqual(r["status"], 200)

        total_processed = sum(s.total_requests_processed for s in servers)
        self.assertEqual(total_processed, 50)

        # Confirm traffic was distributed among all 3 servers
        for s in servers:
            self.assertGreater(s.total_requests_processed, 0)
            self.assertEqual(s.active_connections, 0)


if __name__ == "__main__":
    unittest.main()
