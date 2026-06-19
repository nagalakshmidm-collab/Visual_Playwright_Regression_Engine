import os
import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

from config.sandbox import APP_BASE_URL


@pytest.fixture(scope="session")
def base_url():
    return APP_BASE_URL


@pytest.fixture
def browser_context_args(browser_context_args):
    """Keep rendering consistent between headed and headless runs."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "device_scale_factor": 1,
    }


@pytest.fixture
def assert_snapshot(request):
    """
    Custom fixture to handle pixel-by-pixel visual regression testing
    using pixelmatch and Pillow.
    """
    # Create directories for snapshots and failure diffs
    snapshots_dir = os.path.join(request.config.rootdir, "snapshots")
    failures_dir = os.path.join(request.config.rootdir, "snapshot_failures")
    os.makedirs(snapshots_dir, exist_ok=True)
    os.makedirs(failures_dir, exist_ok=True)

    # Automatically generate a unique snapshot name based on the test name
    test_name = request.node.name.replace("[", "_").replace("]", "")
    headed = request.config.getoption("--headed", default=False)
    mode_suffix = "_headed" if headed else ""
    snapshot_path = os.path.join(snapshots_dir, f"{test_name}{mode_suffix}.png")

    def _assert(actual_screenshot_bytes, threshold=0.1):
        # 1. If the baseline/golden snapshot doesn't exist, create it
        if not os.path.exists(snapshot_path):
            with open(snapshot_path, "wb") as f:
                f.write(actual_screenshot_bytes)
            pytest.fail(f"📸 New baseline snapshot created at {snapshot_path}. Please review and re-run the test.")

        # 2. If baseline exists, perform pixel comparison
        # Save actual screenshot to a temporary path for comparison
        actual_path = os.path.join(failures_dir, f"{test_name}_actual.png")
        with open(actual_path, "wb") as f:
            f.write(actual_screenshot_bytes)

        img_expected = Image.open(snapshot_path).convert("RGBA")
        img_actual = Image.open(actual_path).convert("RGBA")

        # Ensure identical dimensions
        if img_expected.size != img_actual.size:
            pytest.fail(f"❌ Snapshot mismatch: Baseline size {img_expected.size} does not match actual size {img_actual.size}")

        img_diff = Image.new("RGBA", img_expected.size)

        # Run pixelmatch comparison
        mismatched_pixels = pixelmatch(img_expected, img_actual, img_diff, threshold=threshold)

        # 3. Handle visual test failures
        if mismatched_pixels > 0:
            diff_path = os.path.join(failures_dir, f"{test_name}_diff.png")
            img_diff.save(diff_path)
            pytest.fail(
                f"❌ Visual Regression Failure! Mismatched pixels: {mismatched_pixels}.\n"
                f"Expected: {snapshot_path}\n"
                f"Actual: {actual_path}\n"
                f"Diff generated at: {diff_path}"
            )
        
        # Clean up temporary actual image if the test passes
        if os.path.exists(actual_path):
            os.remove(actual_path)

    return _assert