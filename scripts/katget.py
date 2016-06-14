#!/usr/bin/env python3

import html.parser
import sys
import urllib.request
import io
import gzip

def main():
	if len(sys.argv) == 3:
		url = sys.argv[1]
		pages = int(sys.argv[2])
		parser = KickAssParser()
		parser.setup()

		#print("Downloading ", url)
		if not url.endswith("/"):
			url += "/"

		for page in range(1, pages + 1):
			if page > 1:
				if "user" in url:
					page_url = url + "?page=" + str(page)
				elif "usearch" in url:
					page_url = url + str(page)
				else:
					page_url = url
			else:
				page_url = url

			with urllib.request.urlopen(page_url) as response:
				if response.info().get('Content-Encoding') == 'gzip':
					#print("Decompressing...")
					buf = io.BytesIO(response.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = response.read()

				encoding = response.headers.get_content_charset()
				#print("Encoding: ", encoding)
				html_string = html.decode(encoding)
				#print("Parsing...")
				parser.feed(html_string)
	else:
		print("Usage: katget.py <url> <pages>")

class KickAssParser(html.parser.HTMLParser):

	def setup(self):
		self.level = 0
		self.isLink = False

	def handle_starttag(self, tag, attrs):
		self.level += 1

		if tag == "a":
			for attr in attrs:
				if attr[0] == "title" and attr[1] == "Torrent magnet link":
					self.isLink = True
				elif attr[0] == "href" and self.isLink == True:
					self.isLink = False
					self.link = attr[1]
					print(self.link)


	def handle_endtag(self, tag):
		self.level -= 1

if __name__ == '__main__':
	main()