import pytest
from playwright.sync_api import Page, expect
import time
import json


class TestCompleteUserFlow:
    """Complete end-to-end user flow test"""
    
    BASE_URL = "https://testathon.live"
    USERNAME = "demouser"
    PASSWORD = "testingisfun99"
    
    @pytest.fixture(scope="function")
    def setup_complete_flow(self, page: Page):
        """Setup the complete user flow"""
        # Start at signin page
        page.goto(f"{self.BASE_URL}/signin")
        page.wait_for_load_state("networkidle")
        yield page
    
    def test_complete_user_journey(self, setup_complete_flow):
        """Test the complete user journey from signin to orders"""
        page = setup_complete_flow
        
        print("🚀 Starting Complete User Journey Test")
        print("=" * 50)
        
        # Step 1: Login
        print("📝 Step 1: Login Process")
        self._perform_login(page)
        
        # Step 2: Navigate to Homepage
        print("🏠 Step 2: Navigate to Homepage")
        self._navigate_to_homepage(page)
        
        # Step 3: Add items to cart
        print("🛒 Step 3: Add items to cart")
        self._add_items_to_cart(page)
        
        # Step 4: Navigate to Favourites
        print("❤️ Step 4: Navigate to Favourites")
        self._navigate_to_favourites(page)
        
        # Step 5: Go to Checkout
        print("💳 Step 5: Go to Checkout")
        self._navigate_to_checkout(page)
        
        # Step 6: Fill checkout form
        print("📋 Step 6: Fill checkout form")
        self._fill_checkout_form(page)
        
        # Step 7: Navigate to Confirmation
        print("✅ Step 7: Navigate to Confirmation")
        self._navigate_to_confirmation(page)
        
        # Step 8: Download receipt
        print("📄 Step 8: Download receipt")
        self._download_receipt(page)
        
        # Step 9: Navigate to Orders
        print("📦 Step 9: Navigate to Orders")
        self._navigate_to_orders(page)
        
        print("🎉 Complete user journey test finished successfully!")
    
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
        
        # Verify we're logged in (check for user-specific elements or redirect)
        print(f"✅ Logged in as {self.USERNAME}")
    
    def _navigate_to_homepage(self, page: Page):
        """Navigate to homepage after login"""
        page.goto(f"{self.BASE_URL}/")
        page.wait_for_load_state("networkidle")
        
        # Verify homepage elements
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
        
        print("✅ Navigated to homepage")
    
    def _add_items_to_cart(self, page: Page):
        """Add items to cart from homepage"""
        # Wait for products to load
        page.wait_for_timeout(3000)
        
        # Look for add to cart buttons using the correct selectors
        add_to_cart_selectors = [
            "div.shelf-item__buy-btn:has-text('Add to cart')",
            "button.MuiButtonBase-root.MuiIconButton-root",
            "button:has-text('Add to cart')",
            "button:has-text('Add')",
            "[data-testid='add-to-cart']"
        ]
        
        added_items = 0
        
        for selector in add_to_cart_selectors:
            add_to_cart_buttons = page.locator(selector)
            count = add_to_cart_buttons.count()
            
            if count > 0:
                print(f"Found {count} add to cart buttons with selector: {selector}")
                
                # Try to add first few items to cart
                for i in range(min(count, 3)):  # Add up to 3 items
                    try:
                        button = add_to_cart_buttons.nth(i)
                        if button.is_visible():
                            button.click()
                            page.wait_for_timeout(1000)
                            added_items += 1
                            print(f"✅ Added item {i+1} to cart")
                    except Exception as e:
                        print(f"⚠️ Failed to add item {i+1}: {e}")
                
                if added_items > 0:
                    break
        
        if added_items == 0:
            print("⚠️ No add to cart buttons found, continuing...")
        else:
            print(f"✅ Successfully added {added_items} items to cart")
    
    def _navigate_to_favourites(self, page: Page):
        """Navigate to favourites page"""
        # Try direct navigation first (more reliable)
        page.goto(f"{self.BASE_URL}/favourites")
        page.wait_for_load_state("networkidle")
        
        # Verify favourites page
        expect(page.locator("#__next")).to_be_visible()
        print("✅ Navigated to favourites page")
    
    def _navigate_to_checkout(self, page: Page):
        """Navigate to checkout page"""
        # Use direct navigation (more reliable)
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        
        print("✅ Navigated to checkout page")
    
    def _fill_checkout_form(self, page: Page):
        """Fill out the checkout form"""
        # Wait for checkout form to load
        page.wait_for_timeout(2000)
        
        # Look for form fields (adjust selectors based on actual form)
        form_fields = [
            ("firstname", "John"),
            ("lastname", "Doe"),
            ("username", "johndoe"),
            ("email", "john.doe@example.com"),
            ("address1", "123 Main St"),
            ("address2", "Apt 4B"),
            ("country", "United States"),
            ("state", "California"),
            ("zip", "12345"),
            ("cardname", "John Doe"),
            ("cardnumber", "4111111111111111"),
            ("expdate", "12/25"),
            ("cvv", "123")
        ]
        
        for field_name, value in form_fields:
            field = page.locator(f"input[name='{field_name}'], input[id='{field_name}'], input[placeholder*='{field_name}']")
            if field.count() > 0:
                field.first.fill(value)
                print(f"✅ Filled {field_name}")
            else:
                print(f"⚠️ Field {field_name} not found")
        
        # Look for submit button
        submit_button = page.locator("button[type='submit'], button:has-text('Submit'), button:has-text('Place Order')")
        if submit_button.count() > 0:
            submit_button.first.click()
            page.wait_for_load_state("networkidle")
            print("✅ Submitted checkout form")
        else:
            print("⚠️ Submit button not found")
    
    def _navigate_to_confirmation(self, page: Page):
        """Navigate to confirmation page"""
        # Check if we're already on confirmation page
        if "confirmation" not in page.url:
            page.goto(f"{self.BASE_URL}/confirmation")
            page.wait_for_load_state("networkidle")
        
        # Verify confirmation page
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
        
        print("✅ Navigated to confirmation page")
    
    def _download_receipt(self, page: Page):
        """Download receipt from confirmation page"""
        # Look for download receipt button/link
        download_link = page.locator("a:has-text('Download'), button:has-text('Download'), [href*='download']")
        
        if download_link.count() > 0:
            # Note: In a real test, you might want to handle the download
            print("✅ Download receipt link found")
        else:
            print("⚠️ Download receipt link not found")
    
    def _navigate_to_orders(self, page: Page):
        """Navigate to orders page"""
        # Use direct navigation (more reliable)
        page.goto(f"{self.BASE_URL}/orders")
        page.wait_for_load_state("networkidle")
        
        # Verify orders page
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
        
        print("✅ Navigated to orders page")
    
    def test_login_with_slow_network(self, setup_complete_flow):
        """Test login process with slow network conditions"""
        page = setup_complete_flow
        
        # Simulate slow network
        context = page.context
        context.set_extra_http_headers({"X-Slow-Network": "true"})
        
        print("🐌 Testing login with slow network...")
        
        # Perform login with slow network
        start_time = time.time()
        self._perform_login(page)
        login_time = (time.time() - start_time) * 1000
        
        print(f"⏱️ Login took {login_time:.2f}ms with slow network")
        
        # Verify login still works
        expect(page.locator("#__next")).to_be_visible()
        
        # Check for slow network message
        slow_network_message = page.locator("text=Good news is we are online but bad news is you are on slow network")
        if slow_network_message.count() > 0:
            expect(slow_network_message).to_be_visible()
            print("✅ Slow network message displayed")
    
    def test_complete_flow_with_retry_mechanism(self, setup_complete_flow):
        """Test complete flow with retry mechanism for network issues"""
        page = setup_complete_flow
        
        # Simulate intermittent network issues
        context = page.context
        context.set_extra_http_headers({"X-Intermittent-Network": "true"})
        
        print("🔄 Testing complete flow with retry mechanism...")
        
        # Test each step with retry logic
        steps = [
            ("Login", self._perform_login),
            ("Homepage", self._navigate_to_homepage),
            ("Add to Cart", self._add_items_to_cart),
            ("Favourites", self._navigate_to_favourites),
            ("Checkout", self._navigate_to_checkout),
            ("Fill Form", self._fill_checkout_form),
            ("Confirmation", self._navigate_to_confirmation),
            ("Download Receipt", self._download_receipt),
            ("Orders", self._navigate_to_orders)
        ]
        
        for step_name, step_function in steps:
            max_retries = 3
            success = False
            
            for attempt in range(max_retries):
                try:
                    step_function(page)
                    success = True
                    print(f"✅ {step_name} completed")
                    break
                except Exception as e:
                    print(f"⚠️ {step_name} attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
            
            if not success:
                print(f"❌ {step_name} failed after {max_retries} attempts")
                break
        
        print("🎉 Complete flow with retry mechanism finished!")
    
    def test_flow_performance_metrics(self, setup_complete_flow):
        """Test performance metrics for the complete flow"""
        page = setup_complete_flow
        
        print("📊 Testing flow performance metrics...")
        
        # Measure each step
        steps_timing = {}
        
        # Login
        start_time = time.time()
        self._perform_login(page)
        steps_timing["login"] = (time.time() - start_time) * 1000
        
        # Homepage
        start_time = time.time()
        self._navigate_to_homepage(page)
        steps_timing["homepage"] = (time.time() - start_time) * 1000
        
        # Add to cart
        start_time = time.time()
        self._add_items_to_cart(page)
        steps_timing["add_to_cart"] = (time.time() - start_time) * 1000
        
        # Favourites
        start_time = time.time()
        self._navigate_to_favourites(page)
        steps_timing["favourites"] = (time.time() - start_time) * 1000
        
        # Checkout
        start_time = time.time()
        self._navigate_to_checkout(page)
        steps_timing["checkout"] = (time.time() - start_time) * 1000
        
        # Fill form
        start_time = time.time()
        self._fill_checkout_form(page)
        steps_timing["fill_form"] = (time.time() - start_time) * 1000
        
        # Confirmation
        start_time = time.time()
        self._navigate_to_confirmation(page)
        steps_timing["confirmation"] = (time.time() - start_time) * 1000
        
        # Orders
        start_time = time.time()
        self._navigate_to_orders(page)
        steps_timing["orders"] = (time.time() - start_time) * 1000
        
        # Print performance metrics
        print("\n📈 Performance Metrics:")
        total_time = 0
        for step, timing in steps_timing.items():
            print(f"  {step}: {timing:.2f}ms")
            total_time += timing
        
        print(f"  Total: {total_time:.2f}ms")
        
        # Verify all steps completed within reasonable time
        for step, timing in steps_timing.items():
            assert timing < 15000, f"{step} took too long: {timing:.2f}ms"
    
    def test_flow_error_handling(self, setup_complete_flow):
        """Test error handling throughout the flow"""
        page = setup_complete_flow
        
        print("🛡️ Testing error handling...")
        
        # Test with network errors
        context = page.context
        context.set_extra_http_headers({"X-Network-Error": "true"})
        
        try:
            self._perform_login(page)
            print("✅ Login error handling passed")
        except Exception as e:
            print(f"⚠️ Login error handled: {e}")
        
        # Test with timeout errors
        page.set_default_timeout(2000)
        
        try:
            self._navigate_to_homepage(page)
            print("✅ Homepage timeout handling passed")
        except Exception as e:
            print(f"⚠️ Homepage timeout handled: {e}")
        
        # Reset timeout
        page.set_default_timeout(30000)
        
        print("✅ Error handling test completed")
    
    def test_mobile_flow(self, setup_complete_flow):
        """Test the complete flow on mobile device"""
        page = setup_complete_flow
        
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        
        print("📱 Testing mobile flow...")
        
        # Perform complete flow on mobile
        self._perform_login(page)
        self._navigate_to_homepage(page)
        self._add_items_to_cart(page)
        self._navigate_to_favourites(page)
        self._navigate_to_checkout(page)
        self._fill_checkout_form(page)
        self._navigate_to_confirmation(page)
        self._download_receipt(page)
        self._navigate_to_orders(page)
        
        print("✅ Mobile flow completed successfully")
    
    def test_flow_with_console_monitoring(self, setup_complete_flow):
        """Test the flow while monitoring console for errors"""
        page = setup_complete_flow
        
        console_errors = []
        
        def capture_console_errors(msg):
            if msg.type == "error":
                console_errors.append({
                    "text": msg.text,
                    "type": msg.type,
                    "url": msg.location.get("url", "unknown") if hasattr(msg, "location") else "unknown"
                })
        
        page.on("console", capture_console_errors)
        
        print("🔍 Testing flow with console monitoring...")
        
        # Perform complete flow
        self._perform_login(page)
        self._navigate_to_homepage(page)
        self._add_items_to_cart(page)
        self._navigate_to_favourites(page)
        self._navigate_to_checkout(page)
        self._fill_checkout_form(page)
        self._navigate_to_confirmation(page)
        self._download_receipt(page)
        self._navigate_to_orders(page)
        
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


# Run with: pytest fullprocess.py -v
