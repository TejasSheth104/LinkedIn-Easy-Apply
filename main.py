# main.py

from browser.session import create_browser_and_page
from config.settings import JOB_KEYWORDS, MAX_JOBS_PER_KEYWORD
from jobs.collector import collect_job_links
from jobs.filters import filter_easy_apply_jobs
from apply.easy_apply import click_easy_apply_and_classify

def main():
    p, browser, context, page = create_browser_and_page()

    all_easy_apply_jobs = []

    try:
        for kw in JOB_KEYWORDS:
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={kw}&f_LF=f_AL"
            page.goto(search_url)
            page.wait_for_timeout(5000)

            job_links = collect_job_links(page, MAX_JOBS_PER_KEYWORD)
            easy_apply_jobs = filter_easy_apply_jobs(page, job_links)

            all_easy_apply_jobs.extend(easy_apply_jobs)

        print("\n🎯 FINAL EASY APPLY JOBS")
        for job in all_easy_apply_jobs:
            print(f"- {job['title']}")

        if all_easy_apply_jobs:
            page.goto(all_easy_apply_jobs[0]["url"])
            result = click_easy_apply_and_classify(page)
            print(f"\n🧠 Application type: {result}")

    finally:
        page.close()
        context.close()
        browser.close()
        p.stop()

if __name__ == "__main__":
    main()