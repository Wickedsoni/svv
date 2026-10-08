import asyncio
from playwright.async_api import async_playwright
import os

BASE_URL = "http://127.0.0.1:5000"
DIR = "evidence/initial_failures"
os.makedirs(DIR, exist_ok=True)

async def capture_failures():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        # BUG-009: Login Typo
        await page.goto(f"{BASE_URL}/login")
        await page.screenshot(path=f"{DIR}/BUG-009_Login_Button_Typo.png")

        # Login to continue
        await page.fill("input#username", "admin")
        await page.fill("input#password", "admin123")
        await page.click("button#login-btn")
        await page.wait_for_selector("#total-employees")

        # BUG-010: Dashboard Typo
        await page.screenshot(path=f"{DIR}/BUG-010_Dashboard_Title_Typo.png")

        # BUG-011: Wrong Flash Color
        await page.goto(f"{BASE_URL}/employees/add")
        await page.fill("input#employee_id", "EMP900")
        await page.fill("input#emp_name", "Test Wrong Color")
        await page.fill("input#department", "IT")
        await page.fill("input#designation", "Developer")
        await page.fill("input#email", "emp900@test.com")
        await page.fill("input#phone", "9876543210")
        await page.fill("input#date_of_joining", "2026-10-01")
        await page.fill("input#basic_salary", "30000")
        await page.click("button#submit-add-emp")
        await page.wait_for_timeout(1000)
        
        await page.screenshot(path=f"{DIR}/BUG-011_Wrong_Flash_Category.png")

        await browser.close()
        print("Captured new initial failures!")

if __name__ == "__main__":
    asyncio.run(capture_failures())
