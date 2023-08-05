#! python3
"""
http://manhua.dmzj.com/fklmfsnyly/

"""

import re
from urllib.parse import urljoin

from node_vm2 import eval

from ..core import Episode

domain = ["manhua.dmzj.com"]
name = "動漫之家"

def get_title(html, url):
	return re.search("<h1>(.+?)</h1>", html).group(1)

def get_episodes(html, url):
	comicurl = re.search("comic_url = \"(.+?)\"", html).group(1)
	pattern = (
		r'href="(/{}[^"]+)" (?: class="color_red")?>(.+?)</a>\s*</li>'
			.format(comicurl)
	)
	s = []
	for match in re.finditer(pattern, html):
		ep_url, title = match.groups()
		s.append(Episode(title, urljoin(url, ep_url)))
	return s

def get_images(html, url):
	# Set base url
	base = "http://images.dmzj.com/"

	# Get urls
	html = html.replace("\n", "")
	s = re.search(r"page = '';\s*(.+?);\s*var g_comic_name", html).group(1)
	pages = eval(s + "; pages")
	pages = eval(pages)

	# thumbs.db?!
	# http://manhua.dmzj.com/zhuoyandexiana/3488-20.shtml
	return [base + page for page in pages if page and not page.lower().endswith("thumbs.db")]
