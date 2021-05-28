# -*- coding: utf-8 -*-
#
#								ﻢﻴﺣﺮﻟا ﻥﺎﻤﺣﺮﻟا ﻪﻠﻟا ﻢﺳﺎﺑ
#						ﺮﻳﺪﻗ ءﻲﺷ ﻞﻛ ﻰﻠﻋ ﻮﻫ ﻭ ﻚﻠﻤﻟا ﻪﻟ ﻞﻛﻮﺘﻧ ﻪﻴﻠﻋ
#
####################################################################################
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import os
import requests
import random
import datetime as dt
import codecs
import pickle

####################################################################################
tmin=6
tmax=15
t1=8
t2=20
####################################################################################


####################################################################################
print('Initializing Profile...\n')
print('-----------------------------------------------------------------')
#SELENIUM ENTRIES
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
cap['acceptInsecureCerts'] = True
binary = FirefoxBinary('/usr/bin/firefox')
##
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--load-images=no')
options.add_argument("window-size=1400,600")
options.add_argument("user-data-dir=/tmp/tarun")
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--proxy-server=%s' % proxy)
##
profile = webdriver.FirefoxProfile()
#profile.set_preference("general.useragent.override", "[user-agent string]")
profile.set_preference("general.useragent.override", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0")
####################################################################################
url='https://en.trendyol.com'
#
driver = webdriver.Firefox(profile,options = options,capabilities=cap,firefox_binary=binary)
driver.set_page_load_timeout(np.random.randint(5,10))
driver.get(url)

attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
 Belgium_flag)

#driver.find_elements_by_xpath("//img[@alt='Belgium']")
images = driver.find_elements_by_tag_name('img')
#for image in images:
#    print(image.get_attribute('alt'))

# BELGIUM FLAG
Belgium_flag=images[1]
action = webdriver.ActionChains(driver)

# CLICK ON BELGIUM
action.move_to_element(Belgium_flag).click().perform()

# GET ALL RUBRIKS
#Rubriks=driver.find_elements_by_xpath("//span[contains(concat(' ', normalize-space(@class), ' '), 'image-container')]")
#Rubriks=driver.find_elements_by_xpath("//article[contains(concat(' ', normalize-space(@class), ' '), 'component-item')]")

# CHOOSE A RUBRIK
rubrik_url='https://en.trendyol.com/sr?tag=influencerpicks#banner3enweb'
driver.get(rubrik_url)

# FIND ALL ARTICLES
articles=driver.find_elements_by_xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'p-card-chldrn-cntnr')]")
articles_links=[a.find_element_by_css_selector('a').get_attribute('href') for a in articles]

#BUILD DATABSE OF ALL ARTICLE // LOOP ON 10 ARTICLES
data_all=[]

for article in articles_links[:10]:
	# GO TO ARTICLE PAGE
	#article=articles_links[0]
	article_title=previous_price=actual_price=ratings='N/A'
	print('Visting Page:',article)
	driver.get(article)
	time.sleep(np.random.randint(t1,t2))
	try:
		# GET ARTICLE COMPONENTS
		elem=driver.find_element_by_xpath("//h1[@class='pr-new-br']")
		article_title=elem.text
		
		elem=driver.find_element_by_xpath("//span[@class='prc-org']")
		previous_price=elem.text
		
		elem=driver.find_element_by_xpath("//span[@class='prc-slg']")
		actual_price=elem.text
		
		elem=driver.find_element_by_xpath("//span[@class='rvw-cnt-tx international']")
		ratings=elem.text
		print('Components imported')
	except:
		pass
	#SAVE DATA
	data = {
	'Article Title':article_title,
	'Article Previous Price':previous_price,
	'Article Actual Price':actual_price,
	'Number of ratings':ratings,
	}
	##
	data_all.append(data)
	#
	print('-----------------------------------------------------------------')
	print('Saving to file in case\n')
	filename = 'data_lst.txt'
	outfile = open(filename,'wb')
	pickle.dump(data_all,outfile)
	outfile.close()
	# GO BACK
	#print('Go')
	#driver.back()
	print('Next Item:')
	time.sleep(np.random.randint(tmin,tmax))

## WRITE DATABASE INTO PANDAS
df_data=pd.DataFrame(data_all)
df_data.to_csv('data.csv')


f = codecs.open("page_source.txt", "w", "utf−8")
h = driver.page_source
f.write(h)

#
#
#
#