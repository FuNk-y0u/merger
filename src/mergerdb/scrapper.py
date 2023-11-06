from src.inc import *

class Scrapper:
	def __init__(self):
		self.url = os.getenv("YTS_URL")

		#NOTE: ':' is removed
		self.not_allowed = ["\\","/",'"',"<",">","|"]

	def scrape(self, movie_name: str) -> list[dict]:
		movies = {}
		movie_links = self.search_movies(movie_name)

		for link in movie_links:
			movie = self.scrape_movie(link)
			print(movie)
			if movie["title"] and movie["poster_url"] and movie["torrent_url"]:
				movies.update({
					str(uuid.uuid4()): {
						"title"      : movie["title"],
						"poster_url" : movie["poster_url"],
						"torrent_url": movie["torrent_url"]
					}
				})

		return movies

	def search_movies(self, movie_name: str) -> list[str]:
		movie_name = movie_name.replace(" ", "%20")
		url = f"{self.url}/browse-movies/{movie_name}/all/all/0/latest/0/all"

		response = requests.get(url)

		# Collecting all the movie links
		soup = BeautifulSoup(response.text, "html.parser")
		rows = soup.find_all("div", { "class": "browse-movie-bottom" } )

		movies = []
		#NOTE: Hardcoded to only 5 results
		for row in rows[:5:]:
			movies.append(str(row.find("a")["href"]))

		return movies

	def scrape_movie(self, movie_link: str) -> dict:
		print(f"Scrapping link: {movie_link}")

		def __get_title(soup: BeautifulSoup) -> str:
			try:
				temp_title = soup.find(id = "movie-info").find("h1").text
				title = "".join([c if c not in self.not_allowed else " " for c in temp_title])
				return title
			except:
				return None

		def __get_poster_url(soup: BeautifulSoup) -> str:
			try:
				return soup.find(id = "movie-poster").find("img")["src"]
			except:
				return None

		def __get_torrent_url(soup: BeautifulSoup, title: str) -> str:
			fmts = ["WEB", "BluRay"]
			for fmt in fmts:
				download_title = f"Download {title} 720p.{fmt} Torrent"
				anchor = soup.find(title = download_title)
				if anchor: return anchor["href"]

			return None

		response = requests.get(movie_link)
		soup = BeautifulSoup(response.text, "html.parser")

		title       = __get_title(soup)
		poster_url  = __get_poster_url(soup)
		torrent_url = __get_torrent_url(soup, title)

		return {
			"title"      : title,
			"poster_url" : poster_url,
			"torrent_url": torrent_url
		}
