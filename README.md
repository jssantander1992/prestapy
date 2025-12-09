prestapy — PrestaShop Webservice client (Python)

### Overview
`prestapy` is a small Python library and CLI that helps you interact with a PrestaShop store via the Webservice API. It provides simple wrappers around common endpoints (brands/manufacturers, products, categories, features, stock) and a Click-based command-line interface for quick tasks.

The project is work-in-progress. Expect breaking changes and a few TODOs noted below.

### Stack
- Language: Python 3.11
- Package manager/build: Poetry
- Runtime deps: `requests`, `click`
- Test deps: `pytest`, `requests-mock`
- CLI entry point: `prestapy` (exposed by Poetry script)

### Requirements
- Python 3.11+
- Poetry (recommended) or pip
- A PrestaShop instance with Webservice enabled and an API key

### Installation

- Using Poetry (recommended for development):
  - Clone the repo
  - Install deps
    ```bash
    poetry install
    ```
  - Activate the virtualenv for shell usage
    ```bash
    poetry shell
    ```

- Using pip (library usage)
  - From the project root (or after publishing to PyPI in the future):
    ```bash
    pip install .
    ```

### Configuration (Environment Variables)
The library and CLI use environment variables for configuration. Note there is an inconsistency between the CLI and the core classes; both variants are listed here. Passing values explicitly to classes avoids env usage.

- Base URL of your shop
  - CLI expects: `URL`
  - Core classes default to: `BASE_URL`
  - Value example: `https://yourshop.example.com/` (include trailing slash — see TODO below)

- API key
  - CLI expects: `API_KEY`
  - Core classes default to: `PSAPI_KEY`

- Output format
  - `DEFAULT_OUTPUT_FORMAT` — currently only `JSON` is supported; defaults to `JSON`.

Example export for the CLI
```bash
export URL="https://yourshop.example.com/"
export API_KEY="<your-prestashop-webservice-key>"
```

Example export for library defaults
```bash
export BASE_URL="https://yourshop.example.com/"
export PSAPI_KEY="<your-prestashop-webservice-key>"
export DEFAULT_OUTPUT_FORMAT=JSON
```

### CLI Usage
The CLI is implemented with Click and exposed as the `prestapy` command.

- See help
  ```bash
  prestapy --help
  ```

- Brand commands
  - List brands for the configured shop
    ```bash
    prestapy brand brand-list
    ```

Notes
- The command names derive from function names; underscores become dashes (e.g., `brand_list` => `brand-list`).
- The CLI currently supports only the `brand` group with the `brand-list` command.

### Library Usage (Python)
You can use the endpoint classes directly.

Basic examples
```python
from prestapy.prestashop_ep.brands import Brand

# Pass URL and API key explicitly (recommended to avoid env var confusion)
b = Brand(base_url="https://yourshop.example.com/", api_key="<api-key>")

# Get active manufacturers as a dict {id: name}
active = b.get_active()

# Fetch products for a specific brand
products = b.get_products(
    "COMETE GIOIELLI",
    full_info=True,      # include detailed product info
    in_stock=True,       # filter to products that have stock
    without_images=False # filter to products without images when True
)
print(len(products))
```

Other available endpoint classes
- `prestapy.prestashop_ep.product.Product`
- `prestapy.prestashop_ep.category.Category`
- `prestapy.prestashop_ep.feature.Feature`
- `prestapy.prestashop_ep.feature.FeatureValue`
- `prestapy.prestashop_ep.stock.Stock` (see notes/TODOs)

### Scripts and Entry Points
- Poetry script: `prestapy = prestapy.cli:cli` (see `pyproject.toml`)
- Run via Poetry
  ```bash
  poetry run prestapy --help
  ```

### Running Tests
Pytest is configured as a test dependency.

Commands
```bash
poetry run pytest -q
```

Important notes
- Some tests appear to be integration-like and may require a live PrestaShop instance and valid credentials via env vars. If not configured, they will fail or hang.
- There is at least one stale test file referencing non-existent functions:
  - `tests/test_ps_endpoint.py` imports `get_manufacturers` from `brands.py` and `get_full_info` from `product.py` — these functions do not exist. The API is class-based. See TODOs below.

### Project Structure
```
prestapy/
├── prestapy/
│   ├── __init__.py
│   ├── cli.py                      # Click CLI entry group and commands
│   └── prestashop_ep/
│       ├── __init__.py
│       ├── base.py                 # Core PsWebService and EndPointEnum
│       ├── brands.py               # Brand (manufacturer) utilities
│       ├── category.py             # Category wrapper
│       ├── feature.py              # Feature and FeatureValue wrappers
│       ├── product.py              # Product wrapper and helpers
│       └── stock.py                # Stock wrapper (see notes)
├── tests/
│   ├── __init__.py
│   ├── test_brands.py
│   ├── test_features.py
│   ├── test_product.py
│   └── test_ps_endpoint.py         # Stale references — see TODO
├── pyproject.toml                  # Poetry config and scripts
├── poetry.lock
└── README.md
```

### Known Limitations and TODOs
- Env var inconsistency
  - CLI uses `URL` and `API_KEY` while core classes default to `BASE_URL` and `PSAPI_KEY`. Unify these or clearly document precedence.

- Base URL formatting
  - `PsWebService.get_all` builds the URL as `f"{self._url}api/{endpoint}"` (missing `/`), while `get_single` uses `f"{self._url}/api/{endpoint}/{id}``.
  - Workaround: include a trailing slash in `BASE_URL`/`URL` (e.g., `https://example.com/`).
  - TODO: normalize base URL and path joining within the library.

- Tests
  - `tests/test_ps_endpoint.py` references missing functions; refactor to use classes (`Brand`, `Product`) or delete if obsolete.
  - Consider adding proper unit tests with `requests-mock` instead of live calls to PrestaShop.

- Features
  - CLI is minimal; extend with more commands (e.g., products, categories, stock queries) mapping to the existing classes.
  - Implement create/update/delete operations in `PsWebService` where currently stubbed.

### License
No license file found in the repository.

- TODO: Add a license (e.g., MIT, Apache-2.0) to clarify usage terms.

### Changelog
- 0.2.0 — Current version per `pyproject.toml`.
