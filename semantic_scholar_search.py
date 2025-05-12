import requests
import csv
import time

SEARCH_TERMS = ["", ""]
MAX_RESULTS_PER_TERM = 20  # Adjust up to 100 per term
OUTPUT_FILE = "semantic_search_results.csv"

API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,year,venue,authors.name,authors.affiliations"

HEADERS = {
    "User-Agent": "Academic Project (mailto:your_email@example.com)"
}

def search_semantic_scholar(query, limit=20, sleep_time=5):
    results = []
    offset = 0

    while len(results) < limit:
        params = {
            "query": query,
            "limit": min(100, limit - len(results)),
            "offset": offset,
            "fields": FIELDS
        }

        try:
            response = requests.get(API_URL, params=params, headers=HEADERS)
            if response.status_code == 429:
                print("Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                continue
            elif response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
                break

            data = response.json()
            if not data.get("data"):
                break

            results.extend(data["data"])
            offset += len(data["data"])
            print(f"Fetched {len(results)} of {limit} results for '{query}'")

            # Sleep between each request
            time.sleep(sleep_time)

        except Exception as e:
            print(f"Exception during request: {e}")
            break

    return results

def parse_results(raw_results):
    parsed = []
    for item in raw_results:
        title = item.get("title", "")
        year = item.get("year", "")
        venue = item.get("venue", "")
        authors = item.get("authors", [])

        author_lines = []
        for a in authors:
            name = a.get("name", "")
            affs = a.get("affiliations", [])
            author_id = a.get("authorId")
            aff_str = "; ".join(affs) if affs else "N/A"
            profile_url = f"https://www.semanticscholar.org/author/{author_id}" if author_id else "N/A"
            author_lines.append(f"{name} ({aff_str}) [{profile_url}]")

        parsed.append({
            "title": title,
            "authors": "; ".join(author_lines),
            "year": year,
            "journal": venue
        })
    return parsed

def main():
    all_results = []
    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        raw = search_semantic_scholar(term, MAX_RESULTS_PER_TERM)
        parsed = parse_results(raw)
        all_results.extend(parsed)

    with open(OUTPUT_FILE, "w", newline='', encoding='utf-8') as f:
        fieldnames = ["title", "authors", "year", "journal"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in all_results:
            writer.writerow(entry)

    print(f"Done! {len(all_results)} results saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
