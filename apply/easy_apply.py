# apply/easy_apply.py

def safe_click_easy_apply(page):
    try:
        btn = page.locator("button:has-text('Easy Apply')").first
        btn.wait_for(state="attached", timeout=8000)
        btn.wait_for(state="visible", timeout=8000)

        if not btn.is_enabled():
            return False

        page.bring_to_front()
        btn.scroll_into_view_if_needed()
        btn.click(timeout=5000)

        page.wait_for_timeout(2000)
        return True

    except:
        return False


def click_easy_apply_and_classify(page):
    if not safe_click_easy_apply(page):
        return "CLICK_FAILED"

    if page.locator("button:has-text('Submit application')").count() > 0:
        return "ONE_CLICK"

    if page.locator("button:has-text('Next')").count() > 0:
        return "MULTI_STEP"

    if page.locator("text=Continue applying").count() > 0:
        return "EXTERNAL"

    return "UNKNOWN"
