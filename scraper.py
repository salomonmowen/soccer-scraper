from playwright.sync_api import sync_playwright
import csv

URL = "https://theanalyst.com/competition/uefa-champions-league/table"

COLUMNS = [
    "xpos",
    "team",
    "xpts",
    "League",
    "KO_P0",
    "Last16",
    "QF",
    "SF",
    "Final",
    "Winner"
]

def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        # switch tab
        page.locator("button[aria-controls='table-panel-predicted']").click()
        page.wait_for_selector("#table-panel-predicted tbody tr")

        rows = page.locator("#table-panel-predicted tbody tr")

        data = []

        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")

            row = [
                cells.nth(0).inner_text().strip(),
                cells.nth(1).inner_text().strip(),
                cells.nth(2).inner_text().strip(),
                cells.nth(3).inner_text().strip(),
                cells.nth(4).inner_text().strip(),
                cells.nth(5).inner_text().strip(),
                cells.nth(6).inner_text().strip(),
                cells.nth(7).inner_text().strip(),
                cells.nth(8).inner_text().strip(),
                cells.nth(9).inner_text().strip(),
            ]

            data.append(row)

        browser.close()

    # sort alphabetically by team
    data.sort(key=lambda x: x[1])

    # write CSV
    with open("predicted_table.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        writer.writerows(data)

if __name__ == "__main__":
    scrape()
