from fetch_jobs import fetch_jobs
from filter_jobs import filter_jobs

from duplicate_jobs import (
    load_sent_jobs,
    filter_new_jobs,
    get_job_key,
    save_sent_jobs,
)

from telegram import send_telegram_message


def format_job_message(job):
    title = job.get("title", "N/A")
    
    company = job.get("company", {})
    company_name = company.get("name", "N/A")

    experience = job.get("experience", {})
    experience_text = experience.get("text", "N/A")

    url = job.get("url", "N/A")

    description = job.get("description", {})

    if isinstance(description, dict):
        description_text = description.get("short", "")
        
        if not description_text:
            description_text = description.get("full", "")
    else:
        description_text = str(description)

    # Remove HTML tags
    import re
    description_text = re.sub(
        r"<[^>]+>",
        " ",
        description_text
    )

    # Remove extra spaces
    description_text = re.sub(
        r"\s+",
        " ",
        description_text
    ).strip()

    # Keep Telegram message short
    if len(description_text) > 500:
        description_text = description_text[:500] + "..."

    message = (
        "🚨 NEW DEVOPS JOB\n\n"
        f"💼 {title}\n"
        f"🏢 {company_name}\n"
        f"🎯 Experience: {experience_text}\n\n"
        f"📝 {description_text}\n\n"
        f"🔗 Apply:\n{url}\n\n"
        "────────────────────\n"
        "🤖 Naukri Job Bot"
    )

    return message


def main():
    # 1. Fetch jobs from Naukri
    jobs = fetch_jobs()

    # 2. Apply DevOps + experience + location filters
    relevant_jobs = filter_jobs(jobs)

    # 3. Load jobs already sent in previous runs
    sent_jobs = load_sent_jobs()

    # 4. Keep only new jobs
    new_jobs = filter_new_jobs(
        relevant_jobs,
        sent_jobs
    )

    print(
        f"New jobs ready for Telegram: "
        f"{len(new_jobs)}"
    )

    # 5. Send each new job to Telegram
    for job in new_jobs:

        message = format_job_message(job)

        print(
            f"\nSending job: "
            f"{job.get('title')}"
        )

        send_telegram_message(message)

        # 6. Save only after Telegram succeeds
        job_key = get_job_key(job)

        if job_key:
            sent_jobs.add(job_key)

    # 7. Save updated history
    save_sent_jobs(sent_jobs)

    print(
        f"\nSaved {len(sent_jobs)} total sent jobs "
        "to sent_jobs.json"
    )


if __name__ == "__main__":
    main()
