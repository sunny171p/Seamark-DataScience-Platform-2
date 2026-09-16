# ==
# pipeline.py
# Author: Sunday Emmanuel Azeez
# Seamark Global Innovations — Post-Launch Data Science Project (Project 2)
# ==
#
# WHY THIS EXISTS:
# Same reasoning as Project 1's runner — running each analysis script
# by hand is easy to get out of order, and it's easy to forget a
# stage and look at outputs based on stale data without noticing.
# This has grown the same way Project 1's did, one stage at a time,
# and now runs all ten of Project 2's own stages in order.
#
# HOW TO RUN:
#   python pipeline.py
#
# STAGE ORDER MATTERS:
# Stage 2 depends on Stage 1 having written products_clean.csv.
# Stages 3-6 each depend on Stage 1's cleaned data and/or an earlier
# stage's own output (04 reads Stage 3's funnel_summary.csv; 06 reads
# it too). Stage 7 is independent — it reads the raw UpPromote export
# directly, not any cleaned/output file. The catalogue-vs-sales-mix
# check also depends only on Stage 1's cleaned data plus the raw order
# export — it compares real catalogue mix against real sales mix, no
# simulated data. The external-category-benchmark check (Stage 9)
# depends on the catalogue-vs-sales-mix output (Stage 8) plus the real
# external Olist dataset in raw_data/external_olist/ — it compares
# Seamark's real sales mix against that external dataset's real order
# mix, still no simulated data on either side. 08_pipeline_health.py
# runs LAST on purpose (even though its filename number is lower than
# the other two) because it re-checks the outputs every earlier stage
# just wrote, so it needs all of them to already exist. The run order
# below is what actually controls execution order, not the filename
# numbers.
# ==

import subprocess
import sys
import os
from datetime import datetime

START_TIME = datetime.now()

print("=" * 62)
print("  SEAMARK GLOBAL INNOVATIONS")
print("  Post-Launch Data Science Pipeline (Project 2)")
print(f"  Started: {START_TIME.strftime('%d %B %Y at %H:%M:%S')}")
print("=" * 62)


pipeline_stages = [
    ("01_data_cleaning.py",          "Stage 1 — Data Cleaning (Products, Orders, Customers)"),
    ("02_product_classification.py", "Stage 2 — Product Classification, Country Breakdown & Text Clustering (TF-IDF/K-Means)"),
    ("03_funnel_analysis.py",        "Stage 3 — Funnel Analysis, Bot Traffic Adjustment & Drop-off Scenario"),
    ("04_forecast_vs_actual.py",     "Stage 4 — Forecast Accuracy Check & Capital-Exposure Estimate"),
    ("05_pricing_integrity.py",      "Stage 5 — Pricing Integrity Check & Margin Anomaly Detection"),
    ("06_omnichannel_visibility.py",  "Stage 6 — Omnichannel Visibility (Shopify + Google Merchant Center)"),
    ("07_affiliate_analysis.py",      "Stage 7 — Affiliate Programme Analysis (UpPromote signups)"),
    ("09_catalog_vs_sales_mix.py",    "Stage 8 — Catalogue Mix vs Real Sales Mix (by category)"),
    ("10_external_category_benchmark.py", "Stage 9 — Real Sales Mix vs External (Olist) Real Order Mix"),
    ("08_pipeline_health.py",         "Stage 10 — Pipeline Health Check (launch-readiness gate, runs last)"),
]

ANALYTICS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics")

results = []

for filename, stage_name in pipeline_stages:

    print(f"\n{'─' * 62}")
    print(f"  {stage_name}")
    print(f"  Running: {filename}")
    print(f"{'─' * 62}")

    try:
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=ANALYTICS_DIR,
        )

        if result.returncode == 0:
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    print(f"  {line}")
            print(f"\n  Result: SUCCESS")
            results.append((stage_name, "SUCCESS", None))

        else:
            print(f"\n  Result: FAILED")
            error_snippet = result.stderr[-300:] if result.stderr else "No error output captured"
            print(f"  Error : {error_snippet}")
            if result.stderr and "ModuleNotFoundError" in result.stderr:
                missing_module = result.stderr.strip().split('\n')[-1].split("'")
                missing_module = missing_module[1] if len(missing_module) > 1 else "a required package"
                print(f"\n  Fix   : '{missing_module}' isn't installed in this Python environment.")
                print(f"          Run this from the project root, then try again: pip install -r requirements.txt")
            results.append((stage_name, "FAILED", error_snippet))

    except subprocess.TimeoutExpired:
        print(f"\n  Result: TIMEOUT — exceeded 120 seconds")
        results.append((stage_name, "TIMEOUT", "Exceeded 120 second limit"))

    except Exception as e:
        print(f"\n  Result: ERROR — {str(e)}")
        results.append((stage_name, "ERROR", str(e)))


END_TIME = datetime.now()
DURATION = (END_TIME - START_TIME).seconds

success_count = sum(1 for _, status, _ in results if status == "SUCCESS")
fail_count = len(results) - success_count

print(f"\n\n{'=' * 62}")
print("  PIPELINE SUMMARY")
print(f"{'=' * 62}")

for stage_name, status, error in results:
    status_label = "OK  " if status == "SUCCESS" else "FAIL"
    print(f"  [{status_label}]  {stage_name}")
    if error:
        print(f"         {error[:120]}")

print(f"\n{'─' * 62}")
print(f"  Stages run    : {len(pipeline_stages)}")
print(f"  Successful    : {success_count}")
print(f"  Failed        : {fail_count}")
print(f"  Duration      : {DURATION} seconds")
print(f"  Finished      : {END_TIME.strftime('%d %B %Y at %H:%M:%S')}")
print(f"{'─' * 62}")

if fail_count == 0:
    print("\n  ALL STAGES PASSED")
    print("  Cleaned data  : cleaned_data/")
    print("  CSV/chart out : outputs/")
    print("  Affiliate signups are analysed (Stage 7); real order-level affiliate")
    print("  attribution and live-rate integration still depend on data this store")
    print("  doesn't have yet — see DATA_PROVENANCE.md's 'Known gap' section.")
else:
    print(f"\n  PIPELINE FINISHED WITH {fail_count} FAILURE(S)")
    print("  Common causes:")
    print("  - Missing CSV in raw_data/")
    print("  - Column name changed in latest Shopify export")
    print("  - Run the failed stage individually to see the full error")

print(f"{'=' * 62}\n")
