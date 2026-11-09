import os
import unittest
from pathlib import Path


class TestIoWiki(unittest.TestCase):
    def setUp(self):
        self.css_path = Path("snippets/other-projects-icons.css")
        self.html_path = Path("index.html")

    def test_css_snippet_exists_and_valid(self):
        self.assertTrue(self.css_path.exists(), "snippets/other-projects-icons.css should exist")
        content = self.css_path.read_text(encoding="utf-8")

        # Verify selectors
        expected_selectors = [
            "#p-wikibase-otherprojects li:before",
            ".wb-otherproject-link[class*=\"badge-\"]:before",
            "#p-wikibase-otherprojects li.wb-otherproject-wikipedia:before",
            ".wb-otherproject-commons:before",
            ".wb-otherproject-mediawiki:before",
            ".wb-otherproject-meta:before",
            ".wb-otherproject-species:before",
            ".wb-otherproject-wikibooks:before",
            ".wb-otherproject-wikidata:before",
            ".wb-otherproject-wikinews:before",
            ".wb-otherproject-wikiquote:before",
            ".wb-otherproject-wikisource:before",
            ".wb-otherproject-wikiversity:before",
            ".wb-otherproject-wikivoyage:before",
            ".wb-otherproject-wiktionary:before",
            ".skin-monobook #p-wikibase-otherprojects ul",
            ".skin-modern #p-wikibase-otherprojects li",
            "-webkit-min-device-pixel-ratio: 1.5",
        ]
        for sel in expected_selectors:
            self.assertIn(sel, content, f"Missing selector/rule in CSS: {sel}")

    def test_index_html_structure_and_content(self):
        self.assertTrue(self.html_path.exists(), "index.html should exist")
        content = self.html_path.read_text(encoding="utf-8")

        # Verify Ensiclopedia iOWiki branding
        self.assertIn("Ensiclopedia iOWiki", content)
        self.assertIn("🐻‍❄️", content)

        # Verify Conference Announcement
        self.assertIn("MediaWiki Users and Developers Conference Fall 2026", content)
        self.assertIn("Ljubljana, Slovenia", content)

        # Verify Certificate details
        self.assertIn("www.google.com", content)
        self.assertIn("47:DB:E4:E1:85:9A:DA:DC:0A:4D:8B:CA:DE D :BC:70:BD", content)
        self.assertIn("Google Trust Services", content)
        self.assertIn("7 oct. 2026", content)
        self.assertIn("30 dic. 2026", content)
        self.assertIn("83 B9 C3 FF B5 3E D1 EE F2 84 93 24 F5 36 43 0B 19 1D D5 BD 5F 98 D3 F6 43 E3 97 88 4A C9 C6 CB", content)
        self.assertIn("BO DO C5 80 D2 69 3A C9 FF 7D 53 25 C6 69 7D CE 58 26 4A 57 FF 37 11 E8 B9 6E E 3E 09 82 21 DB A5", content)

        # Verify Other Projects sidebar links
        self.assertIn("wb-otherproject-wikipedia", content)
        self.assertIn("wb-otherproject-commons", content)
        self.assertIn("wb-otherproject-mediawiki", content)
        self.assertIn("wb-otherproject-meta", content)
        self.assertIn("wb-otherproject-species", content)
        self.assertIn("wb-otherproject-wikibooks", content)
        self.assertIn("wb-otherproject-wikidata", content)
        self.assertIn("wb-otherproject-wikinews", content)
        self.assertIn("wb-otherproject-wikiquote", content)
        self.assertIn("wb-otherproject-wikisource", content)
        self.assertIn("wb-otherproject-wikiversity", content)
        self.assertIn("wb-otherproject-wikivoyage", content)
        self.assertIn("wb-otherproject-wiktionary", content)


if __name__ == "__main__":
    unittest.main()
