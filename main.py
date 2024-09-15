import argparse
import json
from threading import Thread
from webdrivermanager import WebDriverManager
from settingsmanager import SettingsManager
from executor import Executor
from linkedin import Linkedin
from indeed import Indeed
from wttj import WTTJ
from jobapplier.aihelper import AiHelper
from jobapplier.QuestionsManager import QuestionManager

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run job application bots with configuration options.')
    parser.add_argument('--browsers', nargs='+', default=['chrome'],
                        help='List of browsers to use (e.g., chrome firefox edge).')
    parser.add_argument('--local_paths', type=str,
                        help='Path to a JSON file with local driver paths.')
    parser.add_argument('--start', choices=['linkedin', 'indeed', 'wttj'], required=True,
                        help='Which bot to start.')
    parser.add_argument('--search', action='store_true',
                        help='Trigger a search operation.')
    parser.add_argument('--query', type=str,
                        help='Search query for the bots.')
    parser.add_argument('--threads', type=int, default=4,
                        help='Number of threads to use for executing tasks.')
    return parser.parse_args()

def setup_environment():
    settings = SettingsManager.get_settings()
    return settings

def initialize_drivers(args):
    local_paths = {}
    if args.local_paths:
        with open(args.local_paths, 'r') as file:
            local_paths = json.load(file)

    driver_manager = WebDriverManager(browsers=args.browsers, local_paths=local_paths)
    drivers = driver_manager.get_drivers()
    return drivers, driver_manager

def initialize_bot(bot_type):
    if bot_type == 'linkedin':
        return Linkedin()
    elif bot_type == 'indeed':
        return Indeed()
    elif bot_type == 'wttj':
        return WTTJ()
    else:
        raise ValueError("Unsupported bot type.")

def initialize_executor(drivers, bot, num_threads):
    return Executor(drivers=drivers, bot=bot, num_threads=num_threads)

def main():
    args = parse_arguments()
    settings = setup_environment()
    drivers, driver_manager = initialize_drivers(args)
    
    bot = initialize_bot(args.start)
    ai_helper = AiHelper()
    question_manager = QuestionManager(ai_helper)
    
    executor = initialize_executor(drivers, bot, args.threads)
    
    def run_executor():
        if args.search and args.query:
            print(f"Performing search with query: {args.query}")
            bot.search(args.query)
        else:
            bot.scrap()

    # Start the bot execution in a separate thread
    executor_thread = Thread(target=run_executor)
    executor_thread.start()
    
    # Wait for the executor to finish
    executor_thread.join()

    driver_manager.close_drivers()

if __name__ == "__main__":
    main()
