

# Function to scrape data from website

def scrape():
	
	# Dependencies
	from bs4 import BeautifulSoup
	import requests
	from splinter import Browser
	import pandas as pd
	import time

		
	### NASA Mars News ###
	
	# Opening the chrome browser using Splinter
	executable_path = {'executable_path': 'chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)

	# URL of the website that needs to be scraped
	news_url = 'https://mars.nasa.gov/news/'
	
	# Visiting the url
	browser.visit(news_url)

	# Fetching the html of the web page
	html = browser.html

	# Parse HTML with Beautiful Soup
	soup = BeautifulSoup(html, 'html.parser')

	# Scrape News Title
	news_title = soup.find('div', class_='content_title').a.text
	print(news_title)

	# Scrape News Paragraph
	news_paragraph = soup.find('div', class_='article_teaser_body').text
	print(news_paragraph)


	
	### JPL Mars Space Images - Featured Image ###
	

	# url of website that needs to be scraped
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	# Visiting the url
	browser.visit(url)

	# Clicking the link - 'Full Image' on the page
	try:
		browser.click_link_by_partial_text('FULL IMAGE')
	except Exception as e:
		print("Exception Occured :",e)

	# Clicking the link - 'more info' on the page
	time.sleep(10)
	try:
		browser.click_link_by_partial_text('more info')
	except Exception as e:
		print("Exception Occured :",e)
		

	# Fetching the html of the web page
	html = browser.html
	# Parse HTML with Beautiful Soup
	soup = BeautifulSoup(html, 'html.parser')
	# Retrieve all elements that contain book information
	full_image_url = soup.find_all('img', class_='main_image')[0]['src']


	# Full URL of the Featured Image on the web page
	featured_image_url = 'https://www.jpl.nasa.gov' + full_image_url
	print(featured_image_url)
	

	### Mars Weather ###
	
	# URL of page to be scraped
	weather_url = 'https://twitter.com/marswxreport?lang=en'

	# Retrieve page with the requests module
	response = requests.get(weather_url)

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = BeautifulSoup(response.text, 'html.parser')

	# scraping relevant element from the result
	result = soup.find_all('div', class_="js-tweet-text-container")[0]

	# Scraping Mars Weather Tweet
	weather = result.p.text

	# Removing picture text from tweet
	weather = weather.split('pic.twitter.com/')

	# Latest Mars Weather Tweet
	mars_weather = weather[0]
	print(mars_weather)


	### Mars Facts ###
	
	# URL of page to be scraped
	facts_url = 'https://space-facts.com/mars/'

	# Pandas to scrape the table containing facts about the planet
	tables = pd.read_html(facts_url)
	
	# Fetching only first table of the page
	df = tables[0]

	# Rename column names
	df_new = df.rename(columns={0:'Description',1:'Values'})

	# Creating an index on 'Description' column
	df_new.set_index('Description', inplace=True)

	# Use Pandas to convert the data to a HTML table string
	html_table = df_new.to_html()

	# Strip unwanted newlines to clean up the table
	facts_table = html_table.replace('\n', '')
	print(facts_table)
	

	### Mars Hemispheres ###
	
	# URL of page to be scraped
	hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

	# Retrieve page with the requests module
	response = requests.get(hemispheres_url)

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = BeautifulSoup(response.text, 'html.parser')
	#print(soup.prettify())

	# Visiting the USGS Astrogeology site here to scrape high resolution images & title for each of Mar's hemispheres.

	# Finding all the headings in the main page
	headings = soup.find_all('h3')

	# List of hemisphere dictionaries
	hemisphere_list = []

	# Looping through each of the the heading links via splinter
	for heading in headings:
    
		print(heading.text)
		browser.visit(hemispheres_url)
		
		try:
			# Clicking each of the links to the hemispheres in order to find the image url to the full resolution image.
			browser.click_link_by_partial_text(heading.text)
			html = browser.html
			# Parse HTML with Beautiful Soup
			soup = BeautifulSoup(html, 'html.parser')
			# Scraping the full resolution image from the navigated page
			result_image = soup.find('div',class_='downloads').ul.a['href']
			img_url = result_image
			print(img_url)
			# Scraping the hemisphere title from the navigated page
			title = soup.find('h2',class_='title').text
			print(title)
			print("-"*20)
			
			# Dictionary to store image url and title
			mars_hemispheres = {
							   'title' : title, 
							   'img_url':img_url
							   }
			# Adding each hemisphere info to the list
			hemisphere_list.append(mars_hemispheres)
			
		except Exception as e:
			print("Exception Occured :",e)
	
	
	# Dictionary of scraped data
	scraped_data_dictionary = { 'news_title': news_title, 'news_paragraph':news_paragraph, 'featured_image_url':featured_image_url, 'mars_weather':mars_weather, 'facts_table':facts_table, 'hemisphere_list':hemisphere_list}
	
	return scraped_data_dictionary


