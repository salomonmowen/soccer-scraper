from playwright.sync_api import sync_playwright
import os
import json
import gspread
from google.oauth2.service_account import Credentials

def get_value():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://theanalyst.com/competition/uefa-champions-league/table", timeout=60000)

        # click predicted tab
        page.locator("button[aria-controls='table-panel-predicted']").click()

        # wait for table
        page.wait_for_selector("#table-panel-predicted tbody tr")

        # get Arsenal row
        row = page.locator("#table-panel-predicted tbody tr:has-text('Arsenal')").first

        value = row.locator("td").nth(9).inner_text()

        browser.close()
        return value


def update_sheet(value):
    creds_dict = json.loads(os.environ["GOOGLE_CREDS"])

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(creds)
    sheet = client.open("YourSheetName").sheet1

    sheet.update("A1", value)


def main():
    value = get_value()
    update_sheet(value)
    print("Updated:", value)


main()
