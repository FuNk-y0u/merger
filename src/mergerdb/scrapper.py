from src.inc import *


class SubtitleScrapper:
	def __init__(self):
		self.url = os.getenv("OPENSUBTITLE_URL")

	def scrape(self, imdb_id: str) -> str:
		page: BeautifulSoup = self.__get_download_page(imdb_id)
		url = self.__select_eng_url(page)
		return url

	def __get_download_page(self, imdb_id: str) -> BeautifulSoup:
		id = imdb_id.strip("tt")
		url = f"{self.url}/en/search/sublanguageid-all/imdbid-{id}"
		response = requests.get(url)
		return BeautifulSoup(response.text, "html.parser")

	def __select_eng_url(self, page: BeautifulSoup) -> str:
		table = page.find(id = "search_results")
		rows = table.find_all("tr", { "class": "change" })[1:]

		for row in rows:
			tds = row.find_all("td")
			lang = tds[1].find("a")["title"]
			if lang == "English":
				return self.url + tds[4].find("a")["href"]
		return None


class Scrapper:
	def __init__(self):
		self.url = os.getenv("YTS_URL")

		self.subtitle_scrapper = SubtitleScrapper()

		#NOTE: ':' is removed
		self.not_allowed = ["\\","/",'"',"<",">","|"]

	def scrape(self, movie_name: str) -> list[dict]:
		movies = {}
		movie_links = self.search_movies(movie_name)

		for link in movie_links:
			movie = self.scrape_movie(link)
			if movie["title"] and movie["poster_url"] and movie["torrent_url"]:
				movies.update({
					str(uuid.uuid4()): {
						"title"       : movie["title"],
						"poster_url"  : movie["poster_url"],
						"torrent_url" : movie["torrent_url"],
						"subtitle_url": movie["subtitle_url"],
						"description" : movie["description"]
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

		def __get_subtitle_url(soup: BeautifulSoup) -> str:
			anchor = soup.find(title = re.compile("Download Subtitles"))
			if not anchor: return None

			imdb_id = anchor["href"].split("/")[-1]
			url = self.subtitle_scrapper.scrape(imdb_id)
			return url

		def __get_description(soup: BeautifulSoup) -> str:
			synopsis = soup.find(id = "synopsis")
			if not synopsis: return None

			paragraph = synopsis.find_all("p")[0]
			return paragraph.text

		response = requests.get(movie_link)
		soup = BeautifulSoup(response.text, "html.parser")

		title        = __get_title(soup)
		poster_url   = __get_poster_url(soup)
		torrent_url  = __get_torrent_url(soup, title)
		subtitle_url = __get_subtitle_url(soup)
		description  = __get_description(soup)

		return {
			"title"       : title,
			"poster_url"  : poster_url,
			"torrent_url" : torrent_url,
			"subtitle_url": subtitle_url,
			"description" : description
		}

