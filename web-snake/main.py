from playwright.sync_api import sync_playwright

pswd="Na12345678"

with sync_playwright() as p:
    # Launch Chromium (or 'firefox' or 'webkit'). Set headless=False to see it happen.
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to a website
    page.goto('https://mydsd.davis.k12.ut.us')
    
    # Example interactions:
    page.locator('input[type="text"], input[name*="user"], input[id*="user"]').first.fill('29nnaylor')
    
    # 3. Fill in your Password
    page.locator('input[type="password"]').fill(pswd)
    
    # 4. Click the "Sign In" button 
    # This uses the exact button element classes visible in your HTML inspector screenshot
    # Change this line in your script:
    page.get_by_role("button", name="Sign in").click()

    # page.click('button[type="submit"]')
    
    print(page.title())
    page.wait_for_timeout(10000)
    browser.close()
