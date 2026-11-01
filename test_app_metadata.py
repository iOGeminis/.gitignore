import json
from pathlib import Path
import unittest

from app_metadata import AppMetadata, Category


class TestAppMetadata(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "appId": "com.google.android.calculator",
            "title": "Calculator",
            "url": "https://play.google.com/store/apps/details?id=com.google.android.calculator",
            "developer": "Google LLC",
            "developerId": "5700313618786177705",
            "developerDevProfile": "g.dev/5700313618786177705MX",
            "developerEmail": "apps-help@google.com",
            "developerAlternativeEmail": "Workspace.iah@gmail.com",
            "developerWebsite": "https://support.google.com/calculator",
            "developerAddress": "1600 Amphitheatre Parkway, Mountain View 94043",
            "score": 4.32,
            "ratings": 1234567,
            "reviewCount": 98765,
            "histogram": [50000, 30000, 40000, 150000, 964567],
            "installs": "1,000,000,000+",
            "minInstalls": 1000000000,
            "realInstalls": 1523456789,
            "price": 0,
            "free": True,
            "currency": "USD",
            "genre": "Tools",
            "genreId": "TOOLS",
            "categories": [{"name": "Tools", "id": "TOOLS"}],
            "icon": "https://play-lh.googleusercontent.com/...",
            "headerImage": "https://play-lh.googleusercontent.com/...",
            "screenshots": ["https://play-lh.googleusercontent.com/..."],
            "video": "",
            "contentRating": "Everyone",
            "adSupported": False,
            "containsAds": False,
            "released": "Oct 22, 2014",
            "lastUpdated": "2025-01-15 00:00:00",
            "version": "8.8",
            "description": "A simple calculator app...",
            "recentChanges": "Bug fixes and performance improvements",
            "privacyPolicy": "https://policies.google.com/privacy",
            "reviews": [],
            "scrapedAt": "2025-06-15T12:00:00.000Z",
        }

    def test_from_dict_success(self):
        meta = AppMetadata.from_dict(self.sample_data)
        self.assertEqual(meta.app_id, "com.google.android.calculator")
        self.assertEqual(meta.title, "Calculator")
        self.assertEqual(meta.developer, "Google LLC")
        self.assertEqual(meta.developer_id, "5700313618786177705")
        self.assertEqual(meta.developer_dev_profile, "g.dev/5700313618786177705MX")
        self.assertEqual(meta.developer_email, "apps-help@google.com")
        self.assertEqual(meta.developer_alternative_email, "Workspace.iah@gmail.com")
        self.assertEqual(meta.score, 4.32)
        self.assertEqual(meta.ratings, 1234567)
        self.assertEqual(meta.min_installs, 1000000000)
        self.assertEqual(len(meta.categories), 1)
        self.assertEqual(meta.categories[0].name, "Tools")
        self.assertEqual(meta.categories[0].id, "TOOLS")

    def test_required_fields_validation(self):
        with self.assertRaises(ValueError):
            AppMetadata.from_dict({"title": "Calculator"})

        with self.assertRaises(ValueError):
            AppMetadata.from_dict({"appId": "com.example.app"})

    def test_load_from_json_file(self):
        json_path = Path("app_metadata.json")
        self.assertTrue(json_path.exists())
        meta = AppMetadata.load_from_file(json_path)
        self.assertEqual(meta.app_id, "com.google.android.calculator")
        self.assertEqual(meta.title, "Calculator")
        self.assertEqual(meta.genre, "Tools")
        self.assertEqual(meta.developer_id, "5700313618786177705")

    def test_to_dict_roundtrip(self):
        meta = AppMetadata.from_dict(self.sample_data)
        d = meta.to_dict()
        self.assertEqual(d["appId"], self.sample_data["appId"])
        self.assertEqual(d["title"], self.sample_data["title"])
        self.assertEqual(d["developer"], self.sample_data["developer"])
        self.assertEqual(d["developerDevProfile"], self.sample_data["developerDevProfile"])
        self.assertEqual(d["developerAlternativeEmail"], self.sample_data["developerAlternativeEmail"])
        self.assertEqual(d["score"], 4.32)
        self.assertEqual(d["categories"], [{"name": "Tools", "id": "TOOLS"}])


if __name__ == "__main__":
    unittest.main()
