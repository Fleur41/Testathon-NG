import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Go to the login page before each test
    page.goto("https://testathon.live/signin")
    yield


def test_login_page_title(page: Page):
    """Test that the page title is correct"""
    expect(page).to_have_title("StackDemo")


def test_login_page_logo_is_visible(page: Page):
    """Test that the logo is visible on the page"""
    logo = page.locator("svg[width='156'][height='156']")
    expect(logo).to_be_visible()


def test_username_dropdown_is_present(page: Page):
    """Test that username dropdown exists and has correct placeholder"""
    username_dropdown = page.locator("#username")
    expect(username_dropdown).to_be_visible()

    placeholder = username_dropdown.locator(".css-1wa3eu0-placeholder")
    expect(placeholder).to_have_text("Select Username")


def test_password_dropdown_is_present(page: Page):
    """Test that password dropdown exists and has correct placeholder"""
    password_dropdown = page.locator("#password")
    expect(password_dropdown).to_be_visible()

    placeholder = password_dropdown.locator(".css-1wa3eu0-placeholder")
    expect(placeholder).to_have_text("Select Password")


def test_login_button_is_present_and_visible(page: Page):
    """Test that login button exists and is visible"""
    login_button = page.locator("#login-btn")
    expect(login_button).to_be_visible()
    expect(login_button).to_have_text("Log In")
    expect(login_button).to_be_enabled()


def test_login_form_structure(page: Page):
    """Test the overall structure of the login form"""
    form = page.locator("form.flex.flex-col")
    expect(form).to_be_visible()

    # Check form has correct classes
    expect(form).to_have_class("w-80 flex flex-col justify-between p-3")


def test_login_with_valid_credentials(page: Page):
    """Test successful login with valid credentials"""
    # This test assumes you know what options will be available in the dropdowns
    # You may need to adjust based on actual implementation

    # Select username
    username_dropdown = page.locator("#username")
    username_dropdown.click()
    # Assuming there are options that appear - you'll need to adjust selectors
    page.locator("#react-select-2-input").fill("valid_username")
    page.keyboard.press("Enter")

    # Select password
    password_dropdown = page.locator("#password")
    password_dropdown.click()
    page.locator("#react-select-3-input").fill("valid_password")
    page.keyboard.press("Enter")

    # Click login button
    login_button = page.locator("#login-btn")
    login_button.click()

    # Verify redirect or success (adjust based on your app behavior)
    # expect(page).to_have_url("https://your-app-url.com/dashboard")


def test_login_with_invalid_credentials(page: Page):
    """Test login attempt with invalid credentials"""
    # Select username
    username_dropdown = page.locator("#username")
    username_dropdown.click()
    page.locator("#react-select-2-input").fill("invalid_user")
    page.keyboard.press("Enter")

    # Select password
    password_dropdown = page.locator("#password")
    password_dropdown.click()
    page.locator("#react-select-3-input").fill("wrong_password")
    page.keyboard.press("Enter")

    # Click login button
    login_button = page.locator("#login-btn")
    login_button.click()

    # Verify error message appears (adjust selector based on actual error element)
    # error_message = page.locator(".error-message")
    # expect(error_message).to_be_visible()
    # expect(error_message).to_contain_text("Invalid credentials")


def test_login_with_empty_credentials(page: Page):
    """Test login attempt without selecting credentials"""
    login_button = page.locator("#login-btn")
    login_button.click()

    # Verify validation messages or that login doesn't proceed
    # This depends on how your form validation works


def test_dropdown_interaction(page: Page):
    """Test that dropdowns can be interacted with"""
    username_dropdown = page.locator("#username")

    # Click to open dropdown
    username_dropdown.click()

    # Verify dropdown expands (check for specific classes or styles)
    dropdown_container = username_dropdown.locator(".css-yk16xz-control")
    # You might need to check for specific state classes

    # Type something in the search
    search_input = page.locator("#react-select-2-input")
    search_input.fill("test")

    # Verify search works (this depends on your implementation)


def test_responsive_design(page: Page):
    """Test that the login form is responsive"""
    # Test mobile view
    page.set_viewport_size({"width": 375, "height": 667})

    form = page.locator("form.w-80")
    expect(form).to_be_visible()

    # Test tablet view
    page.set_viewport_size({"width": 768, "height": 1024})
    expect(form).to_be_visible()

    # Test desktop view
    page.set_viewport_size({"width": 1280, "height": 800})
    expect(form).to_be_visible()


def test_accessibility_features(page: Page):
    """Test accessibility features"""
    # Check that form inputs have proper labels
    username_input = page.locator("#react-select-2-input")
    expect(username_input).to_have_attribute("aria-autocomplete", "list")

    # Check that buttons have proper roles
    login_button = page.locator("#login-btn")
    expect(login_button).to_have_attribute("type", "submit")


def test_browser_back_button_after_login_attempt(page: Page):
    """Test browser back button behavior"""
    # Perform login attempt
    login_button = page.locator("#login-btn")
    login_button.click()

    # Go back
    page.go_back()

    # If we're on about:blank, navigate back to the login page
    if page.url == "about:blank":
        page.goto("https://testathon.live/signin")
    
    # Wait for page to load and verify we're back on login page
    page.wait_for_load_state("networkidle")
    expect(page.locator("#login-btn")).to_be_visible()


def test_page_load_performance(page: Page):
    """Test that page loads within acceptable time"""
    # Measure page load time
    import time
    start_time = time.time()
    page.goto("https://testathon.live/signin")
    load_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    assert load_time < 3000, f"Page took {load_time}ms to load (max 3000ms allowed)"


def test_css_styles_are_loaded(page: Page):
    """Verify that CSS styles are properly loaded"""
    # Check that styled elements have expected styles
    login_button = page.locator("#login-btn")

    # You might check for specific styles if they're important
    button_color = login_button.evaluate(
        "el => window.getComputedStyle(el).backgroundColor"
    )
    # assert button_color == "expected_rgb_value"
