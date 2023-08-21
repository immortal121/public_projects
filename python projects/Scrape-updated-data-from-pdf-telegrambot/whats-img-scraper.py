
#pip install schedule
#pip install PyMuPDF
#pip install bs4
# pip install requests

#tmux
#tmux ls
#tmux -a -t 0
# crontab -e
# 0 10 * * *
# 0 15 * * *
import requests
from bs4 import BeautifulSoup
import fitz
import time
import schedule

def send_img_via_telegram():
	# send via telegram
	files = {'photo':open('./static/new_img.png','rb')}
	response = requests.post('https://api.telegram.org/<bot token>/sendPhoto?chat_id=<chatid>',files=files)
	if response.status_code == 200:
		print("success")

def scraper():
	# page scraper #
	url = "https://www.hindalco.com/our-businesses/aluminium-overview/primary-aluminium/primary-metal-price"

	URL = "https://www.hindalco.com/our-businesses/aluminium-overview/primary-aluminium/primary-metal-price"
	page = requests.get(URL,verify=False)

	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find_all('ul')[1].find_all('li')[0].find('a').get("href")
	link = "https://www.hindalco.com"+str(results)
	# download pdf 
	base_url = link

	response = requests.get(base_url, verify=False)

	with open('./static/new_pdf.pdf', 'wb') as f:
		 f.write(response.content)

	# making pdf image

	pdffile = "./static/new_pdf.pdf"
	doc = fitz.open(pdffile)
	zoom = 4
	mat = fitz.Matrix(zoom, zoom)
	count = 0
	# Count variable is to get the number of pages in the pdf
	for p in doc:
		count += 1
	for i in range(count):
		val = "./static/new_img.png"
		page = doc.load_page(i)
		pix = page.get_pixmap(matrix=mat)
		pix.save(val)
	doc.close()

def scrape_and_send_screenshot():
	try:
		print("scraper running")
		scraper()
	except:
		scraper()
	try:
		print("sending msg")
		send_img_via_telegram()
	except:
		pass
		send_img_via_telegram()



schedule.every().day.at("13:4").do(scrape_and_send_screenshot)

schedule.every().day.at("15:00").do(scrape_and_send_screenshot)

while True:
  schedule.run_pending()
  time.sleep(5)
