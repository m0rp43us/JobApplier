import time
import math
import random
import os
import pickle
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import SettingsManager
import DatabaseManager

class Linkedin:
    def __init__(self):
        self.setup_browser()
        self.load_cookies()
        if not self.is_logged_in():
            self.login()
            self.save_cookies()

    def setup_browser(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=utils.chrome_browser_options())
        self.cookies_path = f"{os.path.join(os.getcwd(), 'cookies')}/{self.get_hash(config.email)}.pkl"
        self.driver.get('https://www.linkedin.com')

    def get_hash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def load_cookies(self):
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, "rb") as file:
                cookies = pickle.load(file)
                self.driver.delete_all_cookies()
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

    def save_cookies(self):
        with open(self.cookies_path, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)

    def is_logged_in(self):
        self.driver.get('https://www.linkedin.com/feed')
        try:
            self.driver.find_element(By.XPATH, '//*[@id="ember14"]')
            return True
        except:
            return False

    def login(self):
        self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
        utils.prYellow("🔄 Logging in...")
        try:
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(30)
        except Exception as e:
            utils.prRed(f"❌ Login failed. Error: {e}")

    def generate_urls(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        try:
            with open('data/urlData.txt', 'w', encoding="utf-8") as file:
                linkedin_job_links = utils.LinkedinUrlGenerate().generate_url_links()
                file.write('\n'.join(linkedin_job_links))
            utils.prGreen("✅ URLs generated successfully.")
        except Exception as e:
            utils.prRed(f"❌ URL generation failed. Error: {e}")

    def search_jobs(self, search_query):
        search_url = f'https://www.linkedin.com/jobs/search/?keywords={search_query}'
        self.driver.get(search_url)
        # Further code to extract job URLs from search results
        return utils.extract_job_urls(self.driver)

    def apply_jobs(self):
        self.generate_urls()
        url_data = utils.get_url_data_file()
        for url in url_data:
            self.driver.get(url)
            time.sleep(random.uniform(1, constants.botSpeed))
            total_jobs = self.driver.find_element(By.XPATH, '//small').text
            total_pages = utils.jobs_to_pages(total_jobs)
            url_words = utils.url_to_keywords(url)
            utils.prYellow(f"Processing: Category: {url_words[0]}, Location: {url_words[1]}, Total Jobs: {total_jobs}")

            for page in range(total_pages):
                self.process_page(url, page, url_words)

    def process_page(self, url, page, url_words):
        current_page_jobs = constants.jobsPerPage * page
        paged_url = f"{url}&start={current_page_jobs}"
        self.driver.get(paged_url)
        time.sleep(random.uniform(1, constants.botSpeed))

        offers = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
        offer_ids = [offer.get_attribute("data-occludable-job-id").split(":")[-1] for offer in offers]
        time.sleep(random.uniform(1, constants.botSpeed))

        for offer_id in offer_ids:
            self.apply_job(offer_id, url_words)

    def apply_job(self, job_id, url_words):
        offer_page = f'https://www.linkedin.com/jobs/view/{job_id}'
        self.driver.get(offer_page)
        time.sleep(random.uniform(1, constants.botSpeed))

        job_properties = self.get_job_properties()
        if "blacklisted" in job_properties:
            utils.prYellow(f"Blacklisted job: {offer_page}")
            return

        easy_apply_button = self.find_easy_apply_button()
        if easy_apply_button:
            easy_apply_button.click()
            time.sleep(random.uniform(1, constants.botSpeed))
            self.choose_resume()
            try:
                self.submit_application()
                utils.prGreen(f"Applied to job: {offer_page}")
                database_manager.save_applied_job(offer_page, job_properties)
            except Exception as e:
                utils.prRed(f"Application failed for job: {offer_page}. Error: {e}")
        else:
            utils.prYellow(f"Already applied or no Easy Apply button: {offer_page}")

    def choose_resume(self):
        try:
            resumes = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ui-attachment--pdf')]")
            if resumes:
                preferred_resume = resumes[config.preferredCv - 1] if len(resumes) >= config.preferredCv else resumes[0]
                preferred_resume.click()
        except Exception as e:
            utils.prRed(f"Error selecting resume: {e}")

    def get_job_properties(self):
        job_title = self.get_text(By.XPATH, "//h1[contains(@class, 'job-title')]")
        job_detail = self.get_text(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div")
        job_location = self.get_text(By.XPATH, "//span[contains(@class, 'job-location')]")
        return f"Title: {job_title}, Location: {job_location}, Details: {job_detail}"

    def get_text(self, by, xpath):
        try:
            return self.driver.find_element(by, xpath).text.strip()
        except:
            return ""

    def find_easy_apply_button(self):
        try:
            return self.driver.find_element(By.XPATH, '//button[contains(@class, "jobs-apply-button")]')
        except:
            return None

    def submit_application(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

    def display_results(self, message):
        utils.prGreen(message)

if __name__ == "__main__":
    linkedin_bot = Linkedin()
    linkedin_bot.apply_jobs()