import requests
from bs4 import BeautifulSoup
import json

class TINDataScraper:
    def __init__(self, tin_number, captcha_value):
        self.url = "https://tin.tin.nsdl.com/TinxsysInternetWeb/searchByTin_Inter.jsp"
        self.tin_number = tin_number
        self.captcha_value = captcha_value
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def scrape_data(self):
        payload = {
            'tin': self.tin_number,
            'captcha': self.captcha_value
        }
        response = self.session.post(self.url, headers=self.headers, data=payload)
        print("response = ", response)
        
        with open('dealer_details.html', 'w', encoding='utf-8') as file:
            file.write(response.text)

        if response.status_code == 404:
            raise Exception("The URL returned a 404 status code. Please check the URL.")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        try:
            data = {
                'tin_number': self.tin_number,
                'cst_number': soup.find(string="CST Number").find_next('td').text.strip(),
                'dealer_name': soup.find(string="Dealer Name").find_next('td').text.strip(),
                'dealer_address': soup.find(string="Dealer Address").find_next('td').text.strip(),
                'state_name': soup.find(string="State Name").find_next('td').text.strip(),
                'pan_number': soup.find(string="PAN").find_next('td').text.strip() if soup.find(string="PAN") else 'NOT AVAILABLE',
                'registration_date': soup.find(string="Date of Registration under CST Act").find_next('td').text.strip(),
                'registration_status': soup.find(string="Dealer Registration Status under CST Act").find_next('td').text.strip(),
                'valid_upto': soup.find(string="This record is valid as on").find_next('td').text.strip()
            }
        except AttributeError as e:
            raise Exception("Could not find the necessary data on the page. Please verify the page structure.") from e

        return data

if __name__ == "__main__":
    tin_number = "21711100073"
    captcha_value = input("Enter CAPTCHA value: ")
    scraper = TINDataScraper(tin_number, captcha_value)
    try:
        data = scraper.scrape_data()
        print(json.dumps(data, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")
