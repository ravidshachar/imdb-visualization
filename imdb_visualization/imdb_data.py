from bs4 import BeautifulSoup
from time import time,sleep
from random import randint
import requests
import pandas as pd

HEADERS = {"Accept-Language": "en-US, en;q=0.5"}
NUMBER_OF_REQUESTS = 3
RESULTS_IN_A_PAGE = 50

def get_movie_dataframe(pages_number=2,years=[str(i) for i in range(2000,2002)]):
	record_lists = []
	pages = [i for i in range(1,pages_number+1)]
	start_time = time()
	requests_num = 0
	for year in years:

		# For every page in the interval 1-4
		for page in pages:

			# Make a get request
			current_start = str((RESULTS_IN_A_PAGE*(page-1))+1)
			response = requests.get('https://www.imdb.com/search/title?title_type=feature,tv_movie&release_date=' + year +
			'&sort=num_votes,desc&start=' + current_start 
			+ '&page=' + str(page), headers = HEADERS)

			# Pause the loop so that imdb won't block you
			sleep(randint(4,8))

			# Monitor the requests
			requests_num += 1
			elapsed_time = time() - start_time
			print('Request:{}; Frequency: {} requests/s'.format(requests_num, requests_num/elapsed_time))

			# Throw a warning for non-200 status codes
			if response.status_code != 200:
				print('Request: {}; Status code: {}'.format(requests_num, response.status_code))
			
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
					object_year = container.h3.find('span', class_ = 'lister-item-year').text
					movie_year = int(object_year[object_year.rfind("(") + 1:-1])

					# Scrape the IMDB rating
					imdb = float(container.strong.text)

					# Scrape the Metascore
					m_score = container.find('span', class_ = 'metascore').text
					m_score = int(m_score)
					
					# Scrape the number of votes and gross
					votes_and_gross = container.find_all('span', attrs = {'name':'nv'})
					vote,gross = [x['data-value'] for x in votes_and_gross 
									if len(votes_and_gross) == 2] or (votes_and_gross[0]['data-value'],None)
					vote = int(vote)
					
					#scrape director and actors
					director = container.find('p', class_ = '').find_all('a')[0].text
					actors = [x.text for x in container.find('p', class_ = '').find_all('a')[1:]]
					
					#scrape certificate, runtime and genre
					additional_information = container.find('p', class_ = 'text-muted')
					additional_information = (additional_information.find('span', class_ = 'certificate'),
					additional_information.find('span', class_ = 'runtime'),
					additional_information.find('span', class_ = 'genre'))
					certificate,length,genre = [x.text if x else None for x in additional_information ]
					
					length = int(length.replace(" min",""))
					
					
					#genre is a list
					genre = genre.strip().split(",")
					
					#prepre for data frame
					record_lists.append([name,movie_year,imdb,m_score,vote,director,actors,certificate,length,genre])
	df = pd.DataFrame(record_lists,columns=["name","year","rating","metascore","votes","director","actors","certificate","length","genre"])
	return df
	
if __name__ == "__main__":
	df = get_movie_dataframe()
	print(df.head().to_string())
	print(df.dtypes)