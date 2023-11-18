from utils.inc import *

class Scrapper:
	def __init__(self, username: str, password: str):
		self.url = "https://www.filemoon.sx/"
		self.username = username
		self.password = password

		self.headers = {
			"Accept": "*/*",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": "0",
			"Connection": "keep-alive",
			"Host": "www.filemoon.sx"
		}

		self.cookies = {
			"lang": "1",
			"login": self.username,
			"login_1st": "",
			"msg": "",
			"per_page": "",
			"upload_mode": "file",
			"mas": "2",
			"xfsts": ""
		}

		self.session = requests.Session()

	def scrape_url(self, file_name: str) -> str:
		content = self.__get_videos_page()
		soup = BeautifulSoup(content, "html.parser")
		url = self.__find_video_url(file_name, soup)
		return url

	def __login(self):
		payload = {
			"b": "login",
			"redirect": "",
			"login": self.username,
			"password": self.password
		}

		xform_payload = self.__convert_json_to_xform(payload)
		self.headers.update({ "Content-Length": str(len(xform_payload)) })

		self.session.post(
			f"{self.url}login",
			headers = self.headers,
			data = xform_payload
		)
		self.cookies.update(self.session.cookies.get_dict())

	def __get_videos_page(self) -> str:
		self.__login()

		res = self.session.get(
			f"{self.url}videos",
			cookies = self.cookies
		)
		return res.text

	def __extract_id_from_rows(self, file_name: str, rows: list[Tag]) -> str:
		for row in rows:
			anchors = row.find_all("a")
			for a in anchors:
				url = a["href"]
				if file_name in url:
					id = url.split("/")[4]
					return id

	def __find_video_url(self, file_name: str, soup: BeautifulSoup) -> str:
		tables = soup.find_all("table")

		for table in tables:
			body = table.find("tbody")
			tds = body.find_all("td")
			id = self.__extract_id_from_rows(file_name, tds)

			if not id: return id

			url = f"{self.url}e/{id}"
			return url

	def __convert_json_to_xform(self, data: dict) -> str:
		return "&".join([f"{key}={data[key]}" for key in data])
