# browser/session.py

import os
from playwright.sync_api import sync_playwright
from config.settings import BRAVE_PATH, AUTH_FILE

def create_browser_and_page():
    p = sync_playwright().start()

    browser = p.chromium.launch(
        executable_path=BRAVE_PATH,
        headless=False,
        args=["--start-maximized"]
    )

    if os.path.exists(AUTH_FILE):
        context = browser.new_context(storage_state=AUTH_FILE)
        print("Using saved LinkedIn session")
    else:
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.linkedin.com/")
        print("Waiting 60s for manual login...")
        page.wait_for_timeout(60000)
        context.storage_state(path=AUTH_FILE)
        print("LinkedIn session saved")

    page = context.new_page()
    return p, browser, context, page
