# Testathon

Automated web testing helper for functional and lightweight performance checks.

This repository contains pytest-based web tests and utilities focused on verifying:

- HTTP status codes and basic API responses
- Page performance (simple timing / response time checks)
- Link health (broken link detection)
- Forms and basic flows (login, checkout, search)
- API contract and simple JSON validation

The tests are written in Python (pytest). Example tests and a runnable test suite are stored in the `tests/` folder.

## Quick start

1. Create a virtual environment and install dependencies. From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tests/requirements.txt
# or if you use Pipenv
pipenv install --dev --python 3.11
```

2. Configure the environment (see Environment Configuration below).

3. Run the full test suite with pytest:

```bash
pytest -q
```

Run a single test file (example):

```bash
pytest -q tests/test_homepage.py::test_homepage_loads
```

Run tests and output results in JUnit XML (CI friendly):

```bash
pytest -q --junitxml=reports/junit.xml
```

## Environment configuration

The test suite reads settings from environment variables so you can target different environments (local, staging, production) without changing code.

Common environment variables used in this project:

- TEST_BASE_URL - Base URL under test, e.g. https://staging.example.com
- API_BASE_URL - Base URL for API tests (if different)
- TEST_TIMEOUT - Request timeout in seconds (default: 10)
- BROWSERSTACK_USERNAME / BROWSERSTACK_ACCESS_KEY - credentials for BrowserStack runs (if used)

Set them inline when running commands, or export them in your shell:

```bash
export TEST_BASE_URL=https://staging.example.com
export API_BASE_URL=https://api.staging.example.com
export TEST_TIMEOUT=15
pytest -q
```

You can also create a `.env` file and load it in your shell before running tests using `dotenv` or `direnv`.

## Python examples

Below are copy-paste ready examples you can add as new tests or run interactively. These use `requests` and `pytest` style assertions. The project's tests already provide similar patterns in `tests/`.

1) Check HTTP status and response time

```python
import os
import requests
from time import perf_counter

BASE = os.getenv('TEST_BASE_URL', 'https://example.com')

def test_homepage_status_and_speed():
    url = f"{BASE}/"
    t0 = perf_counter()
    r = requests.get(url, timeout=int(os.getenv('TEST_TIMEOUT', 10)))
    elapsed = perf_counter() - t0

    assert r.status_code == 200, f"unexpected status {r.status_code}"
    # Acceptable page load (server response) under 1 second
    assert elapsed < 1.0, f"page too slow: {elapsed:.2f}s"

```

2) Simple API JSON contract check

```python
import os
import requests

BASE = os.getenv('API_BASE_URL', os.getenv('TEST_BASE_URL', 'https://example.com'))

def test_api_health():
    r = requests.get(f"{BASE}/api/health", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert 'status' in data and data['status'] == 'ok'

```

3) Form submit (login) example

```python
import os
import requests

BASE = os.getenv('TEST_BASE_URL', 'https://example.com')

def test_login_flow():
    session = requests.Session()
    # first load login page for cookies or CSRF token
    r = session.get(f"{BASE}/login")
    assert r.status_code == 200

    # Extract CSRF token example (adjust selector for your site)
    # import re
    # token = re.search(r'name="csrf" value="([^"]+)"', r.text).group(1)

    payload = {"username": "testuser", "password": "password123"}
    r2 = session.post(f"{BASE}/login", data=payload, allow_redirects=True)
    assert r2.status_code in (200, 302)
    # After login, check user-specific page
    r3 = session.get(f"{BASE}/account")
    assert r3.status_code == 200
    assert "Welcome" in r3.text

```

4) Broken link checker (basic)

```python
import os
import requests
from bs4 import BeautifulSoup

BASE = os.getenv('TEST_BASE_URL', 'https://example.com')

def test_no_broken_links():
    r = requests.get(BASE, timeout=10)
    assert r.status_code == 200
    soup = BeautifulSoup(r.text, 'html.parser')

    links = [a.get('href') for a in soup.find_all('a', href=True)]
    # Filter external links or relative ones as needed
    broken = []
    for href in links:
        if href.startswith('#'):
            continue
        if href.startswith('mailto:'):
            continue
        if href.startswith('http'):
            url = href
        else:
            url = BASE.rstrip('/') + '/' + href.lstrip('/')
        try:
            rr = requests.head(url, allow_redirects=True, timeout=5)
            if rr.status_code >= 400:
                broken.append((url, rr.status_code))
        except Exception as e:
            broken.append((url, str(e)))

    assert not broken, f"Broken links found: {broken}"

```

5) Performance smoke test for an API (throughput)

```python
import os
import requests
from concurrent.futures import ThreadPoolExecutor

API = os.getenv('API_BASE_URL', os.getenv('TEST_BASE_URL', 'https://example.com'))

def _call(endpoint):
    r = requests.get(f"{API}{endpoint}", timeout=10)
    return r.status_code

def test_api_throughput():
    endpoints = ['/api/products', '/api/categories']
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(lambda ep: _call(ep), endpoints * 5))

    # Ensure no 5xx responses in the small burst
    assert all(200 <= s < 500 for s in results), f"Unexpected status codes: {results}"

```

## Command line usage for batch testing

Use pytest directly for batch runs. Typical flags:

- `-k` run tests matching expression
- `-m` run tests marked with a marker
- `-n` from pytest-xdist to run tests in parallel (install pytest-xdist)
- `--maxfail=1` stop after first failure

Examples:

Run all tests matching "checkout":

```bash
TEST_BASE_URL=https://staging.example.com pytest -q -k checkout
```

Run tests in parallel (4 workers):

```bash
pip install pytest-xdist
TEST_BASE_URL=https://staging.example.com pytest -q -n 4
```

Run API tests only (assumes tests are marked with @pytest.mark.api)

```bash
pytest -q -m api
```

Run a scripted batch from the included utility (if present):

```bash
python3 tests/run_checkout_flow_tests.py --base-url=https://staging.example.com
```

If you use CI, set `TEST_BASE_URL` and `API_BASE_URL` in your CI pipeline and run `pytest` as part of the build.

## Tips and next steps

- Use smaller, focused tests for functional checks and separate performance tests (smoke only) so the suite stays fast.
- Add more assertions for payload shapes using `jsonschema` or Pydantic for API contract tests.
- Integrate with BrowserStack or Selenium for full browser-based end-to-end verification; keep those tests in a separate mark `@pytest.mark.browser` to avoid running them in every pipeline.
- A quick helper script to run health checks periodically can be added to `scripts/` and scheduled via cron or CI pipelines.

## Files of interest

- `tests/` - contains pytest tests and helpers. Look at `test_homepage.py`, `test_checkout.py`, and `fullprocess.py` for examples.
- `tests/requirements.txt` - Python dependencies for running tests.
- `pytest.ini` - pytest configuration and markers used by the suite.

---

If you'd like, I can also:

- Add a small `scripts/run_smoke.sh` wrapper to run a defined set of smoke tests.
- Add a `requirements-dev.txt` with pinned versions that match the project's tests.

Tell me which you'd prefer next.

## How we ran these specific testcases

The following files contain the testcases you asked to document. Below is a practical, copy-paste guide showing the exact commands used to execute them, how to capture results in JUnit/XML and HTML, and an example pytest summary (clearly labeled as a sample output you can expect).

Test files covered here:

- `tests/run_checkout_flow_tests.py`
- `tests/test_checkout_to_confirmation_flow.py`
- `tests/test_checkout.py`
- `tests/test_confirmationpage.py`
- `tests/test_favourites.py`
- `tests/test_homepage.py`
- `tests/test_login.py`
- `tests/test_orders.py`
- `tests/test_slow_network_edge_cases.py`

Commands used to run the above tests (from the project root):

```bash
# create and activate a venv (macOS / zsh)
python3 -m venv .venv
source .venv/bin/activate

# install test dependencies
pip install -r tests/requirements.txt

# run the listed tests (explicit files)
pytest -q \
    tests/test_homepage.py \
    tests/test_login.py \
    tests/test_checkout.py \
    tests/test_checkout_to_confirmation_flow.py \
    tests/test_confirmationpage.py \
    tests/test_favourites.py \
    tests/test_orders.py \
    tests/run_checkout_flow_tests.py \
    tests/test_slow_network_edge_cases.py
```

Capture JUnit XML (CI friendly) and a simple HTML report:

```bash
# JUnit XML
pytest -q --junitxml=reports/junit.xml \
    tests/test_homepage.py tests/test_login.py tests/test_checkout.py ...

# HTML report (requires pytest-html)
pip install pytest-html
pytest -q --html=reports/report.html --self-contained-html \
    tests/test_homepage.py tests/test_login.py tests/test_checkout.py ...
```

Environment variables

Before running the suite, ensure the environment variables for target URLs are set, for example:

```bash
export TEST_BASE_URL=https://staging.example.com
export API_BASE_URL=https://api.staging.example.com
export TEST_TIMEOUT=15
```

Example pytest summary (sample)

Below is a sample run summary you will typically see at the end of a successful test run. This is an illustrative example — replace it with the actual output from your environment when you run the suite.

```text
=========================== test session starts ===========================
platform darwin -- Python 3.x.y, pytest-7.x, pluggy-1.x
collected 42 items

tests/test_homepage.py ........                                       [ 19%]
tests/test_login.py .......                                         [ 36%]
tests/test_checkout.py ...........                                  [ 64%]
tests/test_checkout_to_confirmation_flow.py ..                      [ 69%]
tests/test_confirmationpage.py .....                                 [ 81%]
tests/test_favourites.py ..                                          [ 86%]
tests/test_orders.py ....                                             [ 95%]
tests/test_slow_network_edge_cases.py .                              [100%]

============================ 42 passed in 12.34s ==========================
