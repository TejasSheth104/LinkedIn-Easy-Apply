# jobs/filters.py

from utils.helpers import get_job_title

def filter_easy_apply_jobs(page, job_links):
    easy_apply_jobs = []

    for link in job_links:
        if link.startswith("/"):
            link = "https://www.linkedin.com" + link

        page.goto(link)
        page.wait_for_timeout(3000)

        title = get_job_title(page)

        if page.locator("button:has-text('Easy Apply')").count() > 0:
            print(f"✅ Easy Apply | {title}")
            easy_apply_jobs.append({"title": title, "url": link})
        else:
            print(f"❌ No Easy Apply | {title}")

    return easy_apply_jobs
