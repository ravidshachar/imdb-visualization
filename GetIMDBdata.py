from bs4 import BeautifulSoup
from time import time,sleep
from random import randint
from IPython.core.display import clear_output
from requests import get

HEADERS = {"Accept-Language": "en-US, en;q=0.5"}
NUMBER_OF_REQUESTS = 3


def get_movie_dataframe(pages_number,year_url):
	pages = [str(i) for i in range(1,pages_number)]
	
	# Redeclaring the lists to store data in
	names = []
	years = []
	imdb_ratings = []
	metascores = []
	votes = []
	directors = []
	stars = []

	# Preparing the monitoring of the loop
	start_time = time()
	requests = 0

	# For every year in the interval 2000-2017
	for year_url in years_url:

		# For every page in the interval 1-4
		for page in pages:

			# Make a get request
			response = get('https://www.imdb.com/search/title?title_type=feature,tv_movie&release_date=' + year_url +
			'&sort=num_votes,desc&page=' + page, headers = HEADERS)

			# Pause the loop
			sleep(randint(4,8))

			# Monitor the requests
			requests += 1
			elapsed_time = time() - start_time
			print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))

			# Throw a warning for non-200 status codes
			if response.status_code != 200:
				print('Request: {}; Status code: {}'.format(requests, response.status_code))

			# Break the loop if the number of requests is greater than expected
			if requests > NUMBER_OF_REQUESTS:
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
					names.append(name)

					# Scrape the year
					year = container.h3.find('span', class_ = 'lister-item-year').text
					years.append(year)

					# Scrape the IMDB rating
					imdb = float(container.strong.text)
					imdb_ratings.append(imdb)

					# Scrape the Metascore
					m_score = container.find('span', class_ = 'metascore').text
					metascores.append(int(m_score))

					# Scrape the number of votes
					vote = container.find('span', attrs = {'name':'nv'})['data-value']
					votes.append(int(vote))
					
					directors.append(director)
					stars.append(star)

					#star = container.find('p')
		if requests > NUMBER_OF_REQUESTS:
			break
	print(stars)
	
def main:
	pages_number = 5
	years_url = [str(i) for i in range(2000,2018)]
	get_movie_dataframe(pages_number,year_url)
