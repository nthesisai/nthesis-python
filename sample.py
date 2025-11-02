import os
import arxiv
from nthesis import Nthesis, ConflictError

base_url = os.getenv("NTHESIS_BASE_URL", "https://nthesis.ai")
api_key = os.getenv("NTHESIS_API_KEY")

client = Nthesis(base_url, api_key)
stores = client.list_stores(timeout=10)
for s in stores:
    print(f"{s.name}")

# Use the store's UUID id (not the human name)
store = client.resolve_store("testing")
search = arxiv.Search(
    query="machine learning AND cat:cs.LG",
    max_results=10,
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
        print('conflict - skipping')
