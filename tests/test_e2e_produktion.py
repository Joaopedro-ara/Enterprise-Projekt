
from playwright.sync_api import Playwright, sync_playwright, expect


def test_dashboard_navigation(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5000/login")
    page.locator("#mitarbeiter_id").click()
    page.locator("#mitarbeiter_id").fill("Dv-0018")
    page.get_by_role("textbox", name="Passwort").click()
    page.get_by_role("textbox", name="Passwort").fill("D")
    page.locator("#mitarbeiter_id").dblclick()
    page.locator("#mitarbeiter_id").click()
    page.locator("#mitarbeiter_id").press("ArrowLeft")
    page.locator("#mitarbeiter_id").press("ArrowLeft")
    page.locator("#mitarbeiter_id").press("ArrowLeft")
    page.locator("#mitarbeiter_id").press("ArrowLeft")
    page.locator("#mitarbeiter_id").press("ArrowLeft")
    page.locator("#mitarbeiter_id").fill("DV-0018")
    page.locator("#mitarbeiter_id").press("ArrowDown")
    page.get_by_role("textbox", name="Passwort").click()
    page.get_by_role("textbox", name="Passwort").fill("Dv-018")
    page.get_by_role("button", name="Anmelden").click()
    page.get_by_role("link", name="Produktionsverwaltung").click()
    page.get_by_role("link", name="Fehler-Logbuch anzeigen").click()
    page.get_by_role("link", name="Fehler-Logbuch anzeigen").click()

    # ---------------------
    expect(page.locator("h1")).to_contain_text("Fehler Meldungen")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    test_dashboard_navigation(playwright)
