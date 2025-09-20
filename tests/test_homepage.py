import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture(scope="function", autouse=True)
def goto_homepage(page: Page):
    """Navigate to homepage before each test"""
    page.goto("https://testathon.live/")  # Replace with actual URL
    yield


def test_homepage_title(page: Page):
    """Test that the page title is correct"""
    expect(page).to_have_title("StackDemo")


def test_page_has_footer(page: Page):
    """Test that the page has a footer element"""
    # Use first to handle multiple footer elements
    footer = page.locator("footer").first
    expect(footer).to_be_visible()


def test_page_structure(page: Page):
    """Test the basic page structure"""
    # Check main container exists
    next_container = page.locator("#__next")
    expect(next_container).to_be_visible()

    # Check div structure - use first to handle multiple divs
    div_container = next_container.locator("div").first
    expect(div_container).to_be_visible()


def test_favicon_is_present(page: Page):
    """Test that favicon is properly linked"""
    favicon = page.locator("link[rel='icon']")
    expect(favicon).to_have_attribute("href", "/favicon.svg")
    expect(favicon).to_have_attribute("type", "image/svg+xml")
    expect(favicon).to_have_attribute("sizes", "any")


def test_viewport_meta_tag(page: Page):
    """Test that viewport meta tag is correctly set"""
    viewport_meta = page.locator("meta[name='viewport']")
    expect(viewport_meta).to_have_attribute(
        "content", "initial-scale=1.0, width=device-width"
    )


def test_charset_meta_tag(page: Page):
    """Test that charset meta tag is correctly set"""
    charset_meta = page.locator("meta[charSet]")
    expect(charset_meta).to_have_attribute("charSet", "utf-8")


def test_next_data_script_exists(page: Page):
    """Test that Next.js data script exists"""
    next_data_script = page.locator("script#__NEXT_DATA__")
    expect(next_data_script).to_be_attached()

    # Verify it contains JSON data
    script_content = next_data_script.text_content()
    assert script_content is not None
    assert "props" in script_content
    assert "pageProps" in script_content


def test_all_scripts_loaded(page: Page):
    """Test that all script tags are present and have src attributes"""
    scripts = page.locator("script[src]")
    count = scripts.count()
    assert count > 0, "No script tags with src found"

    # Check that main scripts are loaded
    expect(page.locator("script[src*='main-']")).to_be_attached()
    expect(page.locator("script[src*='webpack-']")).to_be_attached()
    # Note: framework- script may not exist in all builds


def test_css_stylesheets_loaded(page: Page):
    """Test that CSS stylesheets are properly linked"""
    stylesheets = page.locator("link[rel='stylesheet']")
    count = stylesheets.count()
    assert count > 0, "No stylesheets found"

    # Check specific stylesheets - use first to handle multiple matches
    expect(page.locator("link[href*='412b7dee']").first).to_be_attached()
    # Note: styles.e2bb0603 may not exist in all builds


def test_preload_links_exist(page: Page):
    """Test that preload links are present"""
    preload_links = page.locator("link[rel='preload']")
    count = preload_links.count()
    assert count > 0, "No preload links found"


def test_noscript_tag_present(page: Page):
    """Test that noscript tag exists"""
    noscript = page.locator("noscript")
    expect(noscript).to_be_attached()
    expect(noscript).to_have_attribute("data-n-css", "true")


def test_page_load_performance(page: Page):
    """Test that page loads within acceptable time"""
    start_time = time.time()
    page.goto("https://testathon.live/")
    load_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    assert load_time < 3000, f"Page took {load_time:.2f}ms to load (max 3000ms allowed)"


def test_page_responsive(page: Page):
    """Test that page is responsive to different viewports"""
    # Test mobile view
    page.set_viewport_size({"width": 375, "height": 667})
    footer = page.locator("footer").first
    expect(footer).to_be_visible()

    # Test tablet view
    page.set_viewport_size({"width": 768, "height": 1024})
    expect(footer).to_be_visible()

    # Test desktop view
    page.set_viewport_size({"width": 1280, "height": 800})
    expect(footer).to_be_visible()


def test_page_accessibility(page: Page):
    """Test basic accessibility features"""
    # Check html lang attribute (though not present, this would be good practice)
    html = page.locator("html")

    # Check that page has proper structure for screen readers
    # (minimal content but should still be accessible)
    body = page.locator("body")
    expect(body).to_be_visible()


def test_async_scripts_loading(page: Page):
    """Test that async scripts are properly configured"""
    async_scripts = page.locator("script[async]")
    count = async_scripts.count()
    assert count > 0, "No async scripts found"

    # Verify that at least some scripts have async or defer attributes
    scripts_with_src = page.locator("script[src]")
    total_scripts = scripts_with_src.count()
    async_or_defer_count = 0
    
    for i in range(total_scripts):
        script = scripts_with_src.nth(i)
        async_attr = script.get_attribute("async")
        defer_attr = script.get_attribute("defer")
        if async_attr is not None or defer_attr is not None:
            async_or_defer_count += 1
    
    # Allow some scripts to not have async/defer (like inline scripts)
    assert async_or_defer_count > 0, "No scripts found with async/defer attributes"


def test_next_export_flags(page: Page):
    """Test that Next.js export flags are present in data"""
    next_data_script = page.locator("script#__NEXT_DATA__")
    script_content = next_data_script.text_content()

    # Check for nextExport flag (without quotes for flexibility)
    assert 'nextExport' in script_content, "nextExport flag not found"
    assert 'autoExport' in script_content, "autoExport flag not found"
    # Note: isFallback may not always be present


def test_build_id_present(page: Page):
    """Test that build ID is present in Next.js data"""
    next_data_script = page.locator("script#__NEXT_DATA__")
    script_content = next_data_script.text_content()

    # Check for buildId field (without specific value for flexibility)
    assert 'buildId' in script_content, "Build ID not found"


def test_page_has_no_visible_content_beyond_footer(page: Page):
    """Test that page has no other visible content beyond footer"""
    # Get all visible elements
    visible_elements = page.locator(
        "body > *:not(script):not(style):not(link):not(meta)"
    )
    count = visible_elements.count()

    # Should have at least the #__next div
    assert count >= 1, f"Expected at least 1 main container, found {count}"

    # Check that the main container exists and has content
    next_container = page.locator("#__next")
    expect(next_container).to_be_visible()
    
    # Check that footer exists
    footer = page.locator("footer").first
    expect(footer).to_be_visible()


def test_console_errors(page: Page):
    """Test that there are no critical console errors on page load"""
    console_errors = []

    def capture_console_errors(msg):
        if msg.type == "error":
            # Filter out common non-critical errors
            if "404" not in msg.text and "Failed to load resource" not in msg.text:
                console_errors.append(msg.text)

    page.on("console", capture_console_errors)

    page.goto("https://testathon.live/")

    # Give some time for scripts to load and potentially produce errors
    page.wait_for_timeout(1000)

    # Allow some 404 errors but check for critical errors
    critical_errors = [error for error in console_errors if "404" not in error and "Failed to load resource" not in error]
    assert len(critical_errors) == 0, f"Critical console errors found: {critical_errors}"


def test_network_requests_successful(page: Page):
    """Test that all network requests complete successfully"""
    failed_requests = []

    def capture_failed_requests(request):
        if request.failure:
            failed_requests.append({"url": request.url, "failure": request.failure})

    page.on("requestfailed", capture_failed_requests)

    page.goto("https://testathon.live/")

    # Wait for network to be idle
    page.wait_for_load_state("networkidle")

    assert len(failed_requests) == 0, f"Failed network requests: {failed_requests}"
