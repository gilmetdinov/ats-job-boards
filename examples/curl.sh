#!/bin/sh
# All open engineering jobs at three companies, as JSON.
curl -s -X POST \
  "https://api.apify.com/v2/acts/picdev~ats-jobs-scraper-greenhouse-lever-ashby-workable/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companies": ["stripe", "lever:spotify", "https://jobs.ashbyhq.com/ramp"], "keywords": ["engineer"], "maxItems": 50}'
