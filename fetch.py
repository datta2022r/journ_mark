"""Fetch recent articles from top marketing journals via OpenAlex (free, no key)."""
import json, re, datetime, requests

MAILTO = "datta2022r@gmail.com"   # <- put your email: gives you OpenAlex's faster "polite" pool
DAYS_BACK = 120               # how far back to look
KEEP_DAYS = 365             # drop articles older than this from the feed

# Check these against the current ABDC list. Edit freely.
JOURNALS = [
    "Journal of Marketing",
    "Journal of Marketing Research",
    "Journal of Consumer Research",
    "Marketing Science",
    "Journal of the Academy of Marketing Science",
    "International Journal of Research in Marketing",
    "Journal of Retailing",
    "Journal of Consumer Psychology",
    "Journal of Service Research",
    "Journal of Interactive Marketing",
    "Journal of Advertising",
    "Journal of Product Innovation Management",
]

BASE = "https://api.openalex.org"

def get(path, **params):
    params["mailto"] = MAILTO
    r = requests.get(f"{BASE}/{path}", params=params, timeout=60)
    r.raise_for_status()
    return r.json()

def source_id(name):
    res = get("sources", search=name, **{"per-page": 5})["results"]
    if not res:
        print(f"!! no match for {name}"); return None
    exact = [s for s in res if s["display_name"].lower() == name.lower()]
    s = (exact or res)[0]
    flag = "" if exact else "   <-- not an exact match, check it"
    print(f"{name} -> {s['display_name']}{flag}")
    return s["id"].split("/")[-1]

def abstract(inv):
    if not inv: return ""
    words = {p: w for w, ps in inv.items() for p in ps}
    text = " ".join(words[i] for i in sorted(words))
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        old = {a["id"]: a for a in json.load(open("articles.json")) if not a["id"].startswith("sample")}
    except Exception:
        old = {}

    ids = "|".join(i for i in (source_id(j) for j in JOURNALS) if i)
    since = (now - datetime.timedelta(days=DAYS_BACK)).date().isoformat()
    flt = f"primary_location.source.id:{ids},from_publication_date:{since},type:article"

    results, page = [], 1
    while page <= 5:
        d = get("works", filter=flt, sort="publication_date:desc", **{"per-page": 200, "page": page})
        results += d["results"]
        if len(d["results"]) < 200: break
        page += 1

    for w in results:
        wid = w["id"].split("/")[-1]
        src = (w.get("primary_location") or {}).get("source") or {}
        prev = old.get(wid, {})
        old[wid] = {
            "id": wid,
            "title": w.get("title") or "Untitled",
            "journal": src.get("display_name", ""),
            "date": w.get("publication_date", ""),
            "abstract": abstract(w.get("abstract_inverted_index")),
            "url": w.get("doi") or w["id"],
            "first_seen": prev.get("first_seen", now_iso),
        }

    cutoff = (now - datetime.timedelta(days=KEEP_DAYS)).date().isoformat()
    out = sorted((a for a in old.values() if a["date"] >= cutoff), key=lambda a: a["date"], reverse=True)
    json.dump(out, open("articles.json", "w"), indent=1, ensure_ascii=False)
    print(f"Saved {len(out)} articles")

if __name__ == "__main__":
    main()
