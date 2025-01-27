

import asyncio
from playwright.async_api import async_playwright
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load environment variables from .env file
load_dotenv()

# Constants for readability and maintainability
BASE_URL = os.getenv("BASE_URL")
LOGIN_PAGE_URL = os.getenv("LOGIN_PAGE_URL")
ADMIN_DEFAULT_URL = os.getenv("ADMIN_DEFAULT_URL")
FOOTER_SELECTOR = os.getenv("FOOTER_SELECTOR")

class RestoconceptAutomator:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    async def login(self, page) -> bool:
        """Logs into the Restoconcept admin portal."""
        try:
            logger.info("Navigating to login page...")
            await page.goto(LOGIN_PAGE_URL)
            await page.fill("#adminuser", self.username)
            await page.fill("#adminPass", self.password)
            await page.click("#btn1")

            # Check for successful login
            try:
                await page.wait_for_selector(FOOTER_SELECTOR, timeout=5000)
                return True
            except Exception:
                if page.url == ADMIN_DEFAULT_URL:
                    logger.info("Login successful: Redirect to admin default page detected.")
                    return True
                else:
                    logger.error("Login failed: Neither footer nor admin default page detected.")
                    return False
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    async def fill_and_submit(self, page, rec_id: int):
        """Navigates to the specified page, fills the input, and clicks the submit button."""
        try:
            # Dynamically create the target URL with rec_id
            target_url = f"{BASE_URL}SA_prod_edit.asp?action=edit&recID=27892&msg=Le+produit+a+%C3%A9t%C3%A9+ajout%C3%A9+%C3%A0+la+cat%C3%A9gorie%2E"
            logger.info(f"Navigating to target page with recID={rec_id}...")
            await page.goto(target_url)

            # Fill the input field
            logger.info(f"Filling the input field for recID={rec_id}...")
            await page.fill("#idcategory1", "3323")

            # Click the "Envoyer" button
            logger.info(f"Clicking the 'Envoyer' button for recID={rec_id}...")
            await page.click(
                "form[name='form3'] button:has-text('Envoyer')"
            )

            logger.info(f"Form submitted successfully for recID={rec_id}.")
        except Exception as e:
            logger.error(f"Error during form filling and submission for recID={rec_id}: {e}")

async def main():
    username = "letaief"  # Replace with your username
    password = "mohamed jihe"  # Replace with your password

    automator = RestoconceptAutomator(username, password)

    # List of recIDs you want to process
    rec_ids = [31320 ]  # Add more IDs as needed

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True for a headless browser
        context = await browser.new_context()
        page = await context.new_page()

        # Perform login
        if await automator.login(page):
            logger.info("Login successful.")

            # Process each recID
            for rec_id in rec_ids:
                await automator.fill_and_submit(page, rec_id)

        else:
            logger.error("Login failed. Aborting script.")

        await browser.close()

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
