# ATS job boards list: companies on Greenhouse, Lever, Ashby, Workable, SmartRecruiters, Recruitee and Personio

A list of the 700 largest company job boards on seven applicant tracking systems, with the board token, the number of open jobs and the public API endpoint for each. Every board was checked with a live request. Snapshot: November 2026.

Use it to find which ATS a company uses, to seed a job aggregator, or as a starting list for scraping company career pages.

| Platform | Boards in this repo | Open jobs on them | File |
|---|---|---|---|
| Greenhouse | 100 | 77,016 | [data/greenhouse.csv](data/greenhouse.csv) |
| Lever | 100 | 42,883 | [data/lever.csv](data/lever.csv) |
| Ashby | 100 | 20,578 | [data/ashby.csv](data/ashby.csv) |
| SmartRecruiters | 100 | 126,512 | [data/smartrecruiters.csv](data/smartrecruiters.csv) |
| Recruitee | 100 | 25,689 | [data/recruitee.csv](data/recruitee.csv) |
| Personio | 100 | 8,274 | [data/personio.csv](data/personio.csv) |
| Workable | 100 | 12,141 | [data/workable.csv](data/workable.csv) |

Everything in one file: [data/all.csv](data/all.csv). Columns: `platform`, `token`, `open_jobs`, `board_url`, `api_url`.

These are the 100 largest boards per platform, 313,000 open jobs between them. The full directory has 20,000+ boards and is built into the [ATS Jobs Scraper](https://apify.com/picdev/ats-jobs-scraper-greenhouse-lever-ashby-workable) on Apify, which searches all of them by keyword, location, salary and date.

## Public job board APIs, by ATS

A walkthrough with working Python code for Greenhouse, Lever and Ashby: [Greenhouse, Lever and Ashby have public job APIs. Here is how to read them in Python](https://dev.to/picdev/greenhouse-lever-and-ashby-have-public-job-apis-here-is-how-to-read-them-in-python-4lpb).

All seven platforms publish job postings through an endpoint that needs no key and no login. Replace `{token}` with the value from the `token` column.

| ATS | Endpoint | Format |
|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true` | JSON, `jobs[]` |
| Lever | `https://api.lever.co/v0/postings/{token}?mode=json` | JSON array |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{token}?includeCompensation=true` | JSON, `jobs[]` |
| Workable | `https://apply.workable.com/api/v1/widget/accounts/{token}` | JSON, `jobs[]` |
| SmartRecruiters | `https://api.smartrecruiters.com/v1/companies/{token}/postings?limit=100&offset=0` | JSON, `content[]`, paginated |
| Recruitee | `https://{token}.recruitee.com/api/offers/` | JSON, `offers[]` |
| Personio | `https://{token}.jobs.personio.de/xml?language=en` | XML |

Things that differ between them and will cost you time:

- **Salary.** Ashby, Lever and Recruitee have a structured salary field when the employer fills it in. Greenhouse, Workable, SmartRecruiters and Personio do not: the range is in the description text, if anywhere.
- **Remote.** Ashby and Lever have `workplaceType`, Workable has `telecommuting`, SmartRecruiters has `location.remote`, Recruitee has `remote` and `hybrid` flags. Greenhouse has only the location string.
- **Descriptions.** Greenhouse returns HTML-escaped HTML. SmartRecruiters needs a second request per posting for the full description.
- **Pagination.** Only SmartRecruiters paginates. The others return the whole board in one response.
- **Rate limits.** Workable returns 429 quickly. Space the requests out.

[examples/direct_api.py](examples/direct_api.py) reads these endpoints for the boards in a CSV file and prints job counts. It uses no third-party service.

## One schema for all seven: the Apify Actor

If you want the jobs and not the plumbing, the [ATS Jobs Scraper](https://apify.com/picdev/ats-jobs-scraper-greenhouse-lever-ashby-workable) reads all seven platforms and returns one schema: title, company, department, locations, country, remote flag, salary range with currency and period, publish date, apply URL and the full description. It costs $2 per 1,000 jobs, and companies that are not found cost nothing. Apify's free plan includes $5 of monthly credit.

```bash
export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations

# every open job at these companies, as CSV
python3 examples/jobs.py stripe lever:spotify https://jobs.ashbyhq.com/ramp

# search the whole directory: remote data engineering jobs with a salary, posted this week
python3 examples/jobs.py --search "data engineer" --remote --salary --days 7
```

The examples need Python 3.9+ or Node 18+ and no packages:

- [examples/jobs.py](examples/jobs.py): company jobs or directory search to CSV
- [examples/jobs.mjs](examples/jobs.mjs): the same call from Node
- [examples/curl.sh](examples/curl.sh): one curl command

Sample record:

```json
{
  "id": "ashby:ramp:220e674a-fc70-439f-bacf-687553ca59c9",
  "platform": "ashby",
  "companyToken": "ramp",
  "companyName": "Ramp",
  "title": "Solutions Consultant, Commercial",
  "department": "Sales",
  "team": "Solutions Consulting",
  "location": "Remote (US); Remote (Canada); San Francisco, CA; New York, NY (HQ); Toronto, ON; Miami, FL",
  "countryCode": "US",
  "remote": true,
  "workplaceType": "REMOTE",
  "employmentType": "FullTime",
  "salaryMin": 119000,
  "salaryMax": 189000,
  "salaryCurrency": "USD",
  "salaryPeriod": "YEAR",
  "salaryText": "$119K - $189K",
  "salarySource": "ats",
  "publishedAt": "2026-11-25T20:23:25+00:00",
  "url": "https://jobs.ashbyhq.com/ramp/220e674a-fc70-439f-bacf-687553ca59c9"
}
```

## What people build with it

- **Job boards and aggregators**: backfill a niche board from company career pages, deduplicated by a stable job ID.
- **Hiring signals for sales**: a company that opens five data roles in a week is about to buy data tooling.
- **Salary benchmarks**: published ranges by title, location and company.
- **Job alerts**: a daily run with `postedWithinDays: 1` returns only new openings.

## Notes on the data

- `open_jobs` is the count on the day the board was checked. Boards open and close; expect a few percent to be gone a month later.
- SmartRecruiters counts are capped at 2,000 per company in this list.
- Tokens are case-sensitive on Ashby and SmartRecruiters.
- Workday, iCIMS and SuccessFactors are not covered.

## License

The CSV files are released under CC0. The code is MIT.
