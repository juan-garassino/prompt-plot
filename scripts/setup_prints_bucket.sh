#!/usr/bin/env bash
# The public bucket the portfolio site reads printed plates from.
#
# Idempotent: re-running it re-applies the public-read binding and the CORS
# policy (scripts/prints_cors.json — the site's prod, www, Firebase prod/staging
# and local origins; GET only). The bucket already exists (created 2026-10-03);
# this is the record of how, and the way to rebuild it.
#
#   bash scripts/setup_prints_bucket.sh
#   BUCKET=other-bucket PROJECT=other-project bash scripts/setup_prints_bucket.sh
#
# Upload with `make prints-export` (scripts/prints_export.py --push).
set -euo pipefail

BUCKET=${BUCKET:-garassino-ai-prints}
PROJECT=${PROJECT:-garassino-ai}

gcloud storage buckets describe "gs://$BUCKET" --project "$PROJECT" >/dev/null 2>&1 \
  || gcloud storage buckets create "gs://$BUCKET" --project "$PROJECT" \
       --location europe-west1 --uniform-bucket-level-access --default-storage-class STANDARD

gcloud storage buckets add-iam-policy-binding "gs://$BUCKET" \
  --member=allUsers --role=roles/storage.objectViewer

gcloud storage buckets update "gs://$BUCKET" --cors-file="$(dirname "$0")/prints_cors.json"

# Acceptance: the catalog answers a cross-origin GET with CORS + cache headers.
# A fresh bucket has no catalog yet — that must not fail the script (pipefail).
curl -sI -H "Origin: https://artificial-artifacts.com" \
  "https://storage.googleapis.com/$BUCKET/catalog.json" | grep -iE 'access-control|cache-control' \
  || echo "no catalog yet — run make prints-export, then re-run this to check the headers"
