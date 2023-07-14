import asyncio
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from csv import DictReader

from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
import sqlite3
# import re

conn = sqlite3.connect('betburger.db')
#exception 
class NoBetException(Exception):
  """An exception raised when a list is empty."""
  def __init__(self, message):
    super().__init__(message)

# Create a cursor
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, EventName TEXT ,Link TEXT, value TEXT , sportname TEXT , BookerName TEXT , TimeOfMatch TEXT , Market TEXT , CurrentOdds TEXT , LastAcceptableOdds TEXT,New BOOLEAN,Updated BOOLEAN,onDelete BOOLEAN Default False,Deleted BOOLEAN)')


conn.commit()
#url of the page we want to scrape
# url = "https://www.betburger.com/users/sign_in"
url = "https://www.betburger.com"
  
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
# initiating the webdriver. Parameter includes the path of the webdriver.

driver = webdriver.Chrome('chromedriver',options=options)
driver.get(url)
time.sleep(3)

def get_cookies_values(file):
    with open(file,encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
    return list_of_dicts

cookies = get_cookies_values("cookie.csv")

for i in cookies:
    driver.add_cookie(i)
print("cookies uploading")
print("refreshing")
driver.refresh()

# email = "michalrauch@seznam.cz"
# password = "koqNit-1mizve-totsip"

# emailfield = driver.find_element(By.ID,"betburger_user_email")
# emailfield.send_keys(email)

# pwd = driver.find_element(By.ID,"betburger_user_password")
# pwd.send_keys(password)
# time.sleep(1)
# driver.execute_script("window.scrollBy(0, 400)")
# time.sleep(2)

# submit = driver.find_element(By.CLASS_NAME,"sign_in")
# submit.click()

time.sleep(5)
datatext = driver.find_element(By.CLASS_NAME,"green-btn").text
print(datatext)
if datatext == "Sign out":
    print("Login Successful")
else :
    print("login Failed")
    conn.close()
    driver.close()
    exit()

def New_Updated(conn,cursor,EventName,Link,value,sportname,BookerName,TimeOfMatch,Market,CurrentOdds,LastAcceptableOdds):
    cursor.execute(f"SELECT id,New from messages WHERE EventName = '{EventName}'")
    rows = cursor.fetchall()
    if len(rows) != 0:        
        for row in rows:
            if row:
                """If event match then updated and flag Message updated True"""
                if row[1] == True:
                    sql = f"UPDATE messages SET value = '{value}',EventName='{EventName}','Link' = '{Link}',sportname = '{sportname}',BookerName = '{BookerName}',TimeOfMatch = '{TimeOfMatch}',Market = '{Market}',CurrentOdds = '{CurrentOdds}',LastAcceptableOdds = '{LastAcceptableOdds}',New = True,Updated = False WHERE id = {row[0]}"
                else:
                    sql = f"UPDATE messages SET value = '{value}',EventName='{EventName}','Link' = '{Link}',sportname = '{sportname}',BookerName = '{BookerName}',TimeOfMatch = '{TimeOfMatch}',Market = '{Market}',CurrentOdds = '{CurrentOdds}',LastAcceptableOdds = '{LastAcceptableOdds}',Updated = True WHERE id = {row[0]}"
                
                cursor.execute(sql)
                conn.commit()
                print("Updated")
           
    else:
        sql = f"INSERT INTO messages (value,EventName,sportname,BookerName,TimeOfMatch,Market,CurrentOdds,LastAcceptableOdds,New,Updated,onDelete,Deleted) VALUES ('{value}','{EventName}','{sportname}','{BookerName}','{TimeOfMatch}','{Market}','{CurrentOdds}','{LastAcceptableOdds}',True,False,False,False);"
        cursor.execute(sql)
        conn.commit()   
        print("Inserted")

def onDelete(conn,cursor):
    cursor.execute(f"SELECT id,New from messages WHERE New = False AND Updated = False And Deleted != True")
    rows = cursor.fetchall()
    if len(rows) != 0:        
        for row in rows:
            sql = f"UPDATE messages SET onDelete = True WHERE id = {row[0]}"
            cursor.execute(sql)
            conn.commit()

def remove_whitespaces(string):
  """Removes whitespaces from a string."""
  string = str(string)
  return string.replace("  ", "").replace("\n", "")

def remove_link_chars(string):
    string = str(string)
    return string.replace("%","")

print("Scraping Started")
while True:   
    scrape_url = "https://www.betburger.com/arbs"
    driver.get(scrape_url) 
    time.sleep(5)  
    html = driver.page_source
    # this renders the JS code and stores all
    # of the information in static HTML code.
    soup = bs4.BeautifulSoup(html, "html.parser")
    lists = soup.find_all("li",{'class':'arb'})
    try:
        if len(lists) == 0:
            raise NoBetException("NOBET")

        for list in lists:
            value = list.find("span",{'class':'percent'}).get_text()
            sportname = list.find("span",{"class":"sport-name"}).get_text()
            gameperiod = list.find("div",{'class':'arb-game-period'})
            if gameperiod.span is not None:
                gameperiod = gameperiod.span.get_text()
            else:
                gameperiod = ""
            OppositionName = list.find_all("div",{'class':'bookmaker-name'})[0].get_text()
            BookerName = list.find_all("div",{'class':'bookmaker-name'})[1].get_text()
            EventName = list.find_all("div",{'class':'event-name'})[1].div.a.get_text()
        
            # Link = list.find_all("div",{'class':'event-name'})[1].div.a.get("href")
            Link = list.find_all("a",{'class':'coefficient-link'})[1].get("href")
            Link = "https://www.betburger.com" + Link
            Link = remove_whitespaces(Link)
            Link = remove_link_chars(Link)

            driver.get(Link)
            time.sleep(5)
            link = driver.current_url
            

            if link is None:
                driver.get(Link)
                time.sleep(5)

            Link = '("'+str(driver.current_url)+'")'
            
            Link = remove_link_chars(Link)

            TimeOfMatch = list.find("div",{'class':'date'}).get_text()
            Market = list.find("div",{'class':'market'}).a.span.get_text()

            if gameperiod=="":
                Market = Market
            else:
                Market = Market+" + "+gameperiod
            CurrentOdds = list.find_all("a",{'class':'coefficient-link'})[1].get_text()
            lao = list.find_all("a",{'class':'coefficient-link'})[0].get_text()
            lao = float(lao)
            LastAcceptableOdds = 1/((1/(0.005+1))-(1/lao))
            value = remove_whitespaces(value)
            EventName = remove_whitespaces(EventName)
            OppositionName = remove_whitespaces(OppositionName)
            Link = remove_whitespaces(Link)
            sportname = remove_whitespaces(sportname)
            BookerName  = remove_whitespaces(BookerName)
            TimeOfMatch = remove_whitespaces(TimeOfMatch)
            Market = remove_whitespaces(Market)
            CurrentOdds = remove_whitespaces(CurrentOdds)
            LastAcceptableOdds = remove_whitespaces(LastAcceptableOdds)
            LastAcceptableOdds = round(float(LastAcceptableOdds), 2)
            if (BookerName != "Pinnacle") or (OppositionName != "Pinnacle"):
                if Link is not None:
                    New_Updated(conn,cursor,EventName,Link,value,sportname,BookerName,TimeOfMatch,Market,CurrentOdds,LastAcceptableOdds)           
            onDelete(conn,cursor)
            time.sleep(10)
    except KeyboardInterrupt:
        print("keyboard Interrupt")
        exit()
    except NoBetException:
        print("no bet")
    except:
        print("some exception")


conn.close()
driver.close() # closing the webdriver