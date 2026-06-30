Employee Data Scraper

A Python application that downloads employee data from a Google Drive URL, validates the data, extracts employee details, and displays them in a structured format.

 Features
* Downloads employee data from Google Drive
* Supports CSV and Excel files
* Validates required employee fields
* Handles missing or invalid data
* Logs errors and retry attempts
* Includes unit tests using unittest

Requirements
* Python 3.x
* pandas
* requests
* openpyxl

Install dependencies:
pip install -r requirements.txt

Run:
python employee_scraper.py

Run tests:
python -m unittest test_employee_scraper.py
