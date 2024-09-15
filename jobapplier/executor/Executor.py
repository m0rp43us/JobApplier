from jobapplier.executor.JobApplierStrategy import GlassdoorStrategy, IndeedStrategy, LinkedInStrategy


class Executor:
    def __init__(self):
        # Initialize strategies
        self.strategies = {
            "LinkedIn": LinkedInStrategy(),
            "Indeed": IndeedStrategy(),
            "Glassdoor": GlassdoorStrategy()  # Optional
        }

    def select_strategy(self, platform):
        # Select and return the appropriate strategy
        return self.strategies.get(platform)

    def execute_command(self, command):
        # Determine which strategy to use based on the command's platform
        platform = command.platform
        strategy = self.select_strategy(platform)
        if not strategy:
            raise ValueError(f"No strategy found for platform {platform}")

        # Execute the command using the selected strategy
        if isinstance(command, SearchJobCommand):
            strategy.search_jobs(command.query)
            self.save_job_offer_to_db(command.query)
        elif isinstance(command, ApplyJobCommand):
            strategy.apply_to_jobs(command.job_id)
            self.log_applied_job_to_db(command.job_id)
        else:
            raise ValueError(f"Unknown command type {type(command)}")

        # Send update via WebSocket
        self.send_update(f"Command executed: {type(command).__name__}")

    def save_job_offer_to_db(self, query):
        # Logic to save job offers to DB
        pass

    def log_applied_job_to_db(self, job_id):
        # Logic to log applied job to DB
        pass

    def send_update(self, update):
        # Logic to send update via WebSocket
        pass

class SearchJobCommand:
    def __init__(self, platform, query):
        """
        Initializes a SearchJobCommand instance.

        :param platform: The job platform where the search should be performed (e.g., "LinkedIn", "Indeed").
        :param query: The search query to use (e.g., "Software Engineer").
        """
        self.platform = platform
        self.query = query

    def serialize(self):
        """
        Serializes the command to a format suitable for sending over WebSocket or saving to a database.

        :return: A serialized representation of the command.
        """
        return f"SEARCH_JOB|{self.platform}|{self.query}"

    def execute(self, executor):
        """
        Executes the command using the provided Executor instance.

        :param executor: The Executor instance responsible for processing the command.
        """
        executor.execute_command(self)
        
class ApplyJobCommand:
    def __init__(self, platform, job_id):
        """
        Initializes an ApplyJobCommand instance.

        :param platform: The job platform where the job application should be made (e.g., "LinkedIn", "Indeed").
        :param job_id: The ID of the job to apply to.
        """
        self.platform = platform
        self.job_id = job_id

    def serialize(self):
        """
        Serializes the command to a format suitable for sending over WebSocket or saving to a database.

        :return: A serialized representation of the command.
        """
        return f"APPLY_JOB|{self.platform}|{self.job_id}"

    def execute(self, executor):
        """
        Executes the command using the provided Executor instance.

        :param executor: The Executor instance responsible for processing the command.
        """
        executor.execute_command(self)
