'''
Hal Owens
Supreme Bot using Mechanize: http://wwwsearch.sourceforge.net/mechanize/
Useful Links:
http://www.pythonforbeginners.com/mechanize/browsing-in-python-with-mechanize/
http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/

'''
''' WHAT TO DO TO GET THE ITEM YOU WANT
    Change value of supremeShop website variable to equal section of shop with item
    change color/description in regex
'''
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
