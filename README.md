# SemanticScholarSearch

This script uses the [Semantic Scholar API](https://www.semanticscholar.org/product/api) to search for scientific publications within the last 5 years that mention user-provided terms and extracts key metadata about the publications and authors.

---

## Features

- Searches for publications using specific search terms.
- Batches and throttles API requests to comply with rate limits (≤ 500 req/s) (does NOT require an API key!)
- Extracts metadata:
  - Paper title
  - Publication year
  - Journal name
  - Authors (with affiliations and profile URLs)
- Outputs a structured CSV file with this metadata for further processing.

---

## Requirements

- Python 3.7+
- [Semantic Scholar API key](https://www.semanticscholar.org/product/api#api-key-form)

### Python Packages

Install dependencies with:

```bash
pip install requests
