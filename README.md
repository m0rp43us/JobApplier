# Job Applier Bot

![Job Applier Bot](image.jpeg)

Welcome to the Job Applier Bot project! This bot is designed to automate job applications across various job platforms. It supports integration with LinkedIn, Indeed, and other job boards.

## Features

- **Automated Job Applications**: Apply to jobs on LinkedIn, Indeed, and more.
- **Web Scraping**: Extract job listings from multiple sources.
- **AI Assistance**: Uses AI models for handling job-related queries.
- **Database Integration**: Keeps track of job applications and offers.

## Getting Started

To get started with the Job Applier Bot, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/job-applier-bot.git
    cd job-applier-bot
    ```

2. **Set Up the Environment**:
    - Create a virtual environment:
      ```bash
      python -m venv venv
      ```
    - Activate the virtual environment:
      - On Windows:
        ```bash
        venv\Scripts\activate
        ```
      - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Settings**:
    - Copy the sample configuration file:
      ```bash
      cp config.sample.py config.py
      ```
    - Edit `config.py` to add your LinkedIn, Indeed, and other job board credentials.

5. **Run the Bot**:
    ```bash
    python main.py
    ```

## Configuration

The bot's configuration is managed through the `config.py` file. You can set various parameters, including:

- **API Keys**: For accessing job boards and AI models.
- **Job Board URLs**: URLs for scraping job listings.
- **Database Settings**: Connection details for MongoDB and PostgreSQL.

## Usage

Once configured, you can run the bot to start applying for jobs automatically. The bot will:

- Scrape job listings from the specified sources.
- Apply to jobs based on the configured criteria.
- Log applications and offers in the database.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Push your branch and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [your-email@example.com](mailto:your-email@example.com).

---

Thank you for using Job Applier Bot!
