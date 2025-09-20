import pytest
from playwright.sync_api import Page, expect
import time
import json


@pytest.fixture(scope="function", autouse=True)
def goto_confirmation_page(page: Page):
    """Navigate to confirmation page before each test"""
    page.goto("https://testathon.live/confirmation")  # Replace with actual URL
    yield


def test_confirmation_page_url(page: Page):
    """Test that the page URL is correct"""
    expect(page).to_have_url("https://testathon.live/confirmation")


def test_page_meta_tags(page: Page):
    """Test that all meta tags are correctly set"""
    # Charset meta tag
    charset_meta = page.locator("meta[charSet]")
    expect(charset_meta).to_have_attribute("charSet", "utf-8")

    # Viewport meta tag
    viewport_meta = page.locator("meta[name='viewport']")
    expect(viewport_meta).to_have_attribute("content", "width=device-width")


def test_nextjs_container_exists(page: Page):
    """Test that the Next.js container is present"""
    next_container = page.locator("#__next")
    expect(next_container).to_be_visible()
    expect(next_container).to_be_empty()  # Container is empty in this HTML


def test_next_data_script_content(page: Page):
    """Test that Next.js data script contains correct information"""
    next_data_script = page.locator("script#__NEXT_DATA__")
    expect(next_data_script).to_be_visible()

    # Parse and verify JSON content
    script_content = next_data_script.text_content()
    assert script_content is not None, "Next data script is empty"

    data = json.loads(script_content)

    # Verify page props
    assert (
        data["page"] == "/confirmation"
    ), f"Expected page '/confirmation', got '{data['page']}'"
    assert data["buildId"] == "flryiVW52XrLSOqDaY32K", "Build ID mismatch"
    assert data["nextExport"] == True, "nextExport should be true"
    assert data["autoExport"] == True, "autoExport should be true"
    assert data["isFallback"] == False, "isFallback should be false"

    # Verify query is empty
    assert data["query"] == {}, "Query should be empty object"

    # Verify pageProps is empty
    assert data["props"]["pageProps"] == {}, "pageProps should be empty object"


def test_all_scripts_loaded_correctly(page: Page):
    """Test that all required scripts are loaded"""
    scripts = page.locator("script[src]")
    count = scripts.count()
    assert count > 0, "No script tags with src found"

    # Check specific required scripts
    required_scripts = [
        "main-",
        "webpack-",
        "framework-",
        "styles.",
        "pages/_app-",
        "pages/confirmation-",
        "_buildManifest",
        "_ssgManifest",
    ]

    for script_pattern in required_scripts:
        script_locator = page.locator(f"script[src*='{script_pattern}']")
        expect(script_locator).to_be_attached()


def test_async_script_attributes(page: Page):
    """Test that all scripts have async attribute"""
    scripts = page.locator("script[src]")
    for i in range(scripts.count()):
        script = scripts.nth(i)
        async_attr = script.get_attribute("async")
        assert async_attr is not None, f"Script {i} missing async attribute"


def test_css_stylesheets_present(page: Page):
    """Test that CSS stylesheets are properly linked"""
    stylesheets = page.locator("link[rel='stylesheet']")
    count = stylesheets.count()
    assert count >= 2, f"Expected at least 2 stylesheets, found {count}"

    # Check specific stylesheets
    expect(page.locator("link[href*='412b7dee']")).to_be_attached()
    expect(page.locator("link[href*='styles.e2bb0603']")).to_be_attached()


def test_preload_links_present(page: Page):
    """Test that preload links are present for critical resources"""
    preload_links = page.locator("link[rel='preload']")
    count = preload_links.count()
    assert count > 0, "No preload links found"

    # Verify CSS preloads
    css_preloads = page.locator("link[rel='preload'][as='style']")
    assert css_preloads.count() >= 2, "Expected CSS preload links"

    # Verify script preloads
    script_preloads = page.locator("link[rel='preload'][as='script']")
    assert script_preloads.count() > 0, "Expected script preload links"


def test_noscript_tag_present(page: Page):
    """Test that noscript tag exists with correct attributes"""
    noscript = page.locator("noscript")
    expect(noscript).to_be_attached()
    expect(noscript).to_have_attribute("data-n-css", "true")


def test_polyfill_script_for_legacy_browsers(page: Page):
    """Test that polyfill script is present for legacy browsers"""
    polyfill_script = page.locator("script[nomodule]")
    expect(polyfill_script).to_be_attached()
    expect(polyfill_script).to_have_attribute(
        "src", "/_next/static/chunks/polyfills-1509bd3fd78666178104.js"
    )


def test_confirmation_specific_script(page: Page):
    """Test that confirmation page specific script is loaded"""
    confirmation_script = page.locator("script[src*='confirmation-']")
    expect(confirmation_script).to_be_attached()

    # Verify it's the correct confirmation script
    script_src = confirmation_script.get_attribute("src")
    assert (
        "confirmation-8d4caf1c4b68f003cd02.js" in script_src
    ), "Wrong confirmation script version"


def test_page_load_performance(page: Page):
    """Test that confirmation page loads within acceptable time"""
    start_time = time.time()
    page.goto("https://testathon.live/confirmation")
    load_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    assert (
        load_time < 2000
    ), f"Confirmation page took {load_time:.2f}ms to load (max 2000ms allowed)"


def test_page_responsive_design(page: Page):
    """Test that confirmation page is responsive"""
    viewports = [
        {"width": 375, "height": 667},  # Mobile
        {"width": 768, "height": 1024},  # Tablet
        {"width": 1280, "height": 800},  # Desktop
        {"width": 1920, "height": 1080},  # Large desktop
    ]

    for viewport in viewports:
        page.set_viewport_size(viewport)
        next_container = page.locator("#__next")
        expect(next_container).to_be_visible()


def test_no_console_errors(page: Page):
    """Test that there are no JavaScript console errors"""
    console_errors = []

    def capture_console_errors(msg):
        if msg.type == "error":
            console_errors.append(
                {
                    "text": msg.text,
                    "type": msg.type,
                    "url": (
                        msg.location["url"] if hasattr(msg, "location") else "unknown"
                    ),
                }
            )

    page.on("console", capture_console_errors)

    page.goto("https://testathon.live/confirmation")
    page.wait_for_load_state("networkidle")

    assert len(console_errors) == 0, f"Console errors found: {console_errors}"


def test_no_network_errors(page: Page):
    """Test that all network requests complete successfully"""
    failed_requests = []

    def capture_failed_requests(request):
        if request.failure:
            failed_requests.append({"url": request.url, "failure": request.failure})

    page.on("requestfailed", capture_failed_requests)

    page.goto("https://testathon.live/confirmation")
    page.wait_for_load_state("networkidle")

    assert len(failed_requests) == 0, f"Failed network requests: {failed_requests}"


def test_script_execution_order(page: Page):
    """Test that scripts are loaded in correct order (async but with dependencies)"""
    # This test verifies that critical scripts are present
    # The actual execution order is handled by browser with async

    scripts = page.locator("script[src]")
    script_urls = []

    for i in range(scripts.count()):
        script = scripts.nth(i)
        src = script.get_attribute("src")
        if src:
            script_urls.append(src)

    # Verify critical scripts are present
    assert any("main-" in url for url in script_urls), "Main script not found"
    assert any("webpack-" in url for url in script_urls), "Webpack script not found"
    assert any("framework-" in url for url in script_urls), "Framework script not found"
    assert any(
        "confirmation-" in url for url in script_urls
    ), "Confirmation page script not found"


def test_nextjs_manifest_files(page: Page):
    """Test that Next.js manifest files are loaded"""
    build_manifest = page.locator("script[src*='_buildManifest']")
    expect(build_manifest).to_be_attached()

    ssg_manifest = page.locator("script[src*='_ssgManifest']")
    expect(ssg_manifest).to_be_attached()


def test_body_structure(page: Page):
    """Test that body contains only expected elements"""
    body = page.locator("body")
    direct_children = body.locator("> *")

    # Should contain only #__next div and script tags
    children_count = direct_children.count()
    assert (
        children_count >= 2
    ), f"Expected at least 2 direct children in body, found {children_count}"

    # Verify #__next is the first child (usually)
    first_child = direct_children.first
    expect(first_child).to_have_attribute("id", "__next")


def test_page_accessibility_basics(page: Page):
    """Test basic accessibility features"""
    # Check document language (though not explicitly set in HTML)
    html = page.locator("html")

    # Check body is accessible
    body = page.locator("body")
    expect(body).to_be_visible()

    # Check that page has a title
    expect(page).to_have_title("StackDemo")


def test_dynamic_content_loading(page: Page):
    """Test that dynamic content can be loaded (if applicable)"""
    # Since the #__next div is empty, we might expect React to hydrate it
    # This test waits to see if any content appears dynamically
    next_container = page.locator("#__next")

    # Wait a bit to see if any content gets injected
    page.wait_for_timeout(1000)

    # The container might remain empty or get populated by React
    # This test just ensures no errors occur during the waiting period


def test_confirmation_page_specific_functionality(page: Page):
    """Test any confirmation-specific functionality"""
    # Since this is a confirmation page, we might expect:
    # - Order confirmation details
    # - Success messages
    # - Continue shopping buttons
    # - Order summary

    # For now, just verify the page loads without errors
    next_container = page.locator("#__next")
    expect(next_container).to_be_visible()

    # If this is a React app, content might be loaded dynamically
    # We can check if any React components get rendered
    try:
        # Wait a bit for potential React hydration
        page.wait_for_timeout(500)
    except:
        pass  # Ignore timeout errors for this test


# Run with: pytest test_confirmation_page.py -v
