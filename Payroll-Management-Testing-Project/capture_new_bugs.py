import asyncio
from playwright.async_api import async_playwright
import os

BASE_URL = "http://127.0.0.1:5000"
EVIDENCE_DIR = "evidence/new_failures"

os.makedirs(EVIDENCE_DIR, exist_ok=True)

async def capture_new_bugs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        print("Logging in...")
        await page.goto(f"{BASE_URL}/login")
        await page.fill("input#username", "admin")
        await page.fill("input#password", "admin123")
        await page.click("button#login-btn")
        await page.wait_for_selector("#total-employees")

        print("Capturing BUG-006: Numeric Employee Name Bypassed")
        await page.goto(f"{BASE_URL}/employees/add")
        await page.fill("input#employee_id", "EMP103")
        await page.fill("input#emp_name", "123456") # Numeric name
        await page.fill("input#department", "QA")
        await page.fill("input#designation", "Tester")
        await page.fill("input#email", "123456@test.com")
        await page.fill("input#phone", "9876543210")
        await page.fill("input#date_of_joining", "2026-10-08")
        await page.fill("input#basic_salary", "60000") # > 15000 to hit bug 8
        await page.click("button#submit-add-emp")
        # Wait for redirect to /employees and success alert
        await page.wait_for_selector(".alert-success")
        await page.screenshot(path=f"{EVIDENCE_DIR}/BUG-006.png")
        
        print("Capturing BUG-007: Negative Overtime Hours Bypassed")
        await page.goto(f"{BASE_URL}/attendance/add")
        # Assuming EMP103 is ID=3, but let's just select by label or last option
        # We will use JavaScript to find the option value for EMP103
        emp_val = await page.evaluate("() => { const sel = document.querySelector('#att_employee_id'); return Array.from(sel.options).find(o => o.text.includes('EMP103')).value; }")
        await page.select_option("select#att_employee_id", emp_val)
        await page.select_option("select#att_month", "10")
        await page.fill("input#att_year", "2026")
        await page.fill("input#working_days", "30")
        await page.fill("input#present_days", "30")
        await page.fill("input#leave_days", "0")
        await page.fill("input#overtime_hours", "-10") # Negative
        # Bypass HTML5 form validation to test backend
        await page.evaluate("document.querySelector('#add-attendance-form').setAttribute('novalidate', true)")
        await page.click("button#submit-att")
        await page.wait_for_selector(".alert-success")
        await page.screenshot(path=f"{EVIDENCE_DIR}/BUG-007.png")
        
        print("Capturing BUG-008: Professional Tax Ignore")
        # Generate payroll
        await page.goto(f"{BASE_URL}/payroll/generate")
        emp_val3 = await page.evaluate("() => { const sel = document.querySelector('#payroll_employee_id'); return Array.from(sel.options).find(o => o.text.includes('EMP103')).value; }")
        await page.select_option("select#payroll_employee_id", emp_val3)
        await page.select_option("select#payroll_month", "10")
        await page.fill("input#payroll_year", "2026")
        await page.click("button#submit-generate")
        await page.wait_for_selector(".alert-success")
        
        # View Payslip
        await page.goto(f"{BASE_URL}/payroll")
        # Click view payslip for EMP103
        # Get the ID of the payroll record. It's the most recent one.
        payslip_url = await page.evaluate("() => { const links = Array.from(document.querySelectorAll('a')); return links.find(l => l.innerText.includes('Payslip') && l.href.includes('/payslip')).href; }")
        await page.goto(payslip_url)
        await page.wait_for_selector(".card")
        await page.screenshot(path=f"{EVIDENCE_DIR}/BUG-008.png")

        await browser.close()
        print("All new bug screenshots captured successfully!")

asyncio.run(capture_new_bugs())
