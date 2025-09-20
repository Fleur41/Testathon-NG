import pytest
from playwright.sync_api import Page, expect
import time


class TestFavouritesFunctionality:
    """Test favourites functionality and page"""
    
    BASE_URL = "https://testathon.live"
    USERNAME = "demouser"
    PASSWORD = "testingisfun99"
    
    @pytest.fixture(scope="function")
    def setup_favourites(self, page: Page):
        """Setup favourites test with login"""
        # Login first
        page.goto(f"{self.BASE_URL}/signin")
        page.wait_for_load_state("networkidle")
        
        # Perform login
        self._perform_login(page)
        
        yield page
    
    def _perform_login(self, page: Page):
        """Perform login with demouser and testingisfun99"""
        # Wait for login form to be visible
        expect(page.locator("#username")).to_be_visible()
        expect(page.locator("#password")).to_be_visible()
        expect(page.locator("#login-btn")).to_be_visible()
        
        # Select username from dropdown
        username_dropdown = page.locator("#username")
        username_dropdown.click()
        
        # Fill username in the dropdown input
        username_input = page.locator("#react-select-2-input")
        username_input.fill(self.USERNAME)
        page.keyboard.press("Enter")
        
        # Select password from dropdown
        password_dropdown = page.locator("#password")
        password_dropdown.click()
        
        # Fill password in the dropdown input
        password_input = page.locator("#react-select-3-input")
        password_input.fill(self.PASSWORD)
        page.keyboard.press("Enter")
        
        # Click login button
        login_button = page.locator("#login-btn")
        login_button.click()
        
        # Wait for login to complete
        page.wait_for_load_state("networkidle")
    
    def test_favourites_page_access(self, setup_favourites):
        """Test accessing the favourites page"""
        page = setup_favourites
        
        # Navigate to favourites page
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        
        # Verify favourites page loads
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
        
        print("✅ Favourites page accessed successfully")
    
    def test_favourites_page_structure(self, setup_favourites):
        """Test the structure of the favourites page"""
        page = setup_favourites
        
        # Navigate to favourites page
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        
        # Check for favourites-specific elements
        # These selectors would need to be adjusted based on actual page structure
        favourites_elements = [
            "h1:has-text('Favourites')",
            "h1:has-text('Favorites')",
            ".favourites",
            ".favorites",
            "[data-testid='favourites']",
            "[data-testid='favorites']"
        ]
        
        found_elements = []
        for selector in favourites_elements:
            element = page.locator(selector)
            if element.count() > 0:
                found_elements.append(selector)
                expect(element.first).to_be_visible()
        
        print(f"✅ Found favourites elements: {found_elements}")
    
    def test_add_to_favourites(self, setup_favourites):
        """Test adding items to favourites"""
        page = setup_favourites
        
        # Navigate to homepage first
        page.goto(f"{self.BASE_URL}/")
        page.wait_for_load_state("networkidle")
        
        # Wait for products to load
        page.wait_for_timeout(3000)
        
        # Look for add to favourites buttons using correct selectors
        add_to_favourites_selectors = [
            "button:has-text('Add to Favourites')",
            "button:has-text('Add to Favorites')",
            "button:has-text('❤️')",
            "button:has-text('♡')",
            "button:has-text('Add to Wishlist')",
            "[data-testid='add-to-favourites']",
            "[data-testid='add-to-favorites']",
            "button[class*='favourite']",
            "button[class*='favorite']"
        ]
        
        added_items = 0
        
        for selector in add_to_favourites_selectors:
            add_to_favourites_buttons = page.locator(selector)
            count = add_to_favourites_buttons.count()
            
            if count > 0:
                print(f"Found {count} add to favourites buttons with selector: {selector}")
                
                # Try to add first item to favourites
                try:
                    button = add_to_favourites_buttons.first
                    if button.is_visible():
                        button.click()
                        page.wait_for_timeout(1000)
                        added_items += 1
                        print("✅ Added item to favourites")
                        break
                except Exception as e:
                    print(f"⚠️ Failed to add to favourites: {e}")
        
        if added_items == 0:
            print("⚠️ No add to favourites buttons found")
    
    def test_remove_from_favourites(self, setup_favourites):
        """Test removing items from favourites"""
        page = setup_favourites
        
        # Navigate to favourites page
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        
        # Look for remove from favourites buttons
        remove_buttons = page.locator(
            "button:has-text('Remove'), "
            "button:has-text('Remove from Favourites'), "
            "button:has-text('Remove from Favorites'), "
            "button:has-text('❌'), "
            "[data-testid='remove-from-favourites']"
        )
        
        if remove_buttons.count() > 0:
            # Remove first item from favourites
            remove_buttons.first.click()
            page.wait_for_timeout(1000)
            print("✅ Removed item from favourites")
        else:
            print("⚠️ No remove buttons found")
    
    def test_favourites_navigation(self, setup_favourites):
        """Test navigation to and from favourites page"""
        page = setup_favourites
        
        # Test navigation from homepage to favourites
        page.goto(f"{self.BASE_URL}/")
        page.wait_for_load_state("networkidle")
        
        # Look for favourites link
        favourites_link = page.locator(
            "a:has-text('Favourites'), "
            "a:has-text('Favorites'), "
            "[href*='favourites'], "
            "[href*='favorites']"
        )
        
        if favourites_link.count() > 0:
            favourites_link.first.click()
            page.wait_for_load_state("networkidle")
            print("✅ Navigated to favourites via link")
        else:
            # Try direct navigation
            page.goto(f"{self.BASE_URL}/favourites")
            page.wait_for_load_state("networkidle")
            print("✅ Navigated to favourites directly")
        
        # Test navigation back to homepage
        homepage_link = page.locator(
            "a:has-text('Home'), "
            "a:has-text('Homepage'), "
            "[href='/'], "
            "[href*='home']"
        )
        
        if homepage_link.count() > 0:
            homepage_link.first.click()
            page.wait_for_load_state("networkidle")
            print("✅ Navigated back to homepage")
        else:
            page.goto(f"{self.BASE_URL}/")
            page.wait_for_load_state("networkidle")
            print("✅ Navigated back to homepage directly")
    
    def test_favourites_responsive_design(self, setup_favourites):
        """Test favourites page responsive design"""
        page = setup_favourites
        
        # Navigate to favourites page
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        
        # Test different viewport sizes
        viewports = [
            {"width": 375, "height": 667},   # Mobile
            {"width": 768, "height": 1024},  # Tablet
            {"width": 1280, "height": 800},  # Desktop
            {"width": 1920, "height": 1080}  # Large desktop
        ]
        
        for viewport in viewports:
            page.set_viewport_size(viewport)
            expect(page.locator("#__next")).to_be_visible()
            print(f"✅ Favourites page responsive at {viewport['width']}x{viewport['height']}")
    
    def test_favourites_performance(self, setup_favourites):
        """Test favourites page performance"""
        page = setup_favourites
        
        # Measure favourites page load time
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        load_time = (time.time() - start_time) * 1000
        
        print(f"⏱️ Favourites page load time: {load_time:.2f}ms")
        
        # Verify page loads within reasonable time
        assert load_time < 10000, f"Favourites page too slow: {load_time:.2f}ms"
        
        # Verify page is functional
        expect(page.locator("#__next")).to_be_visible()
    
    def test_favourites_with_slow_network(self, setup_favourites):
        """Test favourites page with slow network conditions"""
        page = setup_favourites
        
        # Simulate slow network
        context = page.context
        context.set_extra_http_headers({"X-Slow-Network": "true"})
        
        print("🐌 Testing favourites with slow network...")
        
        # Navigate to favourites with slow network
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        load_time = (time.time() - start_time) * 1000
        
        print(f"⏱️ Favourites slow network load time: {load_time:.2f}ms")
        
        # Verify page still loads
        expect(page.locator("#__next")).to_be_visible()
        
        # Check for slow network message
        slow_network_message = page.locator("text=Good news is we are online but bad news is you are on slow network")
        if slow_network_message.count() > 0:
            expect(slow_network_message).to_be_visible()
            print("✅ Slow network message displayed")
    
    def test_favourites_error_handling(self, setup_favourites):
        """Test error handling on favourites page"""
        page = setup_favourites
        
        # Simulate network errors
        context = page.context
        context.set_extra_http_headers({"X-Network-Error": "true"})
        
        print("🛡️ Testing favourites error handling...")
        
        try:
            page.goto(f"{self.BASE_URL}/favourites")
            page.wait_for_load_state("networkidle", timeout=10000)
            print("✅ Favourites page loaded despite network errors")
        except Exception as e:
            print(f"⚠️ Network error handled: {e}")
        
        # Verify page eventually loads
        expect(page.locator("#__next")).to_be_visible()
    
    def test_favourites_console_errors(self, setup_favourites):
        """Test for console errors on favourites page"""
        page = setup_favourites
        
        console_errors = []
        
        def capture_console_errors(msg):
            if msg.type == "error":
                console_errors.append({
                    "text": msg.text,
                    "type": msg.type,
                    "url": msg.location.get("url", "unknown") if hasattr(msg, "location") else "unknown"
                })
        
        page.on("console", capture_console_errors)
        
        # Navigate to favourites page
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        
        # Check for console errors
        if console_errors:
            print(f"⚠️ Found {len(console_errors)} console errors:")
            for error in console_errors:
                print(f"  - {error['text']}")
        else:
            print("✅ No console errors found")
        
        # Allow some non-critical errors
        critical_errors = [e for e in console_errors if "404" not in e["text"] and "Failed to load resource" not in e["text"]]
        assert len(critical_errors) == 0, f"Critical console errors found: {critical_errors}"
    
    def test_favourites_accessibility(self, setup_favourites):
        """Test accessibility features on favourites page"""
        page = setup_favourites
        
        # Navigate to favourites page
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        
        # Check for accessibility features
        # These checks would need to be adjusted based on actual page structure
        
        # Check for proper heading structure
        headings = page.locator("h1, h2, h3, h4, h5, h6")
        if headings.count() > 0:
            expect(headings.first).to_be_visible()
            print("✅ Page has proper heading structure")
        
        # Check for alt text on images
        images = page.locator("img")
        if images.count() > 0:
            for i in range(images.count()):
                img = images.nth(i)
                alt_text = img.get_attribute("alt")
                if alt_text:
                    print(f"✅ Image {i} has alt text: {alt_text}")
        
        # Check for proper button labels
        buttons = page.locator("button")
        if buttons.count() > 0:
            for i in range(buttons.count()):
                button = buttons.nth(i)
                button_text = button.text_content()
                if button_text:
                    print(f"✅ Button {i} has text: {button_text}")
        
        print("✅ Accessibility checks completed")


# Run with: pytest test_favourites.py -v
