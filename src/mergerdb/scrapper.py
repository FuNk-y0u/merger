from src.inc import *
from src.mergerdb.torrent_cli import TorrentCLI


class Scrapper:
	def __init__(self):
		self.url = os.getenv("YTS_URL")

		#NOTE: ':' is removed
		self.not_allowed = ["\\","/",'"',"<",">","|"]

		self.torrent_cli = TorrentCLI(
			os.getenv("TORRENT_DEV_URL"),
			os.getenv("TORRENT_USERNAME"),
			os.getenv("TORRENT_PASSWORD")
		)

	def scrape(self, movie_name: str) -> list[dict]:
		movies = {}
		movie_links = self.search_movies(movie_name)

		for link in movie_links:
			movie = self.scrape_movie(link)
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
			try:
				download_title = f"Download {title} 720p.WEB Torrent"
				return soup.find(title = download_title)["href"]
			except:
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

	def download_movie(self, movie: dict):
		torrent_filename = f"{movie['title']}.torrent"

		# Downloading torrent file
		torrent_file = requests.get(movie["torrent_url"], allow_redirects = True)
		open(torrent_filename, "wb").write(torrent_file.content)

		self.torrent_cli.download_from_file(torrent_filename)
