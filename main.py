from playwright.sync_api import sync_playwright
import os
import sys
import time

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
AUTH_FILE = "linkedin_auth.json"
JOB_KEYWORD = ["Software Engineer", "Senior Software Engineer"]
easy_apply_jobs = []

def scroll_and_collect_jobs(page, max_jobs=10):
    """
    Function to scroll down the page and collect job links.
    
    Args:
        page (Page): The Playwright page object.
        max_jobs (int): The maximum number of job links to collect.
        
    Returns:
        list: A list of job links.
    """
    job_links = set()
    last_height = page.evaluate("document.body.scrollHeight")
    
    while len(job_links) < max_jobs:
        # Collect job cards
        job_cards = page.query_selector_all("ul.jobs-search-results__list li div.base-card")
        for card in job_cards:
            try:
                # Check for Easy Apply button inside the card
                easy_apply_btn = card.query_selector("button span:has-text('Easy Apply')")
                if easy_apply_btn:
                    link_elem = card.query_selector("a[href*='/jobs/view/']")
                    if link_elem:
                        job_links.add(link_elem.get_attribute("href"))
            except:
                continue  # ignore any weird cards

        # Scroll down
        page.evaluate("window.scrollBy(0, 1000)")
        time.sleep(3)  # human-like delay

        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print(f"✅ Collected {len(job_links)} Easy Apply job links")
    return list(job_links)

def filter_easy_apply_jobs(page, job_links):
    """
    Filter job links to only include those with the Easy Apply button.

    Args:
        page (Page): The Playwright page object.
        job_links (list): A list of job links to filter.

    Returns:
        list: A list of job links with Easy Apply button.
    """
    easy_apply_jobs = []

    for link in job_links:
        if link.startswith("/"):
            link = "https://www.linkedin.com" + link

        page.goto(link)
        page.wait_for_timeout(3000)

        # Job title
        title_elem = page.locator("h1.top-card-layout__title")
        job_title = title_elem.inner_text().strip() if title_elem.count() > 0 else "UNKNOWN TITLE"

        # Easy Apply button
        easy_apply_btn = page.locator("button:has-text('Easy Apply')")

        if easy_apply_btn.count() > 0:
            print(f"✅ Easy Apply | {job_title}")
            easy_apply_jobs.append({
                "title": job_title,
                "url": link
            })
        else:
            print(f"❌ No Easy Apply | {job_title}")

    return easy_apply_jobs

def collect_job_links(page, max_jobs=25):
    """
    Collect job links from the page.

    Args:
        page (Page): The Playwright page object.
        max_jobs (int): The maximum number of job links to collect.

    Returns:
        list: A list of job links.
    """
    page.wait_for_selector("a[href*='/jobs/view/']")

    links = set()
    cards = page.locator("a[href*='/jobs/view/']")

    for i in range(min(cards.count(), max_jobs)):
        href = cards.nth(i).get_attribute("href")
        if href:
            links.add(href.split("?")[0])

    print(f"🔗 Collected {len(links)} job links")
    return list(links)

def main():
    """
    Main function to run the script.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=BRAVE_PATH,
            headless=False,
            args=["--start-maximized"]
        )

        context = None
        page = None

        try:
            # Try loading existing session
            if os.path.exists(AUTH_FILE):
                context = browser.new_context(storage_state=AUTH_FILE)
                print("Using saved LinkedIn session")
            else:
                # No session found → manual login
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://www.linkedin.com/")
                print("Waiting 60s for manual login...")
                page.wait_for_timeout(60000)  # give user time to log in
                context.storage_state(path=AUTH_FILE)
                print("LinkedIn session saved")

            # If page was not already created, create now
            if page is None:
                page = context.new_page()

            # Navigate to Jobs page with Easy Apply filter
            # and collect job links
            for kw in JOB_KEYWORD:
                search_url = f"https://www.linkedin.com/jobs/search/?keywords={kw}&f_LF=f_AL"
                page.goto(search_url)
                time.sleep(5)
                job_links = collect_job_links(page, max_jobs=30)
                easy_apply_jobs = filter_easy_apply_jobs(page, job_links)

                print("🎯 Final Easy Apply jobs:")
                print(easy_apply_jobs)

            print("All jobs collected", easy_apply_jobs)

        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

        finally:
            if page is not None:
                page.close()
            if context is not None:
                context.close()
            browser.close()

if __name__ == "__main__":
    main()