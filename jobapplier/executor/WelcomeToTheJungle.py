import time
import requests
from bs4 import BeautifulSoup
from settingsmanager.SettingsManager import SettingsManager

class WelcomeToTheJungle:
    def __init__(self):
        self.name = 'Welcome to the Jungle'
        # Fetch settings directly from SettingsManager
        self.url_template = SettingsManager.get_settings().get('wttj_url_template', 'https://www.welcometothejungle.com/fr/jobs?page={}&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Fullstack&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Backend&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Frontend&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Dev+Mobile&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD+%2F+Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance&aroundQuery=Paris%2C+France&aroundLatLng=48.85718%2C2.34141&aroundRadius=10000&sortBy=mostRecent')
        self.should_scroll_page = SettingsManager.get_settings().get('wttj_should_scroll_page', True)

    def scrap(self):
        page = 1
        while True:
            page_url = self._generate_page_url(page)
            page_data = self._fetch_page_data(page_url)
            job_elements = self._parse_page_data(page_data)

            if not job_elements or page > 6:
                print(f"Finished scraping WTTJ page #{page}.")
                break

            self._process_jobs(job_elements)
            page += 1

    def _generate_page_url(self, page_number):
        """
        Generates the URL for a specific page number using the template.
        """
        return self.url_template.format(page_number)

    def _fetch_page_data(self, url):
        """
        Fetches page data from the given URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page data: {e}")
            return ""

    def _parse_page_data(self, page_data):
        """
        Parses the page data and returns a list of job elements.
        """
        page_soup = BeautifulSoup(page_data, 'html.parser')
        return page_soup.find_all('article', attrs={'data-role': 'jobs:thumb'})

    def _process_jobs(self, job_elements):
        """
        Processes each job element: extracts details, checks the database, and handles new jobs.
        """
        print(f"Found {len(job_elements)} jobs to process.")
        for job in job_elements:
            job_details = self._extract_job_details(job)
            if job_details:
                job_company, job_name, job_thumbnail, job_link = job_details
                if not is_url_in_database(job_link):
                    self._handle_new_job(job_link, job_name, job_company, job_thumbnail)
        print('Page processing finished.')

    def _extract_job_details(self, job):
        """
        Extracts job details from a BeautifulSoup job element.
        """
        try:
            job_company = job.find('h4').find('span', attrs={'class': 'ais-Highlight-nonHighlighted'}).text
            job_name = job.find('h3').find('span', attrs={'class': 'ais-Highlight-nonHighlighted'}).text
            job_thumbnail = job.find('img', attrs={'alt': job_company})['src']
            job_link = 'https://welcometothejungle.com' + job.find('a', href=True)['href']
            return job_company, job_name, job_thumbnail, job_link
        except AttributeError as e:
            print(f"Error extracting job details: {e}")
            return None

    def _handle_new_job(self, job_link, job_name, job_company, job_thumbnail):
        """
        Handles a new job: adds to the database.
        """
        print(f"Found new job: {job_link}")
        add_url_in_database(job_link)
        # Optionally, implement further handling if needed
        time.sleep(4)
