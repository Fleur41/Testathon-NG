<https://www.browserstack.com/docs/automate/playwright/getting-started/python/integrate-your-tests?fw-lang=python>

```bash
# ensure you have pipx and pipenv installed
pipx install pipenv
pipenv install
pipenv shell
playwright install # install browsers
pytest test_login.py
```

Local execution: `pytest test_login.py` (fast, local browser)
BrowserStack execution: `browserstack-sdk pytest test_login.py` (cloud browsers, cross-platform testing)
