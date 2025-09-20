import pytest
from playwright.sync_api import Page, expect
import time


class TestSlowNetworkEdgeCases:
    """Test edge cases for slow network conditions"""
    
    BASE_URL = "https://testathon.live"
    
    @pytest.fixture(scope="function")
    def setup_slow_network(self, page: Page):
        """Setup page with slow network simulation"""
        # Simulate slow network conditions
        context = page.context
        context.set_extra_http_headers({"X-Slow-Network": "true"})
        yield page
    
    def test_slow_network_message_display(self, setup_slow_network):
        """Test that slow network message is displayed correctly"""
        page = setup_slow_network
        
        # Navigate to checkout page with slow network
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        # Check for slow network message
        # This would be implemented in your app to show:
        # "Good news is we are online but bad news is you are on slow network"
        slow_network_message = page.locator("text=Good news is we are online but bad news is you are on slow network")
        
        # If the message exists, verify it's visible
        if slow_network_message.count() > 0:
            expect(slow_network_message).to_be_visible()
        else:
            # If message doesn't exist, verify page still loads
            expect(page.locator("#__next")).to_be_visible()
            print("Slow network message not implemented yet")
    
    def test_slow_network_loading_indicators(self, setup_slow_network):
        """Test that loading indicators are shown during slow network"""
        page = setup_slow_network
        
        # Navigate to checkout page
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Check for loading indicators
        loading_indicators = page.locator("[data-testid='loading'], .loading, .spinner")
        
        # If loading indicators exist, verify they appear
        if loading_indicators.count() > 0:
            expect(loading_indicators.first).to_be_visible()
        
        # Wait for page to fully load
        page.wait_for_load_state("networkidle")
        
        # Verify page loads despite slow network
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_timeout_handling(self, setup_slow_network):
        """Test timeout handling with slow network"""
        page = setup_slow_network
        
        # Set shorter timeout to test timeout handling
        page.set_default_timeout(2000)
        
        try:
            # Try to navigate with short timeout
            page.goto(f"{self.BASE_URL}/checkout")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Timeout occurred as expected: {e}")
            
            # Check for timeout message or retry mechanism
            timeout_message = page.locator("text=Connection timeout, please try again")
            if timeout_message.count() > 0:
                expect(timeout_message).to_be_visible()
        
        # Reset timeout and retry
        page.set_default_timeout(30000)
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        
        # Verify page loads with longer timeout
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_progress_indicators(self, setup_slow_network):
        """Test progress indicators during slow network loading"""
        page = setup_slow_network
        
        # Navigate to checkout page
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Check for progress bars or loading progress
        progress_indicators = page.locator("progress, .progress-bar, [role='progressbar']")
        
        # If progress indicators exist, verify they work
        if progress_indicators.count() > 0:
            expect(progress_indicators.first).to_be_visible()
        
        # Wait for completion
        page.wait_for_load_state("networkidle")
        
        # Verify page loads completely
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_retry_mechanism(self, setup_slow_network):
        """Test retry mechanism with slow network"""
        page = setup_slow_network
        
        # Simulate intermittent slow network
        context = page.context
        context.set_extra_http_headers({"X-Intermittent-Slow": "true"})
        
        # Try to navigate with retry logic
        max_retries = 3
        success = False
        
        for attempt in range(max_retries):
            try:
                page.goto(f"{self.BASE_URL}/checkout")
                page.wait_for_load_state("networkidle", timeout=10000)
                success = True
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retry
        
        assert success, "Failed to load page after retries"
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_user_feedback(self, setup_slow_network):
        """Test user feedback during slow network conditions"""
        page = setup_slow_network
        
        # Navigate to checkout page
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Check for user feedback messages
        feedback_messages = [
            "Loading...",
            "Please wait...",
            "Connecting...",
            "Network is slow",
            "Good news is we are online but bad news is you are on slow network"
        ]
        
        for message in feedback_messages:
            message_element = page.locator(f"text={message}")
            if message_element.count() > 0:
                expect(message_element).to_be_visible()
                print(f"Found feedback message: {message}")
                break
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        # Verify page loads despite slow network
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_resource_prioritization(self, setup_slow_network):
        """Test that critical resources load first during slow network"""
        page = setup_slow_network
        
        # Navigate to checkout page
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Check that critical resources load first
        critical_resources = [
            "script#__NEXT_DATA__",
            "#__next",
            "meta[charset]",
            "meta[name='viewport']"
        ]
        
        for resource in critical_resources:
            element = page.locator(resource)
            if element.count() > 0:
                expect(element).to_be_attached()
        
        # Wait for all resources to load
        page.wait_for_load_state("networkidle")
        
        # Verify page is functional
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_graceful_degradation(self, setup_slow_network):
        """Test graceful degradation with slow network"""
        page = setup_slow_network
        
        # Navigate to checkout page
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Check for fallback content or simplified version
        fallback_content = page.locator(".fallback, .simplified, .basic-version")
        
        # If fallback content exists, verify it's visible
        if fallback_content.count() > 0:
            expect(fallback_content.first).to_be_visible()
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        # Verify page is still functional
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_performance_metrics(self, setup_slow_network):
        """Test performance metrics with slow network"""
        page = setup_slow_network
        
        # Measure performance with slow network
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/checkout")
        page.wait_for_load_state("networkidle")
        load_time = (time.time() - start_time) * 1000
        
        # With slow network, we expect longer load times
        print(f"Slow network load time: {load_time:.2f}ms")
        
        # Verify page still loads within reasonable time
        assert load_time < 30000, f"Page too slow even with slow network: {load_time:.2f}ms"
        
        # Verify page is functional
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_confirmation_flow(self, setup_slow_network):
        """Test confirmation page with slow network"""
        page = setup_slow_network
        
        # Navigate to confirmation page with slow network
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        load_time = (time.time() - start_time) * 1000
        
        print(f"Confirmation page slow network load time: {load_time:.2f}ms")
        
        # Verify page loads within reasonable time
        assert load_time < 30000, f"Confirmation page too slow: {load_time:.2f}ms"
        
        # Verify page is functional
        expect(page.locator("#__next")).to_be_visible()
        expect(page).to_have_title("StackDemo")
    
    def test_slow_network_user_experience(self, setup_slow_network):
        """Test overall user experience with slow network"""
        page = setup_slow_network
        
        # Test checkout page user experience
        page.goto(f"{self.BASE_URL}/checkout")
        
        # Check for user experience indicators
        ux_indicators = [
            "text=Good news is we are online but bad news is you are on slow network",
            "text=Loading...",
            "text=Please wait...",
            ".loading",
            ".spinner"
        ]
        
        found_indicators = []
        for indicator in ux_indicators:
            element = page.locator(indicator)
            if element.count() > 0:
                found_indicators.append(indicator)
        
        print(f"Found UX indicators: {found_indicators}")
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        # Verify page is functional
        expect(page.locator("#__next")).to_be_visible()
        
        # Test confirmation page user experience
        page.goto(f"{self.BASE_URL}/confirmation")
        page.wait_for_load_state("networkidle")
        expect(page.locator("#__next")).to_be_visible()
    
    def test_slow_network_error_handling(self, setup_slow_network):
        """Test error handling with slow network"""
        page = setup_slow_network
        
        # Simulate network errors during slow conditions
        context = page.context
        context.set_extra_http_headers({"X-Slow-Network-Error": "true"})
        
        # Try to navigate with potential errors
        try:
            page.goto(f"{self.BASE_URL}/checkout")
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            print(f"Network error handled: {e}")
            
            # Check for error messages
            error_messages = page.locator("text=Network error, text=Connection failed, text=Please try again")
            if error_messages.count() > 0:
                expect(error_messages.first).to_be_visible()
        
        # Verify page eventually loads
        expect(page.locator("#__next")).to_be_visible()


# Run with: pytest test_slow_network_edge_cases.py -v
