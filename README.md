## TYPO3 Content Craft

TYPO3 Content Craft is a powerful tool designed to automatically generate pages and content in a TYPO3 installation using data from Wikipedia. This tool is perfect for quickly creating test content or populating a TYPO3 site with real-world information on various topics.

## Features

- Automatic generation of TYPO3 pages based on Wikipedia topics
- Creation of varied and relevant content for each page
- Multi-language support
- Direct connection to the TYPO3 database
- Customization of page titles and content
- Intelligent handling of complex and specific topics
- Flexible use via command line or interactive mode

## Prerequisites

- Python 3.7 or higher
- Access to a TYPO3 database
- Write permissions on the TYPO3 database
- Internet connection to access the Wikipedia API

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/typo3-content-craft.git
   cd typo3-content-craft
   ```

2. Create a virtual environment (recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the environment variables by creating a `.env` file at the root of the project:
   ```
   DB_HOST=your_host
   DB_NAME=your_database_name
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_PORT=your_port
   ```

## Usage

You can run the script in two ways:

1. Interactive mode:
   ```
   python content_craft.py
   ```

2. Using command-line arguments:
   ```
   python content_craft.py --parent_id 1 --num_pages 10 --language fr --num_words 200 --themes "Electric Vehicles,Autonomous Driving,Road Safety"
   ```

### Available options:

- `--parent_id`: ID of the parent page in TYPO3
- `--num_pages`: Number of pages to create
- `--language`: Language code (e.g., fr, en)
- `--num_words`: Number of words for the content of each page
- `--themes`: Comma-separated list of themes

## How it works

1. The script connects to the specified TYPO3 database.
2. For each page to be created, it selects a random theme from those provided
3. It searches for relevant content on Wikipedia for that theme
4. It generates a catchy title for the page
5. It creates a new page in TYPO3 with the obtained content
6. The process repeats until the requested number of pages is reached

## Usage tips

- For optimal results, use varied and specific themes
- Adjust the number of words according to your content needs
- Always check the generated content to ensure it meets your expectations

## Troubleshooting

- If you encounter database connection errors, check your settings in the `.env` file
- For issues related to the Wikipedia API, make sure you have a stable internet connection
- In case of persistent errors, consult the logs for more details

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details

---

Developed by Cyril Wolfangel with ❤️ for the TYPO3 community 
