from dataclasses import asdict, dataclass
from pathlib import Path

from playwright.sync_api import Page

from config.sandbox import (
    APP_BASE_URL,
    DASHBOARD_PATH,
    METRICS_API_ROUTE,
)
from pages.base_page import BasePage
from pages.components.metrics_panel import MetricsPanel

DASHBOARD_HTML = Path(__file__).resolve().parent.parent / "fixtures" / "dashboard.html"


@dataclass(frozen=True)
class DashboardMetrics:
    """Shape of the /v1/metrics response payload."""

    total_event_count: int
    system_status: str
    workflow_accuracy: str

    def to_payload(self) -> dict:
        return asdict(self)


class DashboardPage(BasePage):
    """Page object for the LocalHost Analytics Dashboard."""

    PATH = DASHBOARD_PATH
    METRICS_API = METRICS_API_ROUTE

    def __init__(self, page: Page, base_url: str = APP_BASE_URL) -> None:
        super().__init__(page, base_url)
        self.metrics = MetricsPanel(page)

    def open(self) -> "DashboardPage":
        self.goto(self.PATH)
        return self

    def serve_mock_ui(self) -> "DashboardPage":
        html = DASHBOARD_HTML.read_text(encoding="utf-8")

        def fulfill(route) -> None:
            route.fulfill(status=200, content_type="text/html", body=html)

        self.page.route(f"**{self.PATH}", fulfill)
        return self

    def mock_metrics(self, metrics: DashboardMetrics) -> "DashboardPage":
        payload = metrics.to_payload()

        def fulfill(route) -> None:
            route.fulfill(
                status=200,
                content_type="application/json",
                json=payload,
            )

        self.page.route(self.METRICS_API, fulfill)
        return self

    @staticmethod
    def default_metrics(**overrides) -> DashboardMetrics:
        defaults = {
            "total_event_count": 0,
            "system_status": "HEALTHY",
            "workflow_accuracy": "95.0%",
        }
        defaults.update(overrides)
        return DashboardMetrics(**defaults)
