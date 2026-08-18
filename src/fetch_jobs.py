import os
import requests


APIFY_API_URL = (
    "https://api.apify.com/v2/acts/"
    "valig~naukri-jobs-scraper/"
    "run-sync-get-dataset-items"
)


SEARCH_KEYWORDS = [
    "DevOps Engineer",
    "AWS DevOps Engineer",
    "Junior DevOps Engineer",
    "Cloud Engineer",
    "DevOps Associate",
    "Cloud DevOps Engineer",
    "SRE",
    "Site Reliability Engineer",
    "Platform Engineer",
]


def fetch_jobs():
    token = os.getenv("APIFY_API_TOKEN")

    if not token:
        raise ValueError("APIFY_API_TOKEN is missing")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    all_jobs = []

    for keyword in SEARCH_KEYWORDS:

        print(f"\nSearching Naukri for: {keyword}")

        payload = {
            "title": keyword,
            "location": "India",
            "sortBy": "date",
            "freshness": "1",
            "resultsLimit": 10
        }

        params = {
            "format": "json",
            "clean": "true",
            "limit": 10,
            "maxTotalChargeUsd": 0.10
        }

        response = requests.post(
            APIFY_API_URL,
            headers=headers,
            params=params,
            json=payload,
            timeout=300
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Apify API error for '{keyword}': "
                f"{response.status_code} - {response.text}"
            )

        jobs = response.json()

        print(
            f"Fetched {len(jobs)} jobs "
            f"for '{keyword}'"
        )

        all_jobs.extend(jobs)

    print(
        f"\nTotal jobs fetched before "
        f"duplicate removal: {len(all_jobs)}"
    )

    # Remove duplicates from multiple searches.
    unique_jobs = []
    seen_jobs = set()

    for job in all_jobs:

        job_id = job.get("id")
        job_url = job.get("url")

        # Prefer Naukri Job ID.
        unique_key = job_id or job_url

        if not unique_key:
            continue

        if unique_key in seen_jobs:
            continue

        seen_jobs.add(unique_key)
        unique_jobs.append(job)

    print(
        f"Unique jobs after duplicate removal: "
        f"{len(unique_jobs)}"
    )

    return unique_jobs
