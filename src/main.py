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

# Temporary location/work-mode debugging
print(f"Location: {job.get('location')}")
print(f"Work Mode: {job.get('wfhType')}")
print(f"Job Location: {job.get('jobLocation')}")

print("-" * 60)
