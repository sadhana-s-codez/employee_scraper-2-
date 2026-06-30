import os
import csv
import logging
import requests
import pandas as pd
from time import sleep

logging.basicConfig(
    filename="employee.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = "https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download"
DOWNLOAD_FILE = "downloaded_file.csv"
REQUIRED_COLUMNS = [
    "Employee ID",
    "First Name",
    "Last Name",
    "Email",
    "Job Title",
    "Phone Number"
]


def download_file(url, filename, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filename, "wb") as file:
                file.write(response.content)
            logging.info("File downloaded successfully.")
            return filename

        except requests.exceptions.RequestException as e:
            logging.error(f"Download failed: {e}")
            if attempt < retries - 1:
                print("Retrying download...")
                sleep(2)
            else:
                print("Download failed after maximum retries.")
                logging.error("Maximum retries exceeded.")
                return None


def detect_file_type(filename):
    extension = os.path.splitext(filename)[1].lower()
    if extension == ".csv":
        return "csv"
    elif extension in [".xlsx", ".xls"]:
        return "excel"
    else:
        return None


def read_file(filename):
    file_type = detect_file_type(filename)
    if file_type == "csv":
        df = pd.read_csv(filename)
    elif file_type == "excel":
        df = pd.read_excel(filename)
    else:
        raise ValueError("Unsupported File Format")
    return df


def validate_columns(df):
    missing = []
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing.append(column)
    if missing:
        raise ValueError(f"Missing Columns : {missing}")
    return True


def validate_data(df):
    if df[REQUIRED_COLUMNS].isnull().values.any():
        logging.warning("Missing employee information detected.")
        print("Some employee records contain missing values.")
    else:
        print("No missing values found.")
    return True

def extract_data(df):
    employees = []
    for _, row in df.iterrows():
        employee = {
            "Employee ID": row["Employee ID"],
            "First Name": row["First Name"],
            "Last Name": row["Last Name"],
            "Email": row["Email"],
            "Job Title": row["Job Title"],
            "Phone Number": row["Phone Number"],
            
        }
        employees.append(employee)
    return employees


def main():
    filename = download_file(URL, DOWNLOAD_FILE)
    if filename is None:
        print("Failure Notification : Download Failed")
        return

    try:
        df = read_file(filename)
        df=df.rename(columns={
        "User Id":"Employee ID",
        "Phone":"Phone Number"
        })
        validate_columns(df)
        validate_data(df)
        employees = extract_data(df)
        print()
        print("Employee Data")
        print("-------------------------")

        for employee in employees:
            print(f"Employee ID  : {employee['Employee ID']}")
            print(f"First Name   : {employee['First Name']}")
            print(f"Last Name    : {employee['Last Name']}")
            print(f"Email        : {employee['Email']}")
            print(f"Job Title    : {employee['Job Title']}")
            print(f"Phone Number : {employee['Phone Number']}")
            print("-" * 50)
        logging.info("Data extraction completed successfully.")

    except Exception as e:
        logging.error(str(e))
        print("Error :", e)

if __name__ == "__main__":
    main()