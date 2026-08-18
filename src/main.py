from fetch_jobs import fetch_jobs
from filter_jobs import filter_jobs


def main():
    jobs = fetch_jobs()

    relevant_jobs = filter_jobs(jobs)

    print("\n========== Relevant Naukri Jobs ==========\n")

    for job in relevant_jobs:

        print(f"ID: {job.get('id')}")
        print(f"Title: {job.get('title')}")

        company = job.get("company", {})
        print(f"Company: {company.get('name')}")

        experience = job.get("experience", {})

        print(
            f"Experience: "
            f"{experience.get('minimum')}-"
            f"{experience.get('maximum')} Yrs"
        )

        print(f"URL: {job.get('url')}")

        # Temporary location debugging
        print(f"Location: {job.get('location')}")
        print(f"Work Mode: {job.get('wfhType')}")
        print(f"Job Location: {job.get('jobLocation')}")

        print("-" * 60)


if __name__ == "__main__":
    main()
