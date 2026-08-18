import os
import requests


APIFY_API_URL = (
    "https://api.apify.com/v2/acts/"
    "valig~naukri-jobs-scraper/"
    "run-sync-get-dataset-items"
)


def fetch_jobs():
    token = os.getenv("APIFY_API_TOKEN")

    if not token:
        raise ValueError("APIFY_API_TOKEN is missing")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "title": "DevOps Engineer",
        "location": "India",
        "sortBy": "f",
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

    if response.status_code != 200:
        raise RuntimeError(
            f"Apify API error: "
            f"{response.status_code} - {response.text}"
        )

    jobs = response.json()

    print(f"Fetched {len(jobs)} jobs from Naukri")

    return jobs
