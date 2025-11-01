# nthesis (Python client)

A small / ingest focused Python client for the nthesis API.

## Install

- Editable install for local dev: `pip install -e .`
- Build a wheel/sdist: `python -m build` (requires `pip install build`)

## Usage

```py
import os
import arxiv
from nthesis import Nthesis
from nthesis.nthesis import ConflictError

api_key = os.getenv("NTHESIS_API_KEY")

client = Nthesis(base_url, api_key)

# Use the store's UUID id (not the human name)
store = client.resolve_store("example")
search = arxiv.Search(
    query="machine learning AND cat:cs.LG",
    max_results=50,
)

# Use the arXiv Client for reliable iteration
arxiv_client = arxiv.Client()
for result in arxiv_client.results(search):
    summary = result.summary.strip()
    content = f'{summary}\n{result.pdf_url}'
    try:
        res = client.add_item(store.id, content)
        print(res.hash)
    except ConflictError:
    # Content in Nthesis is indexed by hash. Catching ConflictError
    # allows you to skip duplicates when progressively loading data
        print('summary exists - skipping')
```

