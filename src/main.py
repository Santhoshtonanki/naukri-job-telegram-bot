from fetch_jobs import fetch_jobs


def main():
    jobs = fetch_jobs()

    print("\n========== Naukri Jobs ==========\n")

    for job in jobs:
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

        print("-" * 60)


if __name__ == "__main__":
    main()
