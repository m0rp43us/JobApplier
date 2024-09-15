from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from settingsmanager import SettingsManager
import os

class WebDriverManager:
    def __init__(self, browsers: list, local_paths: dict = None):
        self.browsers = browsers
        self.local_paths = local_paths if local_paths else {}
        self.settings = SettingsManager.get_settings()
        self.drivers = self._initialize_drivers()

    def _initialize_drivers(self) -> list:
        drivers = []
        for browser in self.browsers:
            if browser in self.local_paths:
                drivers.append(self._setup_local_driver(browser))
            else:
                if browser == "chrome":
                    drivers.append(self._setup_chrome_driver())
                elif browser == "firefox":
                    drivers.append(self._setup_firefox_driver())
                elif browser == "edge":
                    drivers.append(self._setup_edge_driver())
                elif browser == "safari":
                    drivers.append(self._setup_safari_driver())
                else:
                    raise ValueError(f"Unsupported browser: {browser}")
        return drivers

    def _setup_local_driver(self, browser: str) -> webdriver.WebDriver:
        path = self.local_paths.get(browser)
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"Local driver not found at {path}")

        if "chrome" in path.lower():
            return webdriver.Chrome(executable_path=path)
        elif "firefox" in path.lower():
            return webdriver.Firefox(executable_path=path)
        elif "edge" in path.lower():
            return webdriver.Edge(executable_path=path)
        else:
            raise ValueError(f"Unsupported local driver: {path}")

    def _setup_chrome_driver(self) -> webdriver.Chrome:
        print("Setting up Chrome driver...")
        service = ChromeService(self.settings.chrome_driver_path)
        options = ChromeOptions()
        for arg in self.settings.chrome_options:
            options.add_argument(arg)
        return webdriver.Chrome(service=service, options=options)

    def _setup_firefox_driver(self) -> webdriver.Firefox:
        print("Setting up Firefox driver...")
        service = FirefoxService(self.settings.firefox_driver_path)
        options = FirefoxOptions()
        for arg in self.settings.firefox_options:
            options.add_argument(arg)
        return webdriver.Firefox(service=service, options=options)

    def _setup_edge_driver(self) -> webdriver.Edge:
        print("Setting up Edge driver...")
        service = EdgeService(self.settings.edge_driver_path)
        options = EdgeOptions()
        for arg in self.settings.edge_options:
            options.add_argument(arg)
        return webdriver.Edge(service=service, options=options)

    def _setup_safari_driver(self) -> webdriver.Safari:
        print("Setting up Safari driver...")
        try:
            return webdriver.Safari()
        except Exception as e:
            raise RuntimeError("Safari driver setup failed. Ensure Safari is installed and WebDriver support is enabled.") from e

    def get_drivers(self) -> list:
        return self.drivers

    def close_drivers(self) -> None:
        for driver in self.drivers:
            if driver:
                driver.quit()
