# utils/helpers.py

def get_job_title(page):
    selectors = [
        "h1.top-card-layout__title",
        "h1.jobs-unified-top-card__job-title",
        "h1",
        "title"
    ]

    for sel in selectors:
        loc = page.locator(sel)
        if loc.count() > 0:
            try:
                text = loc.first.inner_text().strip()
                if text and "LinkedIn" not in text:
                    return text
            except:
                pass

    return "UNKNOWN TITLE"