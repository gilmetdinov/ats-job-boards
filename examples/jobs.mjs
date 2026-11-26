// Jobs from company career sites in one schema. Node 18+, no dependencies.
//   APIFY_TOKEN=... node jobs.mjs stripe lever:spotify
const ACTOR = 'picdev~ats-jobs-scraper-greenhouse-lever-ashby-workable';
const companies = process.argv.slice(2);

const res = await fetch(`https://api.apify.com/v2/acts/${ACTOR}/run-sync-get-dataset-items`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.APIFY_TOKEN}`,
  },
  body: JSON.stringify({
    companies: companies.length ? companies : ['stripe'],
    maxItems: 50,
    includeDescription: false,
  }),
});
if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);

for (const job of await res.json()) {
  const pay = job.salaryMin ? ` | ${job.salaryMin}-${job.salaryMax} ${job.salaryCurrency}` : '';
  console.log(`${job.companyName} | ${job.title} | ${job.location ?? ''}${pay} | ${job.url}`);
}
