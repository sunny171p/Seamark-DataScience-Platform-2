# Case study: Seamark Global Innovations, Projects 1 and 2

Author: Sunday Emmanuel Azeez

This is the real story behind the two Seamark projects in this GitHub account, written for anyone who wants more context than a README gives: a recruiter, an award or endorsement reviewer, or just someone deciding whether to fork the code. Every number and event here is real. Where something was found wrong, or actually broke, that's included too, since that's a more honest signal of the work than a project that only ever shows the finished, working version.

## The store, and why two projects

Seamark Global Innovations is a real Shopify store. Project 1 started before it had taken a single order: the job was to audit the catalog and pricing, look at whatever traffic data existed, and build a forecasting model ready to run the moment real sales began. Project 2 picks up after the store actually launched, once there was real order history to check the earlier work against.

## What Project 1 found

The catalog audit checked every product's "compare at" price against its actual price, the two numbers that together decide whether a "sale" badge is real. About 95.6% of price-checked products had a discount the pricing data didn't support. That's not a rounding error, it's most of the catalog. Finding that before a single customer had a chance to notice it was the whole point of doing the audit pre-launch.

The forecasting side used Prophet, trained on a synthetic order series, since there was no real sales history yet to train on. That's stated plainly in Project 1's own documentation rather than left implied, because a forecast trained on made-up data presented as if it were real would be the kind of thing this whole project is built to avoid.

## What Project 2 validated, and what it found once real data existed

Project 2 re-ran the same category of checks against real orders instead of a pre-launch snapshot, and added a few things Project 1 didn't have: a bot-traffic adjustment so the funnel numbers reflect real visitors, a catalog-vs-sales-mix comparison, and a live sync straight from Shopify's API instead of a one-time manual export.

Getting live data flowing wasn't clean on the first attempt. Shopify's newer app-creation flow only hands out a Client ID and Secret, not the older-style permanent access token the sync script originally expected, so the script needed a second path added: exchanging that Client ID and Secret for a temporary token itself, each run. Once real data started flowing, two pipeline stages broke immediately, because the automated export was missing two columns (Payment Method and Variant SKU) that a manual Shopify export includes but the API call hadn't originally asked for. Both were straightforward once diagnosed. A third bug was subtler: after adding the Variant SKU field, the pipeline suddenly matched only 6 of 11 real order line items to a product, down from all 11 before. The cause turned out to be that the sync only fetched each product's first variant, so an order placed against a different size or color had no matching SKU in the export at all. The fix was to fetch every variant per product and lay the export out the same way Shopify's own manual export does, one row per variant. After that, the pipeline matched all 11 line items again, and the category percentages it produced lined up exactly with the numbers an earlier manual audit had already confirmed by hand.

## The mistake that mattered most

At one point, real customer names and emails ended up committed to this repository's git history, both in the raw Shopify export and in a derived cleaned file. This wasn't caught by a tool, it was caught by asking the question directly: does this repo, which is public, actually contain real customer data. It did. The fix was `.gitignore` entries for both the raw and derived files, `git rm --cached` to untrack them, and since the repository's history was short enough to do safely, amending and force-pushing to remove them from history rather than just going forward clean from that point on. That happened twice, once for the raw export, once for the derived file that carried the same data forward. Both are now confirmed absent from the repo's full history, not just the current commit.

## Two bugs in the screenshot automation, since they're a good example of debugging methodology

Building an automated full-page screenshot tool for the dashboard hit two separate real bugs, each fixed by figuring out the actual mechanism rather than guessing. The first: the script would silently produce zero screenshots, because it was waiting for the browser's network activity to go fully idle before proceeding, and Streamlit keeps a permanent websocket connection open for live updates, so the network never actually goes idle. Waiting on the page's load event instead of network idle fixed it. The second, found only by checking the actual pixel dimensions of the output files rather than trusting that "full page" meant what it said: every screenshot came back at exactly the browser's viewport size, because Streamlit renders its content inside its own internally-scrolling container, not the page's real body, so a standard full-page screenshot, which measures the real document, never saw past one screen. The fix measures that inner container's real height directly and resizes the browser viewport to match before capturing.

## What this adds up to

A real business had a real pricing-integrity problem that got caught before launch. A real customer-data mistake got caught and actually removed from a public repository's history, not just patched going forward. A handful of real bugs, in the Shopify sync, in the screenshot automation, got diagnosed by finding the actual mechanism rather than working around the symptom, each one verified fixed before being called done. None of that is dramatic on its own. Together, it's a more honest description of what building something real actually looks like than a project that only shows the parts that worked on the first try.
