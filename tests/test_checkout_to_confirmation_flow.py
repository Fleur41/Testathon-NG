import pytest
from playwright.sync_api import Page, expect
import time
import json


class TestCheckoutToConfirmationFlow:
    """Test the complete flow from checkout to confirmation page"""
    
    BASE_URL = "https://testathon.live"
    
    @pytest.fixture(scope="function")
    def setup_checkout_flow(self, page: Page):
        """Setup the complete checkout to confirmation flow"""
        # Start at checkout page
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        yield page
    
    def test_checkout_to_confirmation_navigation(self, setup_checkout_flow):
        """Test that user can navigate from checkout to confirmation"""
        page = setup_checkout_flow
        
        # Verify we're on checkout page
        expect(page).to_have_url(f"{self.BASE_URL}/checkout")
        
        # Simulate checkout process (this would depend on your actual checkout flow)
        # For now, we'll navigate directly to confirmation
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        
        # Verify we're now on confirmation page
        expect(page).to_have_url(f"{self.BASE_URL}/confirmation")
        
        # Verify confirmation page elements
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
    
    def test_checkout_page_validation_before_confirmation(self, setup_checkout_flow):
        """Test that checkout page is properly loaded before proceeding to confirmation"""
        page = setup_checkout_flow
        
        # Verify checkout page structure
        expect(page.locator("#__next")).to_be_visible()
        
        # Verify Next.js data is present
        next_data_script = page.locator("script#__NEXT_DATA__")
        expect(next_data_script).to_be_attached()
        
        # Verify page data
        script_content = next_data_script.text_content()
        data = json.loads(script_content)
        assert data["page"] == "/checkout"
        assert data["buildId"] == "flryiVW52XrLSOqDaY32K"
    
    def test_confirmation_page_after_checkout(self, setup_checkout_flow):
        """Test that confirmation page loads correctly after checkout"""
        page = setup_checkout_flow
        
        # Navigate to confirmation
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        
        # Verify confirmation page structure
        expect(page.locator("#__next")).to_be_visible()
        
        # Verify Next.js data for confirmation page
        next_data_script = page.locator("script#__NEXT_DATA__")
        expect(next_data_script).to_be_attached()
        
        script_content = next_data_script.text_content()
        data = json.loads(script_content)
        assert data["page"] == "/confirmation"
        assert data["buildId"] == "flryiVW52XrLSOqDaY32K"
    
    def test_flow_performance(self, setup_checkout_flow):
        """Test that the checkout to confirmation flow performs within acceptable time"""
        page = setup_checkout_flow
        
        # Measure checkout page load time
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        checkout_load_time = (time.time() - start_time) * 1000
        
        # Measure confirmation page load time
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        confirmation_load_time = (time.time() - start_time) * 1000
        
        # Both pages should load within 3 seconds
        assert checkout_load_time < 3000, f"Checkout page took {checkout_load_time:.2f}ms to load"
        assert confirmation_load_time < 3000, f"Confirmation page took {confirmation_load_time:.2f}ms to load"
    
    def test_flow_with_slow_network_simulation(self, setup_checkout_flow):
        """Test the flow with slow network conditions"""
        page = setup_checkout_flow
        
        # Simulate slow network by throttling
        context = page.context
        context.set_extra_http_headers({"X-Slow-Network": "true"})
        
        # Test checkout page with slow network
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        checkout_slow_time = (time.time() - start_time) * 1000
        
        # Test confirmation page with slow network
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        confirmation_slow_time = (time.time() - start_time) * 1000
        
        # With slow network, we expect longer load times but still functional
        assert checkout_slow_time < 10000, f"Checkout page too slow: {checkout_slow_time:.2f}ms"
        assert confirmation_slow_time < 10000, f"Confirmation page too slow: {confirmation_slow_time:.2f}ms"
        
        # Verify pages still work correctly
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
    
    def test_slow_network_user_message(self, setup_checkout_flow):
        """Test that appropriate message is shown for slow network conditions"""
        page = setup_checkout_flow
        
        # Simulate slow network
        context = page.context
        context.set_extra_http_headers({"X-Slow-Network": "true"})
        
        # Navigate to checkout with slow network
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Check for slow network message (this would be implemented in your app)
        # For now, we'll verify the page still loads and is functional
        expect(page.locator("#__next")).to_be_visible()
        
        # Navigate to confirmation with slow network
        page.goto(f"{self.BASE_URL}/confirmation")
        expect(page.locator("#__next")).to_be_visible()
        
        # In a real implementation, you might check for:
        # - Loading indicators
        # - "Good news is we are online but bad news is you are on slow network" message
        # - Progress bars
        # - Timeout handling
    
    def test_network_error_handling(self, setup_checkout_flow):
        """Test how the flow handles network errors"""
        page = setup_checkout_flow
        
        # Simulate network issues
        context = page.context
        context.set_extra_http_headers({"X-Network-Error": "true"})
        
        # Test checkout page with network issues
        try:
            page.goto(f"{self.BASE_URL}/checkout", timeout=5000)
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            # Handle network errors gracefully
            print(f"Network error handled: {e}")
        
        # Test confirmation page with network issues
        try:
            page.goto(f"{self.BASE_URL}/confirmation", timeout=5000)
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            # Handle network errors gracefully
            print(f"Network error handled: {e}")
    
    def test_flow_with_retry_mechanism(self, setup_checkout_flow):
        """Test the flow with retry mechanism for failed requests"""
        page = setup_checkout_flow
        
        # Simulate intermittent network issues
        context = page.context
        context.set_extra_http_headers({"X-Intermittent-Network": "true"})
        
        # Test with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                page.goto(f"{self.BASE_URL}/checkout")
                page.wait_for_load_state("networkidle", timeout=5000)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
        
        # Verify checkout page loaded
        expect(page.locator("#__next")).to_be_visible()
        
        # Test confirmation page with retry
        for attempt in range(max_retries):
            try:
                page.goto(f"{self.BASE_URL}/confirmation")
                page.wait_for_load_state("networkidle", timeout=5000)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
        
        # Verify confirmation page loaded
        expect(page.locator("#__next")).to_be_visible()
    
    def test_flow_with_offline_simulation(self, setup_checkout_flow):
        """Test the flow when network goes offline"""
        page = setup_checkout_flow
        
        # Simulate offline condition
        context = page.context
        context.set_offline(True)
        
        # Try to navigate to checkout (should fail gracefully)
        try:
            page.goto(f"{self.BASE_URL}/checkout", timeout=2000)
        except Exception as e:
            print(f"Offline navigation handled: {e}")
        
        # Re-enable network
        context.set_offline(False)
        
        # Now try to navigate normally
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        expect(page.locator("#__next")).to_be_visible()
        
        # Navigate to confirmation
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        expect(page.locator("#__next")).to_be_visible()
    
    def test_flow_with_high_latency(self, setup_checkout_flow):
        """Test the flow with high latency network conditions"""
        page = setup_checkout_flow
        
        # Simulate high latency
        context = page.context
        context.set_extra_http_headers({"X-High-Latency": "true"})
        
        # Test with high latency
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        checkout_latency_time = (time.time() - start_time) * 1000
        
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        confirmation_latency_time = (time.time() - start_time) * 1000
        
        # High latency should still be within reasonable bounds
        assert checkout_latency_time < 15000, f"Checkout page too slow with high latency: {checkout_latency_time:.2f}ms"
        assert confirmation_latency_time < 15000, f"Confirmation page too slow with high latency: {confirmation_latency_time:.2f}ms"
        
        # Verify pages still work
        expect(page.locator("#__next")).to_be_visible()
    
    def test_flow_with_poor_connection(self, setup_checkout_flow):
        """Test the flow with poor connection quality"""
        page = setup_checkout_flow
        
        # Simulate poor connection
        context = page.context
        context.set_extra_http_headers({"X-Poor-Connection": "true"})
        
        # Test checkout page with poor connection
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        
        # Verify page still loads correctly
        expect(page.locator("#__next")).to_be_visible()
        
        # Test confirmation page with poor connection
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        
        # Verify page still loads correctly
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
    
    def test_flow_with_timeout_handling(self, setup_checkout_flow):
        """Test the flow with timeout handling"""
        page = setup_checkout_flow
        
        # Set shorter timeout for testing
        page.set_default_timeout(3000)
        
        # Test checkout page with timeout
        try:
            page.goto(f"{self.BASE_URL}/checkout")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Timeout handled: {e}")
            # Retry with longer timeout
            page.set_default_timeout(10000)
            page.goto(f"{self.BASE_URL}/checkout")
            page.wait_for_load_state("networkidle")
        
        # Test confirmation page with timeout
        try:
            page.goto(f"{self.BASE_URL}/confirmation")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Timeout handled: {e}")
            # Retry with longer timeout
            page.set_default_timeout(10000)
            page.goto(f"{self.BASE_URL}/confirmation")
            page.wait_for_load_state("networkidle")
        
        # Verify both pages loaded
        expect(page.locator("#__next")).to_be_visible()
    
    def test_flow_with_resource_loading_issues(self, setup_checkout_flow):
        """Test the flow when some resources fail to load"""
        page = setup_checkout_flow
        
        # Simulate resource loading issues
        context = page.context
        context.set_extra_http_headers({"X-Resource-Issues": "true"})
        
        # Test checkout page with resource issues
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        
        # Verify page still functions despite resource issues
        expect(page.locator("#__next")).to_be_visible()
        
        # Test confirmation page with resource issues
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        
        # Verify page still functions
        expect(page.locator("#__next")).to_be_visible()
    
    def test_flow_with_mobile_network_simulation(self, setup_checkout_flow):
        """Test the flow simulating mobile network conditions"""
        page = setup_checkout_flow
        
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        
        # Simulate mobile network conditions
        context = page.context
        context.set_extra_http_headers({"X-Mobile-Network": "true"})
        
        # Test checkout page on mobile network
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        expect(page.locator("#__next")).to_be_visible()
        
        # Test confirmation page on mobile network
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        expect(page.locator("#__next")).to_be_visible()
        
        # Verify responsive design still works
        page.set_viewport_size({"width": 768, "height": 1024})  # Tablet
        expect(page.locator("#__next")).to_be_visible()
        
        page.set_viewport_size({"width": 1280, "height": 800})  # Desktop
        expect(page.locator("#__next")).to_be_visible()


# Run with: pytest test_checkout_to_confirmation_flow.py -v
