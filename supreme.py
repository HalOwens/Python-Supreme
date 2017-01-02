
import mechanize
import cookielib
import re
import json
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
    #Going to have to edit this to refresh the page unless it gets a result
    htmlShop = supremeShop.read()
    regex = re.compile(keywords+'.{0,100}'+color) #first find the objects which contain the adjectives
    roughLink = re.findall(regex, htmlShop)
    regexUrl = re.compile('\/shop\/[a-zA-Z0-9\/]*') #this will then find the link in the previously found strings
    link = re.findall(regexUrl, roughLink[0])
    return 'http://www.supremenewyork.com' + link[0]


browser.get(findItem("Blue", "Animal")) #Open the newly found link
wait = WebDriverWait(browser, 10)

def pickSize(size): #Need to modify to actually select size might need to use regex
    if size != 'os':
        sizeList = browser.find_element_by_name("size")
        sizeList.send_keys(Keys.ARROW_DOWN)


def addToCart():
    cart = browser.find_element_by_name('commit')  # Find the search box
    cart.click()
    checkout = browser.find_element_by_link_text("checkout now")
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "checkout now")))
    checkout.click();

def checkOut():
    wait.until(EC.visibility_of_element_located((By.ID, "order_billing_name")))
    info = browser.find_element_by_id("order_billing_name")
    info.send_keys(data["name"])
    info = browser.find_element_by_id("order_email")
    info.send_keys(data["email"])
    info = browser.find_element_by_id("order_tl")
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



pickSize("Large")
addToCart()
checkOut()
#for i in link:
#    print i
#link.send_keys(Keys.TAB)
#link.send_keys(Keys.TAB) #To find the add to cart button which is initially hiden i go to the button before it in the tab order and tab over
#link.send_keys(Keys.ENTER)

#browser.quit()







'''
MECHANIZE

Hal Owens
Supreme Bot using Mechanize: http://wwwsearch.sourceforge.net/mechanize/
Useful Links:
http://www.pythonforbeginners.com/mechanize/browsing-in-python-with-mechanize/
http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/


https://pypi.python.org/pypi/selenium
https://github.com/mozilla/geckodriver/releases

    WHAT TO DO TO GET THE ITEM YOU WANT
    Change value of supremeShop website variable to equal section of shop with item
    change color/description in regex

import mechanize
import cookielib
import re


#open browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
# Makes robot look like a fedora machine running firefox to bypass bot protections
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#Uncomment for debugging messages
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)


#Opens page to the hats --change to desired item
supremeShop = br.open("http://www.supremenewyork.com/shop/all/hats")
#Going to have to edit this to refresh the page unless it gets a result
htmlShop = supremeShop.read()
regex = re.compile('Glossy.{0,100}Royal') #first find the objects which contain the adjectives
roughLink = re.findall(regex, htmlShop)
regexUrl = re.compile('\/shop\/[a-zA-Z0-9\/]*') #this will then find the link in the previously found strings
link = re.findall(regexUrl, roughLink[0])
productpage = br.open("http://www.supremenewyork.com" + link[0])
print br.geturl()
br.select_form(nr=0)
br.submit()
tempHtml = productpage.read()
print tempHtml
regexTemp = re.compile('class="logo".{0,500}') ##MAKE REGEX TO FIND OUT IF PRODUCT IS IN CART
status = re.findall(regexTemp, tempHtml)
print status
'''
