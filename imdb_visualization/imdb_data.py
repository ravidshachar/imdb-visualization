from bs4 import BeautifulSoup
from time import time,sleep
from random import randint
import requests
import pandas as pd

HEADERS = {"Accept-Language": "en-US, en;q=0.5"}
NUMBER_OF_REQUESTS = 3

def get_movie_dataframe(pages_number=4,years=[str(i) for i in range(2000,2018)]):
	record_lists = []
	pages = [str(i) for i in range(1,pages_number)]

	# Preparing the monitoring of the loop
	start_time = time()
	requests_num = 0

	# For every year in the interval 2000-2017
	for year in years:

		# For every page in the interval 1-4
		for page in pages:

			# Make a get request
			response = requests.get('https://www.imdb.com/search/title?title_type=feature,tv_movie&release_date=' + year +
			'&sort=num_votes,desc&page=' + page, headers = HEADERS)

			# Pause the loop so that imdb won't block you
			sleep(randint(4,8))

			# Monitor the requests
			requests_num += 1
			elapsed_time = time() - start_time
			print('Request:{}; Frequency: {} requests/s'.format(requests_num, requests_num/elapsed_time))

			# Throw a warning for non-200 status codes
			if response.status_code != 200:
				print('Request: {}; Status code: {}'.format(requests_num, response.status_code))

			# Break the loop if the number of requests is greater than expected
			if requests_num > NUMBER_OF_REQUESTS:
				print('Number of requests was greater than expected.')
				break
			
			# Parse the content of the request with BeautifulSoup
			page_html = BeautifulSoup(response.text, 'html.parser')

			# Select all the 50 movie containers from a single page
			mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
			# For every movie of these 50
			for container in mv_containers:
				# If the movie has a Metascore, then:
				if container.find('div', class_ = 'ratings-metascore') is not None:

					# Scrape the name
					name = container.h3.a.text

					# Scrape the year
					movie_year = container.h3.find('span', class_ = 'lister-item-year').text

					# Scrape the IMDB rating
					imdb = float(container.strong.text)

					# Scrape the Metascore
					m_score = container.find('span', class_ = 'metascore').text

					# Scrape the number of votes
					vote = container.find('span', attrs = {'name':'nv'})['data-value']
					
					director = container.find('p', class_ = '').find_all('a')[0].text
					actors = [x.text for x in container.find('p', class_ = '').find_all('a')[1:]]
					
					record_lists.append([name,movie_year,imdb,m_score,vote,director,actors])

					#star = container.find('p')
		if requests_num > NUMBER_OF_REQUESTS:
			break
	df = pd.DataFrame(record_lists,columns=["name","year","imdb_rating","metascore","votes","director","actors"])
	return df
	
if __name__ == "__main__":
	print(get_movie_dataframe().head().to_string())