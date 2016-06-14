#!/usr/bin/env python3

# katget.py - Quick and dirty Python 3 script to extract magnet links from KAT
# user/seach pages.
#
# Usage: ./katget.py <url> <number of pages>
#
# Make sure to link to the first page of user uploads or search results, or
# the script will not work!
#
# ~ Malintent

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

			# Decompress data if gzipped
			with urllib.request.urlopen(page_url) as response:
				if response.info().get('Content-Encoding') == 'gzip':
					buf = io.BytesIO(response.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = response.read()

				# Convert byte data to string
				encoding = response.headers.get_content_charset()
				html_string = html.decode(encoding)
				parser.feed(html_string)
	else:
		print("Usage: katget.py <url> <pages>")

class KickAssParser(html.parser.HTMLParser):

	def __init__(self):
		html.parser.HTMLParser.__init__(self)
		self.level = 0
		self.isLink = False

	def handle_starttag(self, tag, attrs):
		self.level += 1

		if tag == "a":
			for key, value in attrs:
				if key == "title" and value == "Torrent magnet link":
					self.isLink = True
				elif key == "href" and self.isLink == True:
					self.isLink = False
					self.link = value
					print(self.link)


	def handle_endtag(self, tag):
		self.level -= 1

if __name__ == '__main__':
	main()
