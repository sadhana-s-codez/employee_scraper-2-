import unittest
from unittest.mock import patch, Mock
import pandas as pd

from employee_scraper import (
    download_file,
    detect_file_type,
    validate_columns,
    validate_data,
    extract_data
)

class TestEmployeeScraper(unittest.TestCase):

    @patch("employee_scraper.requests.get")
    def test_download_file(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"sample"
        mock_get.return_value = mock_response
        result = download_file("dummy", "test_downloaded_file.csv")
        self.assertEqual(result, "test_downloaded_file.csv")


    
    def test_extract_data(self):
        df = pd.DataFrame({
            "Employee ID":[1],
            "First Name":["John"],
            "Last Name":["David"],
            "Email":["john@gmail.com"],
            "Job Title":["Developer"],
            "Phone Number":["9999999999"],   
            
        })
        self.assertEqual(len(extract_data(df)),1)


    
    def test_file_type(self):
        self.assertEqual(detect_file_type("downloaded_file.csv"),"csv")


    
    def test_validate_columns(self):
        df = pd.DataFrame({
            "Employee ID":[1],
            "First Name":["John"],
            "Last Name":["David"],
            "Email":["john@gmail.com"],
            "Job Title":["Developer"],
            "Phone Number":["9999999999"],   
        })

        self.assertTrue(validate_columns(df))


    
    def test_missing_data(self):
        df = pd.DataFrame({
            "Employee ID":[1],
            "First Name":[None],
            "Last Name":["David"],
            "Email":["john@gmail.com"],
            "Job Title":["Developer"],
            "Phone Number":["9999999999"],   
        
        })

        self.assertTrue(validate_data(df))


if __name__ == "__main__":
    unittest.main()