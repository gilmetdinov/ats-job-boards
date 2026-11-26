"""Jobs from company career sites in one schema, saved to CSV.

    export APIFY_TOKEN=...            # https://console.apify.com/settings/integrations
    python3 jobs.py stripe lever:spotify https://jobs.ashbyhq.com/ramp
    python3 jobs.py --search "data engineer" --remote --days 7
"""
import argparse, csv, sys
from apify_run import run_actor

ACTOR = "picdev~ats-jobs-scraper-greenhouse-lever-ashby-workable"
COLUMNS = ["companyName", "title", "location", "remote", "salaryMin", "salaryMax",
           "salaryCurrency", "publishedAt", "platform", "url"]

p = argparse.ArgumentParser()
p.add_argument("companies", nargs="*", help="company names, platform:token or career page URLs")
p.add_argument("--search", action="append", default=[], help="keyword in the job title (repeatable)")
p.add_argument("--remote", action="store_true")
p.add_argument("--salary", action="store_true", help="only jobs with a published salary")
p.add_argument("--days", type=int, help="posted within N days")
p.add_argument("--max", type=int, default=100)
a = p.parse_args()

run_input = {"maxItems": a.max, "includeDescription": False}
if a.companies:
    run_input["companies"] = a.companies
if a.search:
    run_input["keywords"] = a.search
if a.remote:
    run_input["remoteOnly"] = True
if a.salary:
    run_input["withSalaryOnly"] = True
if a.days:
    run_input["postedWithinDays"] = a.days

jobs = run_actor(ACTOR, run_input)
w = csv.DictWriter(sys.stdout, fieldnames=COLUMNS, extrasaction="ignore")
w.writeheader()
w.writerows(jobs)
print(f"{len(jobs)} jobs", file=sys.stderr)
