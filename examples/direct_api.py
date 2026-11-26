"""Read the public ATS APIs yourself, no Apify involved: job counts for boards from data/*.csv.

    python3 direct_api.py ../data/ashby.csv 10

Every platform returns a different shape, so this only counts jobs. Covers the JSON APIs;
Personio publishes XML (see the api_url column).
"""
import csv, json, sys, urllib.request

def count(platform: str, data) -> int:
    if platform in ("greenhouse", "ashby", "workable"):
        return len(data.get("jobs", []))
    if platform == "lever":
        return len(data)
    if platform == "smartrecruiters":
        return data.get("totalFound", len(data.get("content", [])))
    if platform == "recruitee":
        return len(data.get("offers", []))
    raise ValueError(platform)

path, limit = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10
for row in list(csv.DictReader(open(path)))[:limit]:
    if row["platform"] == "personio":
        continue
    req = urllib.request.Request(row["api_url"], headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f'{row["platform"]:16} {row["token"]:32} {count(row["platform"], json.load(r))}')
    except Exception as e:
        print(f'{row["platform"]:16} {row["token"]:32} error: {e}')
