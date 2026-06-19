from playwright.sync_api import Locator, Page, expect


class MetricsPanel:
    """Page component for the dashboard metrics panel and its child widgets."""

    ROOT = "#metrics-panel"
    EVENT_COUNTER = "#event-counter"
    STATUS_BADGE = "#status-badge"
    WORKFLOW_ACCURACY = "#workflow-accuracy"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.root: Locator = page.locator(self.ROOT)
        self.event_counter: Locator = page.locator(self.EVENT_COUNTER)
        self.status_badge: Locator = page.locator(self.STATUS_BADGE)
        self.workflow_accuracy: Locator = page.locator(self.WORKFLOW_ACCURACY)

    def is_visible(self) -> None:
        expect(self.root).to_be_visible()

    def event_count(self) -> str:
        return self.event_counter.inner_text()

    def system_status(self) -> str:
        return self.status_badge.inner_text()

    def workflow_accuracy_text(self) -> str:
        return self.workflow_accuracy.inner_text()

    def expect_event_count(self, value: str) -> None:
        expect(self.event_counter).to_have_text(value)

    def expect_system_status(self, value: str) -> None:
        expect(self.status_badge).to_have_text(value)

    def expect_workflow_accuracy(self, value: str) -> None:
        expect(self.workflow_accuracy).to_have_text(value)

    def screenshot(self) -> bytes:
        return self.root.screenshot()
