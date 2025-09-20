import pytest
from playwright.sync_api import Page, expect

# Base URL configuration (adjust as needed)
BASE_URL = "https://testathon.live"  # Change to your actual URL

@pytest.fixture(scope="function")
def setup_page(page: Page):
    """Setup fixture to navigate to the checkout page"""
    page.goto(f"{BASE_URL}/checkout")
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
    expect(css_links).to_have_count(2)  # Adjust count based on actual CSS files
    
    # Verify specific CSS chunks are loaded
    expect(page.locator('link[href*="412b7dee.11f4ec51.chunk.css"]').first).to_be_attached()
    expect(page.locator('link[href*="styles.e2bb0603.chunk.css"]').first).to_be_attached()

def test_script_tags_loaded(setup_page):
    """Test that all JavaScript files are properly loaded"""
    page = setup_page
    
    # Count all script tags (including polyfills and async scripts)
    script_tags = page.locator("script[src]")
    expect(script_tags).to_have_count(14)  # Should have multiple scripts
    
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
    
    # Basic validation of JSON structure
    import json
    data = json.loads(next_data_content)
    
    # Verify basic structure
    assert "props" in data
    assert "page" in data
    assert data["page"] == "/checkout"
    assert "buildId" in data
    assert data["buildId"] == "flryiVW52XrLSOqDaY32K"
    assert data["isFallback"] == False

def test_async_script_loading(setup_page):
    """Test that scripts are loaded asynchronously"""
    page = setup_page
    
    # Check that main scripts have async attribute
    async_scripts = page.locator('script[async]')
    expect(async_scripts).to_have_count(12)
    
    # Verify specific async scripts
    expect(page.locator('script[src*="main-"][async]')).to_be_attached()
    expect(page.locator('script[src*="webpack-"][async]')).to_be_attached()

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

def test_preload_links(setup_page):
    """Test that preload links are properly set up"""
    page = setup_page
    
    # Check preload links for CSS
    css_preloads = page.locator('link[rel="preload"][as="style"]')
    expect(css_preloads).to_have_count(2)
    
    # Check preload links for JS
    js_preloads = page.locator('link[rel="preload"][as="script"]')
    expect(js_preloads).to_have_count(10)

def test_noscript_tag(setup_page):
    """Test that noscript tag is present"""
    page = setup_page
    
    noscript_tag = page.locator('noscript[data-n-css="true"]')
    expect(noscript_tag).to_be_attached()

def test_page_is_exported(setup_page):
    """Test that the page is marked as exported"""
    page = setup_page
    
    next_data_script = page.locator("#__NEXT_DATA__")
    next_data_content = next_data_script.text_content()
    
    import json
    data = json.loads(next_data_content)
    
    assert data["nextExport"] == True
    assert data["autoExport"] == True

def test_responsive_design(setup_page):
    """Test that the page is responsive"""
    page = setup_page
    
    # Test different viewport sizes
    page.set_viewport_size({"width": 320, "height": 568})  # Mobile
    expect(page.locator("#__next")).to_be_visible()
    
    page.set_viewport_size({"width": 768, "height": 1024})  # Tablet
    expect(page.locator("#__next")).to_be_visible()
    
    page.set_viewport_size({"width": 1200, "height": 800})  # Desktop
    expect(page.locator("#__next")).to_be_visible()

def test_page_performance(setup_page):
    """Test that page loads within acceptable time"""
    page = setup_page
    
    # Measure load time (this is a simple example)
    load_time = page.evaluate("() => window.performance.timing.loadEventEnd - window.performance.timing.navigationStart")
    
    # Adjust threshold based on your requirements
    assert load_time < 5000, f"Page took {load_time}ms to load, which is too slow"

# Run with: pytest -v --headed (for visible browser) or just pytest for headless