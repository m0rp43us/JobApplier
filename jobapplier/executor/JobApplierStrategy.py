from abc import ABC, abstractmethod

class JobStrategy(ABC):
    @abstractmethod
    def search_jobs(self, query):
        """
        Searches for jobs based on the query.

        :param query: The search query.
        """
        pass

    @abstractmethod
    def apply_to_jobs(self, job_id):
        """
        Applies to a specific job.

        :param job_id: The ID of the job to apply to.
        """
        pass

class LinkedInStrategy(JobStrategy):
    def search_jobs(self, query):
        print(f"Searching for jobs on LinkedIn with query: {query}")
        # Implementation for LinkedIn job search

    def apply_to_jobs(self, job_id):
        print(f"Applying to job {job_id} on LinkedIn")
        # Implementation for LinkedIn job application

class IndeedStrategy(JobStrategy):
    def search_jobs(self, query):
        print(f"Searching for jobs on Indeed with query: {query}")
        # Implementation for Indeed job search

    def apply_to_jobs(self, job_id):
        print(f"Applying to job {job_id} on Indeed")
        # Implementation for Indeed job application

class GlassdoorStrategy(JobStrategy):
    def search_jobs(self, query):
        print(f"Searching for jobs on Glassdoor with query: {query}")
        # Implementation for Glassdoor job search

    def apply_to_jobs(self, job_id):
        print(f"Applying to job {job_id} on Glassdoor")
        # Implementation for Glassdoor job application



