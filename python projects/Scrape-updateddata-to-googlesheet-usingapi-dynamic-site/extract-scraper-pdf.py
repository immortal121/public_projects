from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
import time
from selenium.webdriver.common.by import By
  
from PyPDF2 import PdfReader
import re
import requests
from bs4 import BeautifulSoup
import datetime
import gspread
gc = gspread.service_account(filename='google.json')

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

def get_sbi_tt_price(text):
	pattern = r"UNITED STATES DOLLAR USD/INR \d+\.\d+ (?P<exchange_rate>\d+\.\d+)"
	match = re.search(pattern,text)
	if match:
		return float(match.group("exchange_rate"))

def check_for_today_date(text):
  """Checks if the text contains today's date in the given format.

  Args:
    text: The text to check.

  Returns:
    True if the text contains today's date, False otherwise.
  """
  today = datetime.datetime.today().strftime("%d-%m-%Y")
  pattern = r"{}".format(today)
  match = re.search(pattern, text)
  return match is not None

def pdf_downloader(base_url,pdf):
	response = requests.get(base_url, verify=False)
	with open(pdf, 'wb') as f:
		f.write(response.content)
	print("pdf writed")

def send_text_via_telegram(csp,bic,today,LME,sbi_tt_price):
	csp  = round(csp,2)
	bic = round(bic,2)
	text_msg = f"\nDATE : {today}\nCSP Price : {csp}\nBIC Price : {bic}\nLME : {LME}\nSBI TT Price : {sbi_tt_price}"
	response = requests.post('https://api.telegram.org/<bot token>/sendMessage?chat_id=<chat token>&text={}'.format(text_msg))
	if response.status_code == 200:
		print("success")

def add_to_spreadsheet_lme_tt(csp,bic,today,LME,sbi_tt_price):
	sheet = gc.open_by_key('<worksheet key>')
	worksheet = sheet.get_worksheet(3)
	body = csp,bic,today,LME,sbi_tt_price
	body = list(body)
	res = worksheet.append_row(body, table_range="A:C") 

def scraper():
	try:
		# scraping Lme 
		LME = 0
		sbi_tt_price = 0
		url = "https://metalradar.com/lme-prices/"
		page = requests.get(url,verify=False)
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find('table',class_='tLME').find_all('tr')[2].find_all('td')[1].text
		LME = float(results)
		# sbi tt price extraction

		url = "https://sbi.co.in"
		page = requests.get(url,verify=False)
		if page.status_code != 500:
			soup = BeautifulSoup(page.content, "html.parser")
			results = soup.find('ul',class_='list-unstyled').find_all('li')[0].find('a').get('href')
			link = url+str(results)
			print(link)
			# download pdf 
			pdf_loc = "static/sbi-tt-price.pdf"
			pdf_downloader(link,pdf_loc)
			reader = PdfReader('static/sbi-tt-price.pdf')

			page = reader.pages[0]
			text = page.extract_text()
			if check_for_today_date(text):
				page = reader.pages[1]
				text = page.extract_text()
				text = get_sbi_tt_price(text)
				sbi_tt_price = float(text)
				print(sbi_tt_price)
				print("sbi")
			else:
				# google usr-inr
				print("google")
				url = "https://google.com/search?q=usd+inr"
				driver = webdriver.Chrome('chromedriver',options=options)
				driver.get(url)
				time.sleep(5)
				data = driver.find_element(By.XPATH,'//*[@id="knowledge-currency__updatable-data-column"]/div[3]/div/div[2]/input').get_attribute('value')
				sbi_tt_price = (float(data) + 0.50)
				print(sbi_tt_price)
				driver.close()
		else:
			print("google")
			url = "https://google.com/search?q=usd+inr"
			driver = webdriver.Chrome('chromedriver',options=options)
			driver.get(url)
			time.sleep(5)
			data = driver.find_element(By.XPATH,'//*[@id="knowledge-currency__updatable-data-column"]/div[3]/div/div[2]/input').get_attribute('value')
			sbi_tt_price = (float(data) + 0.50)
			print(sbi_tt_price)
			driver.close()


		bic = ((((LME + 190) * 1.106 * sbi_tt_price) + 4250) / 1000)

		csp = ((((LME + 190) * 1.055 * sbi_tt_price) + 4250) / 1000)
		print(bic,csp)
		today = datetime.datetime.today().strftime("%d-%m-%Y")
		send_text_via_telegram(csp,bic,today,LME,sbi_tt_price)
		add_to_spreadsheet_lme_tt(csp,bic,today,LME,sbi_tt_price)
	except:
		pass

def scrape_and_send_screenshot():
	try:
		print("scraper running")
		scraper()
	except:
		scraper()
	

scrape_and_send_screenshot()

