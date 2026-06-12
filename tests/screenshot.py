from playwright.sync_api import sync_playwright
import random

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto("http://127.0.0.1:5000")
    page.wait_for_load_state("networkidle")
    page.fill("#project_name", "Wavestone Brand Test")
    rng = random.Random(42)
    for sel in page.query_selector_all("select.js-answer"):
        sel.select_option(rng.choice(["voll", "voll", "voll", "teil"]))
    with ctx.expect_page() as p:
        page.locator("button[formaction*='report/html']").click()
    rp = p.value
    rp.wait_for_load_state("networkidle")
    rp.screenshot(path="tests/report_preview.png", full_page=True)
    # Also screenshot the questionnaire
    page.screenshot(path="tests/questionnaire_preview.png", full_page=False)
    browser.close()
    print("Screenshots gespeichert")
