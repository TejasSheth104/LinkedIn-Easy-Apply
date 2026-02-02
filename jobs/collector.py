# jobs/collector.py

def collect_job_links(page, max_jobs):
    page.wait_for_selector("a[href*='/jobs/view/']")

    links = set()
    cards = page.locator("a[href*='/jobs/view/']")

    for i in range(min(cards.count(), max_jobs)):
        href = cards.nth(i).get_attribute("href")
        if href:
            links.add(href.split("?")[0])

    print(f"🔗 Collected {len(links)} job links")
    return list(links)
