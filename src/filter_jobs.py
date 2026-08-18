def get_job_text(job):
    """
    Combine useful job fields into one searchable text.
    """

    description = job.get("description", {})

    if isinstance(description, dict):
        full_description = description.get("full", "")
        short_description = description.get("short", "")
    else:
        full_description = description or ""
        short_description = ""

    return normalize_text(
        " ".join([
            str(job.get("title", "")),
            str(job.get("url", "")),
            str(full_description),
            str(short_description),
        ])
    )


def has_visa_sponsorship(job):
    """
    Detect explicit visa sponsorship / visa support.
    """

    text = get_job_text(job)

    sponsorship_keywords = [
        "visa sponsorship",
        "visa sponsored",
        "visa sponsor",
        "sponsor visa",
        "work visa sponsorship",
        "visa support",
        "sponsorship available",
        "sponsorship provided",
        "visa assistance",
        "relocation and visa",
        "relocation assistance and visa",
    ]

    for keyword in sponsorship_keywords:
        if keyword in text:
            return True

    return False


def is_location_eligible(job):
    """
    Current Naukri Actor is India-focused.

    Therefore:
    - India jobs are allowed.
    - Remote/Hybrid jobs are allowed.
    - Explicit visa sponsorship is checked for
      international-style listings when present.
    """

    wfh_type = str(job.get("wfhType", ""))

    # Office / Remote / Hybrid are all acceptable
    # for the India-focused Naukri search.
    if wfh_type in ["0", "2", "3"]:
        return True

    # If work mode is missing, allow the current
    # India search result rather than rejecting it.
    if not wfh_type or wfh_type == "None":
        return True

    return has_visa_sponsorship(job)
