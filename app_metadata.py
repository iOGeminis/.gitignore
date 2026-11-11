"""
Module to parse, validate, and inspect Google Play app metadata.
"""

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Category:
    name: str
    id: str


@dataclass
class AppMetadata:
    app_id: str
    title: str
    url: str
    developer: str
    developer_id: str
    developer_email: str
    developer_website: str
    developer_address: str
    score: float
    ratings: int
    review_count: int
    histogram: List[int]
    installs: str
    min_installs: int
    real_installs: int
    price: float
    free: bool
    currency: str
    genre: str
    genre_id: str
    categories: List[Category]
    icon: str
    header_image: str
    screenshots: List[str]
    video: str
    content_rating: str
    ad_supported: bool
    contains_ads: bool
    released: str
    last_updated: str
    version: str
    description: str
    recent_changes: str
    privacy_policy: str
    reviews: List[Any]
    scraped_at: str
    developer_dev_profile: Optional[str] = None
    developer_alternative_email: Optional[str] = None
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppMetadata":
        """Create AppMetadata instance from dictionary representation."""
        if not data.get("appId"):
            raise ValueError("appId is required")
        if not data.get("title"):
            raise ValueError("title is required")

        categories = [
            Category(name=c.get("name", ""), id=c.get("id", ""))
            for c in data.get("categories", [])
            if isinstance(c, dict)
        ]

        known_keys = {
            "appId", "title", "url", "developer", "developerId",
            "developerDevProfile", "developerEmail", "developerAlternativeEmail",
            "developerWebsite", "developerAddress", "score", "ratings",
            "reviewCount", "histogram", "installs", "minInstalls",
            "realInstalls", "price", "free", "currency", "genre", "genreId",
            "categories", "icon", "headerImage", "screenshots", "video",
            "contentRating", "adSupported", "containsAds", "released",
            "lastUpdated", "version", "description", "recentChanges",
            "privacyPolicy", "reviews", "scrapedAt"
        }

        extras = {k: v for k, v in data.items() if k not in known_keys}

        return cls(
            app_id=str(data.get("appId", "")),
            title=str(data.get("title", "")),
            url=str(data.get("url", "")),
            developer=str(data.get("developer", "")),
            developer_id=str(data.get("developerId", "")),
            developer_dev_profile=data.get("developerDevProfile"),
            developer_email=str(data.get("developerEmail", "")),
            developer_alternative_email=data.get("developerAlternativeEmail"),
            developer_website=str(data.get("developerWebsite", "")),
            developer_address=str(data.get("developerAddress", "")),
            score=float(data.get("score", 0.0)),
            ratings=int(data.get("ratings", 0)),
            review_count=int(data.get("reviewCount", 0)),
            histogram=list(data.get("histogram", [])),
            installs=str(data.get("installs", "")),
            min_installs=int(data.get("minInstalls", 0)),
            real_installs=int(data.get("realInstalls", 0)),
            price=float(data.get("price", 0.0)),
            free=bool(data.get("free", True)),
            currency=str(data.get("currency", "USD")),
            genre=str(data.get("genre", "")),
            genre_id=str(data.get("genreId", "")),
            categories=categories,
            icon=str(data.get("icon", "")),
            header_image=str(data.get("headerImage", "")),
            screenshots=list(data.get("screenshots", [])),
            video=str(data.get("video", "")),
            content_rating=str(data.get("contentRating", "")),
            ad_supported=bool(data.get("adSupported", False)),
            contains_ads=bool(data.get("containsAds", False)),
            released=str(data.get("released", "")),
            last_updated=str(data.get("lastUpdated", "")),
            version=str(data.get("version", "")),
            description=str(data.get("description", "")),
            recent_changes=str(data.get("recentChanges", "")),
            privacy_policy=str(data.get("privacyPolicy", "")),
            reviews=list(data.get("reviews", [])),
            scraped_at=str(data.get("scrapedAt", "")),
            extra_fields=extras,
        )

    @classmethod
    def load_from_file(cls, filepath: str | Path) -> "AppMetadata":
        """Load and parse metadata from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert AppMetadata instance back to dictionary."""
        data = {
            "appId": self.app_id,
            "title": self.title,
            "url": self.url,
            "developer": self.developer,
            "developerId": self.developer_id,
            "developerEmail": self.developer_email,
            "developerWebsite": self.developer_website,
            "developerAddress": self.developer_address,
            "score": self.score,
            "ratings": self.ratings,
            "reviewCount": self.review_count,
            "histogram": self.histogram,
            "installs": self.installs,
            "minInstalls": self.min_installs,
            "realInstalls": self.real_installs,
            "price": self.price,
            "free": self.free,
            "currency": self.currency,
            "genre": self.genre,
            "genreId": self.genre_id,
            "categories": [{"name": c.name, "id": c.id} for c in self.categories],
            "icon": self.icon,
            "headerImage": self.header_image,
            "screenshots": self.screenshots,
            "video": self.video,
            "contentRating": self.content_rating,
            "adSupported": self.ad_supported,
            "containsAds": self.contains_ads,
            "released": self.released,
            "lastUpdated": self.last_updated,
            "version": self.version,
            "description": self.description,
            "recentChanges": self.recent_changes,
            "privacyPolicy": self.privacy_policy,
            "reviews": self.reviews,
            "scrapedAt": self.scraped_at,
        }
        if self.developer_dev_profile:
            data["developerDevProfile"] = self.developer_dev_profile
        if self.developer_alternative_email:
            data["developerAlternativeEmail"] = self.developer_alternative_email
        data.update(self.extra_fields)
        return data
