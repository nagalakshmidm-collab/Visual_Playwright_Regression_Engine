from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage


def test_mock_dashboard_and_visual_snapshot(page: Page, assert_snapshot):
    dashboard = DashboardPage(page)
    metrics = dashboard.default_metrics(
        total_event_count=999999,
        system_status="CRITICAL_OVERLOAD",
        workflow_accuracy="99.8%",
    )

    dashboard.serve_mock_ui().mock_metrics(metrics).open()

    dashboard.metrics.expect_event_count("999,999")
    dashboard.metrics.expect_system_status("CRITICAL_OVERLOAD")

    assert_snapshot(dashboard.metrics.screenshot())
