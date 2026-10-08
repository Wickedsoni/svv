import asyncio
from playwright.async_api import async_playwright
import os

BASE_URL = "http://127.0.0.1:5000"
SCREENSHOT_DIR = "screenshots"

async def recapture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        print("Capturing SS-001: Login")
        await page.goto(f"{BASE_URL}/login")
        await page.screenshot(path=f"{SCREENSHOT_DIR}/SS-001.png")

        print("Capturing SS-002: Invalid Login (Empty Fields)")
        await page.click("button#login-btn")
        await page.wait_for_selector(".alert-danger")
        await page.screenshot(path=f"{SCREENSHOT_DIR}/SS-002.png")

        print("Logging in...")
        await page.fill("input#username", "admin")
        await page.fill("input#password", "admin123")
        await page.click("button#login-btn")
        await page.wait_for_selector("#total-employees")

        print("Capturing SS-003: Dashboard")
        await page.screenshot(path=f"{SCREENSHOT_DIR}/SS-003.png")

        await browser.close()
        print("SS-001, SS-002, and SS-003 recaptured successfully!")

asyncio.run(recapture())
