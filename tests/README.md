# Testathon-NG: Comprehensive E-commerce Testing Suite

## Project Overview
Testathon-NG is a comprehensive end-to-end testing suite built with Playwright and Python, designed to test the StackDemo e-commerce application. The project provides robust testing capabilities for various user flows including login, checkout, orders, and homepage functionality, with support for both local and cloud-based testing via BrowserStack.

## Features
- Comprehensive Test Coverage: Tests for homepage, login, checkout, orders, and confirmation pages
- Cross-Browser Testing: Support for Chrome, Firefox, Safari, and Edge
- Cloud Testing: BrowserStack integration for cross-platform testing
- Performance Testing: Load time and performance validation
- Accessibility Testing: Basic accessibility compliance checks
- Responsive Design Testing: Multi-viewport testing for mobile, tablet, and desktop
- Network Edge Cases: Slow network simulation and error handling
- Parallel Execution: Support for running tests in parallel
- Detailed Reporting: Comprehensive test reports with screenshots and logs

## Project Structure
```
Testathon/
├── README.md                          # This file
├── tests/                             # Test directory
│   ├── conftest.py                    # Pytest configuration and fixtures
│   ├── pytest.ini                    # Pytest settings and markers
│   ├── browserstack.yml              # BrowserStack configuration
│   ├── Pipfile                       # Python dependencies
│   ├── Pipfile.lock                  # Locked dependencies
│   ├── requirements.txt              # Alternative dependency file
│   ├── test_homepage.py              # Homepage functionality tests
│   ├── test_login.py                 # Login page tests
│   ├── test_checkout.py              # Checkout page tests
│   ├── test_orders.py                # Orders page tests
│   ├── test_confirmationpage.py      # Confirmation page tests
│   ├── test_favourites.py            # Favorites functionality tests
│   ├── test_checkout_to_confirmation_flow.py  # End-to-end flow tests
│   ├── test_slow_network_edge_cases.py        # Network edge case tests
│   ├── run_checkout_flow_tests.py    # Checkout flow test runner
│   ├── fullprocess.py                # Full process automation
│   └── log/                          # Test logs and metrics
│       ├── key-metrics.json.lock
│       └── pytest_configs.json
```

## Prerequisites
Before setting up the project, ensure you have the following installed:
- Python 3.8+ (recommended: Python 3.9 or higher)
- pipx - For installing pipenv
- pipenv - For dependency management
- Git - For version control

### Installing Prerequisites

#### macOS (using Homebrew):
```bash
# Install Python
brew install python

# Install pipx
brew install pipx
pipx ensurepath

# Install pipenv
pipx install pipenv
```

#### Windows:
```bash
# Install Python from python.org
# Install pipx
python -m pip install --user pipx
python -m pipx ensurepath

# Install pipenv
pipx install pipenv
```

#### Linux (Ubuntu/Debian):
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip

# Install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install pipenv
pipx install pipenv
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Testathon
```

### 2. Set Up Virtual Environment
```bash
# Navigate to the tests directory
cd tests

# Create and activate virtual environment
pipenv install

# Activate the virtual environment
pipenv shell
```

### 3. Install Playwright Browsers
```bash
# Install Playwright browsers
playwright install

# Install specific browsers (optional)
playwright install chromium firefox webkit
```

### 4. Verify Installation
```bash
# Run a simple test to verify setup
pytest test_homepage.py::test_homepage_title -v
```

## Test Execution

### Local Testing

#### Run All Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with detailed output
pytest -v --tb=short
```

#### Run Specific Test Files
```bash
# Run homepage tests
pytest test_homepage.py

# Run login tests
pytest test_login.py

# Run checkout tests
pytest test_checkout.py

# Run orders tests
pytest test_orders.py
```

#### Run Specific Tests
```bash
# Run specific test function
pytest test_homepage.py::test_homepage_title

# Run tests with specific markers
pytest -m checkout
pytest -m performance
```

#### Run Tests with Different Options
```bash
# Run with headed browser (visible)
pytest --headed

# Run in parallel (if pytest-xdist is installed)
pytest -n auto

# Run with custom timeout
pytest --timeout=600

# Run and generate HTML report
pytest --html=report.html --self-contained-html
```

### BrowserStack Cloud Testing

#### Prerequisites for BrowserStack
1. Create a BrowserStack account at browserstack.com
2. Get your username and access key from the account settings
3. Update browserstack.yml with your credentials

#### Run Tests on BrowserStack
```bash
# Install BrowserStack SDK
pip install browserstack-sdk

# Run tests on BrowserStack
browserstack-sdk pytest test_homepage.py

# Run all tests on BrowserStack
browserstack-sdk pytest

# Run with specific configuration
browserstack-sdk pytest test_checkout.py --config browserstack.yml
```

## Test Categories

### 1. Homepage Tests (test_homepage.py)
- Page title validation
- Footer presence and visibility
- Page structure verification
- Favicon validation
- Viewport meta tag testing
- Responsive design checks
- Performance metrics
- Accessibility compliance

### 2. Login Tests (test_login.py)
- Login page title validation
- Logo visibility
- Username/password dropdown presence
- Login button functionality
- Form structure validation
- Input field validation
- Error handling
- Successful login flow

### 3. Checkout Tests (test_checkout.py)
- Page title and structure
- Meta tags validation
- CSS/JS resource loading
- Script tag verification
- Next.js data validation
- Async script loading
- Preload links verification
- Performance testing
- Responsive design validation

### 4. Orders Tests (test_orders.py)
- Orders page functionality
- Script and resource loading
- Performance validation
- Accessibility checks
- Responsive design testing
- Console error validation
- Page structure verification

### 5. Confirmation Tests (test_confirmationpage.py)
- Confirmation page validation
- Order completion verification
- Page structure and content
- Performance metrics

### 6. Favorites Tests (test_favourites.py)
- Favorites functionality
- User interaction testing
- State management validation

### 7. Flow Tests (test_checkout_to_confirmation_flow.py)
- End-to-end user journeys
- Complete checkout process
- Cross-page functionality
- Data persistence validation

### 8. Edge Case Tests (test_slow_network_edge_cases.py)
- Slow network simulation
- Timeout handling
- Error recovery
- Network failure scenarios

## Configuration

### Pytest Configuration (pytest.ini)
```ini
[tool:pytest]
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Test execution order
collect_ignore = ["__pycache__", "*.pyc"]

# Verbose output
addopts = -v --tb=short

# Timeout for tests (in seconds)
timeout = 300

# Markers for test categorization
markers =
    checkout: Tests for checkout page
    confirmation: Tests for confirmation page
    flow: Tests for checkout to confirmation flow
    slow_network: Tests for slow network edge cases
    performance: Performance tests
    edge_case: Edge case tests
```

### BrowserStack Configuration (browserstack.yml)
```yaml
# BrowserStack Credentials
userName: your_username
accessKey: your_access_key

# Project Configuration
projectName: Testathon-NG
buildName: testathon build
buildIdentifier: '#${BUILD_NUMBER}'
framework: pytest

# Test Platforms
platforms:
  - os: Windows
    osVersion: 11
    browserName: playwright-chromium
    browserVersion: latest
  - os: Windows
    osVersion: 10
    browserName: playwright-chromium
    browserVersion: latest

# Parallel Execution
parallelsPerPlatform: 1

# Debugging Features
debug: false
networkLogs: false
consoleLogs: errors
```

### Environment Variables
Create a .env file in the tests directory:
```bash
# BrowserStack Credentials
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key

# Test Configuration
BASE_URL=https://testathon.live
HEADLESS=true
BROWSER=chromium
```

## BrowserStack Integration

### Setting Up BrowserStack
1. Create Account: Sign up at browserstack.com
2. Get Credentials: Find your username and access key in account settings
3. Update Configuration: Modify browserstack.yml with your credentials
4. Install SDK: pip install browserstack-sdk

### BrowserStack Features
- Cross-Platform Testing: Test on Windows, macOS, Linux
- Multiple Browsers: Chrome, Firefox, Safari, Edge
- Mobile Testing: iOS and Android devices
- Parallel Execution: Run tests simultaneously
- Video Recording: Automatic video capture of test runs
- Screenshots: Automatic screenshot capture on failures
- Network Logs: HAR file generation for debugging
- Console Logs: Browser console output capture

### Running Tests on BrowserStack
```bash
# Basic execution
browserstack-sdk pytest

# With specific configuration
browserstack-sdk pytest --config browserstack.yml

# Run specific test file
browserstack-sdk pytest test_checkout.py

# Run with custom build name
browserstack-sdk pytest --build-name "Feature Testing"
```

## Troubleshooting

### Common Issues

#### 1. Browser Installation Issues
```bash
# Reinstall Playwright browsers
playwright install --force

# Install specific browser
playwright install chromium
```

#### 2. Permission Issues
```bash
# Fix pipenv permissions
pipenv --python python3

# Recreate virtual environment
rm -rf .venv
pipenv install
```

#### 3. Test Failures
```bash
# Run with detailed output
pytest -v --tb=long

# Run single test for debugging
pytest test_homepage.py::test_homepage_title -v -s

# Run with headed browser
pytest --headed
```

#### 4. BrowserStack Connection Issues
```bash
# Verify credentials
echo $BROWSERSTACK_USERNAME
echo $BROWSERSTACK_ACCESS_KEY

# Test connection
browserstack-sdk pytest test_homepage.py::test_homepage_title
```

### Debug Mode
Enable debug mode for detailed logging:
```bash
# Run with debug output
pytest -v -s --tb=long

# Run with Playwright debug
DEBUG=pw:api pytest test_homepage.py

# Run with BrowserStack debug
browserstack-sdk pytest --debug
```

### Performance Issues
```bash
# Run tests in parallel
pytest -n auto

# Run with reduced timeout
pytest --timeout=60

# Run specific test categories
pytest -m "not slow_network"
```

## Test Reports

### HTML Reports
```bash
# Generate HTML report
pytest --html=report.html --self-contained-html

# Generate with screenshots
pytest --html=report.html --self-contained-html --screenshot=only-on-failure
```

### JUnit Reports
```bash
# Generate JUnit XML report
pytest --junitxml=report.xml
```

### Coverage Reports
```bash
# Install coverage
pip install pytest-cov

# Run with coverage
pytest --cov=. --cov-report=html
```

## Contributing

### Adding New Tests
1. Create Test File: Follow naming convention test_*.py
2. Use Fixtures: Leverage existing fixtures from conftest.py
3. Add Markers: Use appropriate markers for test categorization
4. Document Tests: Add docstrings explaining test purpose
5. Follow Patterns: Use existing test patterns for consistency

### Test Structure Template
```python
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def setup_page(page: Page):
    """Setup fixture for page navigation"""
    page.goto("https://testathon.live/your-page")
    yield page

def test_your_functionality(setup_page):
    """Test description"""
    page = setup_page
    
    # Test implementation
    expect(page.locator("selector")).to_be_visible()
    assert page.title() == "Expected Title"
```

### Code Style
- Follow PEP 8 guidelines
- Use descriptive test names
- Add type hints where appropriate
- Include docstrings for all functions
- Use meaningful variable names

## Additional Resources
- Playwright Documentation: https://playwright.dev/python/
- Pytest Documentation: https://docs.pytest.org/
- BrowserStack Playwright Guide: https://www.browserstack.com/docs/automate/playwright
- Python Testing Best Practices: https://docs.python.org/3/library/unittest.html

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review BrowserStack documentation
- Consult Playwright documentation

---
Happy Testing!