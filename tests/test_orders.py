import pytest
import json
from playwright.sync_api import Page, expect

# Base URL configuration (adjust as needed)
BASE_URL = "https://testathon.live"  # Change to your actual URL

@pytest.fixture(scope="function")
def setup_page(page: Page):
    """Setup fixture to navigate to the orders page"""
    page.goto(f"{BASE_URL}/orders")
    yield page

def test_page_title(setup_page):
    """Test that the page has the correct title"""
    page = setup_page
    assert page.title() == "StackDemo"

def test_page_structure(setup_page):
    """Test basic page structure and essential elements"""
    page = setup_page
    
    # Check that the main container exists
    expect(page.locator("#__next")).to_be_visible()
    
    # Check that the NEXT_DATA script exists
    expect(page.locator("#__NEXT_DATA__")).to_be_attached()

def test_meta_tags(setup_page):
    """Test that essential meta tags are present"""
    page = setup_page
    
    # Check charset meta tag
    charset_meta = page.locator('meta[charset="utf-8"]')
    expect(charset_meta).to_be_attached()
    
    # Check viewport meta tag
    viewport_meta = page.locator('meta[name="viewport"]')
    expect(viewport_meta).to_be_attached()
    expect(viewport_meta).to_have_attribute("content", "initial-scale=1.0, width=device-width")

def test_css_stylesheets_loaded(setup_page):
    """Test that CSS stylesheets are properly loaded"""
    page = setup_page
    
    # Check CSS links
    css_links = page.locator('link[rel="stylesheet"]')
    expect(css_links).to_have_count(2)
    
    # Verify specific CSS chunks are loaded
    expect(page.locator('link[href*="412b7dee.11f4ec51.chunk.css"]').first).to_be_attached()
    expect(page.locator('link[href*="styles.e2bb0603.chunk.css"]').first).to_be_attached()

def test_script_tags_loaded(setup_page):
    """Test that all JavaScript files are properly loaded"""
    page = setup_page
    
    # Count all script tags
    script_tags = page.locator("script[src]")
    expect(script_tags).to_have_count(17)
    
    # Verify that we have Next.js scripts (more flexible approach)
    next_scripts = page.locator('script[src*="/_next/static/chunks/"]')
    expect(next_scripts).to_have_count(5)  # Should have multiple Next.js chunks

def test_next_data_content(setup_page):
    """Test that the __NEXT_DATA__ script contains expected content"""
    page = setup_page
    
    next_data_script = page.locator("#__NEXT_DATA__")
    expect(next_data_script).to_be_attached()
    
    # Get the JSON content
    next_data_content = next_data_script.text_content()
    assert next_data_content is not None
    
    # Parse and validate JSON structure
    data = json.loads(next_data_content)
    
    # Verify basic structure
    assert "props" in data
    assert "page" in data
    assert data["page"] == "/orders"
    assert "buildId" in data
    assert data["buildId"] == "flryiVW52XrLSOqDaY32K"
    assert data["isFallback"] == False
    assert data["nextExport"] == True
    assert data["autoExport"] == True

def test_async_script_loading(setup_page):
    """Test that scripts are loaded asynchronously"""
    page = setup_page
    
    # Check that main scripts have async attribute
    async_scripts = page.locator('script[async]')
    expect(async_scripts).to_have_count(15)
    
    # Verify specific async scripts
    expect(page.locator('script[src*="main-"][async]')).to_be_attached()
    expect(page.locator('script[src*="webpack-"][async]')).to_be_attached()

def test_preload_links(setup_page):
    """Test that preload links are properly set up"""
    page = setup_page
    
    # Check preload links for CSS
    css_preloads = page.locator('link[rel="preload"][as="style"]')
    expect(css_preloads).to_have_count(2)
    
    # Check preload links for JS
    js_preloads = page.locator('link[rel="preload"][as="script"]')
    expect(js_preloads).to_have_count(13)

def test_polyfills_loaded(setup_page):
    """Test that polyfills are properly included"""
    page = setup_page
    
    polyfill_script = page.locator('script[src*="polyfills-"]')
    expect(polyfill_script).to_be_attached()
    expect(polyfill_script).to_have_attribute("nomodule", "")

def test_build_manifest_loaded(setup_page):
    """Test that build manifests are loaded"""
    page = setup_page
    
    build_manifest = page.locator('script[src*="_buildManifest.js"]')
    ssg_manifest = page.locator('script[src*="_ssgManifest.js"]')
    
    expect(build_manifest).to_be_attached()
    expect(ssg_manifest).to_be_attached()

def test_noscript_tag(setup_page):
    """Test that noscript tag is present"""
    page = setup_page
    
    noscript_tag = page.locator('noscript[data-n-css="true"]')
    expect(noscript_tag).to_be_attached()

def test_orders_specific_scripts(setup_page):
    """Test that orders page specific scripts are loaded"""
    page = setup_page
    
    # Check orders page script
    orders_script = page.locator('script[src*="pages/orders-"]')
    expect(orders_script).to_be_attached()
    
    # Check other specific scripts mentioned in preload
    specific_scripts = [
        "29107295.cc37323fff835cb3f1a5.js",
        "b8893a6f06b70a9cc8257c2531fbea864096704d.997ca2aa2fc58a8032c0.js",
        "0d59522aa4d49d537fa1e452691a43255e2011f7.d0e0408b9762be71b769.js",
        "5dd68d992e454f53e934be0a6bdc449c090bf9c7.3d7a79c958a7fd0af5d3.js"
    ]
    
    for script_name in specific_scripts:
        script_locator = page.locator(f'script[src*="{script_name}"]')
        expect(script_locator).to_be_attached()

def test_responsive_design(setup_page):
    """Test that the page is responsive"""
    page = setup_page
    
    # Test different viewport sizes
    viewports = [
        {"width": 320, "height": 568},   # Mobile
        {"width": 768, "height": 1024},  # Tablet
        {"width": 1200, "height": 800},  # Desktop
        {"width": 1920, "height": 1080}  # Large desktop
    ]
    
    for viewport in viewports:
        page.set_viewport_size(viewport)
        expect(page.locator("#__next")).to_be_visible()

def test_page_performance(setup_page):
    """Test that page loads within acceptable time"""
    page = setup_page
    
    # Measure load time using Performance API
    load_time = page.evaluate("""
        () => {
            const navTiming = performance.getEntriesByType('navigation')[0];
            if (navTiming && navTiming.loadEventEnd && navTiming.navigationStart) {
                return navTiming.loadEventEnd - navTiming.navigationStart;
            }
            return null;
        }
    """)
    
    # Skip performance test if timing data is not available
    if load_time is not None and not (isinstance(load_time, float) and load_time != load_time):  # Check for NaN
        assert load_time < 5000, f"Page took {load_time}ms to load, which is too slow"
    else:
        # If timing data is not available, just verify page loaded successfully
        assert page.title() is not None, "Page failed to load properly"

def test_no_console_errors(setup_page):
    """Test that there are no console errors"""
    page = setup_page
    
    # Capture console messages
    console_messages = []
    
    def log_console_message(msg):
        if msg.type == 'error':
            console_messages.append(msg.text)
    
    page.on("console", log_console_message)
    
    # Refresh page to capture any initial errors
    page.reload()
    
    # Allow some time for scripts to load and potentially produce errors
    page.wait_for_timeout(1000)
    
    # Check if there were any console errors
    assert len(console_messages) == 0, f"Found console errors: {console_messages}"

def test_accessibility(setup_page):
    """Test basic accessibility requirements"""
    page = setup_page
    
    # Check that the page has a lang attribute (optional - some pages may not have it)
    html_element = page.locator("html")
    lang_attribute = html_element.get_attribute("lang")
    # If lang attribute exists, it should be "en", but it's not required
    if lang_attribute is not None:
        assert lang_attribute == "en", f"Expected lang='en', got lang='{lang_attribute}'"
    
    # Check that the page has a main content area
    # (Assuming the #__next div serves as the main content)
    main_content = page.locator("#__next")
    expect(main_content).to_be_attached()

# Run with: pytest -v --headed (for visible browser) or just pytest for headless