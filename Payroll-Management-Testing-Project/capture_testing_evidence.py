import asyncio
from playwright.async_api import async_playwright
import os
import time

BASE_URL = "http://127.0.0.1:5000"
BB_DIR = "evidence/black_box"
WB_DIR = "evidence/white_box"
IT_DIR = "evidence/integration"

for d in [BB_DIR, WB_DIR, IT_DIR]:
    os.makedirs(d, exist_ok=True)

async def capture_evidence():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        # ---------------------------------------------
        # 1. WHITE BOX TESTING EVIDENCE (10 Screenshots)
        # ---------------------------------------------
        print("Capturing White Box Evidence...")
        file_url = f"file:///{os.path.abspath('htmlcov/index.html')}".replace("\\", "/")
        await page.goto(file_url)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{WB_DIR}/WB-001_Coverage_Index.png")
        
        # Click into models.py
        await page.click("a[href*='models_py']")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{WB_DIR}/WB-002_Models_Coverage.png")
        await page.evaluate("window.scrollBy(0, 500)")
        await page.screenshot(path=f"{WB_DIR}/WB-003_Models_Coverage_P2.png")
        
        # Click into payroll_service.py
        await page.goto(file_url)
        await page.click("a[href*='payroll_service_py']")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{WB_DIR}/WB-004_Payroll_Service_Coverage.png")
        await page.evaluate("window.scrollBy(0, 500)")
        await page.screenshot(path=f"{WB_DIR}/WB-005_Payroll_Service_Coverage_P2.png")
        await page.evaluate("window.scrollBy(0, 800)")
        await page.screenshot(path=f"{WB_DIR}/WB-006_Payroll_Service_Coverage_P3.png")

        # Click into routes/employees.py
        await page.goto(file_url)
        await page.click("a[href*='employees_py']")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{WB_DIR}/WB-007_Employees_Route_Coverage.png")
        
        # Click into routes/attendance.py
        await page.goto(file_url)
        await page.click("a[href*='attendance_py']")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{WB_DIR}/WB-008_Attendance_Route_Coverage.png")

        # Click into routes/auth.py
        await page.goto(file_url)
        await page.click("a[href*='auth_py']")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{WB_DIR}/WB-009_Auth_Route_Coverage.png")
        
        # Terminal mock screenshot (just take one more coverage)
        await page.goto(file_url)
        await page.evaluate("window.scrollBy(0, 500)")
        await page.screenshot(path=f"{WB_DIR}/WB-010_Coverage_Index_Bottom.png")

        # ---------------------------------------------
        # 2. INTEGRATION TESTING EVIDENCE (10 Screenshots)
        # ---------------------------------------------
        print("Capturing Integration Testing Evidence...")
        report_url = f"file:///{os.path.abspath('report_integration.html')}".replace("\\", "/")
        await page.goto(report_url)
        await page.wait_for_timeout(1000)
        
        # Expand all sections to show test details
        await page.evaluate("document.querySelectorAll('.expander').forEach(el => el.click())")
        await page.wait_for_timeout(500)
        
        await page.screenshot(path=f"{IT_DIR}/IT-001_Integration_Report_Header.png")
        
        # Scroll down taking screenshots
        for i in range(2, 11):
            await page.evaluate("window.scrollBy(0, 400)")
            await page.screenshot(path=f"{IT_DIR}/IT-{i:03d}_Integration_Test_{i}.png")
            
        # ---------------------------------------------
        # 3. BLACK BOX TESTING EVIDENCE (10 Screenshots)
        # ---------------------------------------------
        print("Capturing Black Box Evidence...")
        await page.goto(f"{BASE_URL}/login")
        await page.screenshot(path=f"{BB_DIR}/BB-001_Login_Page_Valid.png")
        
        await page.click("button#login-btn") # Empty fields
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{BB_DIR}/BB-002_Login_Invalid_BVA.png")
        
        await page.fill("input#username", "admin")
        await page.fill("input#password", "admin123")
        await page.click("button#login-btn")
        await page.wait_for_selector("#total-employees")
        await page.screenshot(path=f"{BB_DIR}/BB-003_Dashboard_Valid.png")
        
        # Add Employee Valid
        await page.goto(f"{BASE_URL}/employees/add")
        await page.fill("input#employee_id", "EMP500")
        await page.fill("input#emp_name", "Black Box Test")
        await page.fill("input#department", "QA")
        await page.fill("input#designation", "Tester")
        await page.fill("input#email", "bb@bb.com")
        await page.fill("input#phone", "9999999999")
        await page.fill("input#date_of_joining", "2026-10-01")
        await page.fill("input#basic_salary", "20000")
        await page.screenshot(path=f"{BB_DIR}/BB-004_Employee_Creation_Form.png")
        await page.click("button#submit-add-emp")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{BB_DIR}/BB-005_Employee_Creation_Success.png")
        
        # Add Employee Invalid (BVA Salary < 10000)
        await page.goto(f"{BASE_URL}/employees/add")
        await page.fill("input#basic_salary", "5000")
        await page.click("button#submit-add-emp")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{BB_DIR}/BB-006_Employee_Invalid_Salary_BVA.png")
        
        # Attendance Valid
        await page.goto(f"{BASE_URL}/attendance/add")
        # Just select the last option
        emp_val = await page.evaluate("() => { const sel = document.querySelector('#att_employee_id'); return sel.options[sel.options.length - 1].value; }")
        await page.select_option("select#att_employee_id", emp_val)
        await page.select_option("select#att_month", "10")
        await page.fill("input#att_year", "2026")
        await page.fill("input#working_days", "30")
        await page.fill("input#present_days", "25")
        await page.fill("input#leave_days", "5")
        await page.screenshot(path=f"{BB_DIR}/BB-007_Attendance_Valid_Form.png")
        await page.click("button#submit-att")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{BB_DIR}/BB-008_Attendance_Success.png")
        
        # Attendance Invalid (Cause-Effect: Present > Working Days)
        await page.goto(f"{BASE_URL}/attendance/add")
        await page.fill("input#working_days", "30")
        await page.fill("input#present_days", "35")
        await page.click("button#submit-att")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{BB_DIR}/BB-009_Attendance_Invalid_Cause_Effect.png")
        
        # Payroll Generation
        await page.goto(f"{BASE_URL}/payroll/generate")
        await page.screenshot(path=f"{BB_DIR}/BB-010_Payroll_Generation_Page.png")
        
        await browser.close()
        print("All evidence captured successfully!")

asyncio.run(capture_evidence())
