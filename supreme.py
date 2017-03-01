
import mechanize
import cookielib
import re
import json
import time
#from datetime import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


#Load json data
with open('info.json') as data_file:
    data = json.load(data_file)

#open browser
br = mechanize.Browser()
browser = webdriver.Firefox()
browser.get("http://supremenewyork.com/shop/all/" + data["subsection"])


def findItem(color, keywords):
    #Opens page to the hats --change to desired item
    supremeShop = br.open("http://www.supremenewyork.com/shop/all/" + data["subsection"])
    htmlShop = supremeShop.read()
    #Going to have to edit this to refresh the page unless it gets a result
    link = [""]
    start = time.time()
    regex = re.compile(keywords+'.{0,100}'+color) #first find the objects which contain the adjectives
    regexUrl = re.compile('\/shop\/[a-zA-Z0-9\/]*') #this will then find the link in the previously found strings
    while link[0] == "":
        loopTime = int(time.time() - start)
        if loopTime%15 == 0:
            print "Searching again"
            roughLink = re.findall(regex, htmlShop) # find rough outline of link
            try: # This is a terrible way to get around trying to fill an array with null when the regex finds nothing
                link = re.findall(regexUrl, roughLink[0])
                break
            except IndexError:
                browser.refresh()
                link[0] = ""
                br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
                htmlShop = supremeShop.read()
    return 'http://www.supremenewyork.com' + link[0]


while int(time.strftime("%H")) < 8: # Stalls until hour = 8 am
    word = "hey"
while int(time.strftime("%M")) < 59:    #stalls until time = 8:59 am
    word = "nay" # cant have an empty block so added this shit
browser.get(findItem(data["color"], data["keyword"])) #Open the newly found link
wait = WebDriverWait(browser, 2)

def pickSize(size): #Need to modify to actually select size might need to use regex
    if size != 'os':
        sizeList = browser.find_element_by_name("size")
        sizeList.send_keys(size)

def addToCart():
    cart = browser.find_element_by_name('commit')  # Find the search box
    cart.click()
    checkout = browser.find_element_by_link_text("checkout now")
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "checkout now")))
    checkout.click();

def checkOut():
    wait.until(EC.visibility_of_element_located((By.ID, "order_billing_name"))) # need to add all of this stuff into a for loop to lazy to do it right now
    #Temporary yet completely permanent patch together
    info = browser.find_element_by_id("order_billing_name")
    info.send_keys(data["name"])
    info = browser.find_element_by_id("order_email")
    info.send_keys(data["email"])
    info = browser.find_element_by_id("order_tel")
    info.send_keys(data["tel"])
    info = browser.find_element_by_id("bo")
    info.send_keys(data["address"])
    info = browser.find_element_by_id("zip_label")
    info.send_keys(data["zip"])
    info = browser.find_element_by_id("order_billing_city")
    info.send_keys(data["city"])
    info = browser.find_element_by_id("state_label")
    info.send_keys(data["state"])
    info = browser.find_element_by_id("credit_card_type")
    info.send_keys(data["type"])
    info = browser.find_element_by_id("cnb")
    info.send_keys(data["number"])
    info = browser.find_element_by_id("credit_card_month")
    info.send_keys(data["month"])
    info = browser.find_element_by_id("credit_card_year")
    info.send_keys(data["year"])
    info = browser.find_element_by_id("vval")
    info.send_keys(data["cvv"])
    info = browser.find_element_by_id("order_terms")
    info.click()




pickSize(34)
addToCart()
checkOut()
