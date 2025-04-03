├── .flake8
├── .github
    └── workflows
    │   └── python-package.yml
├── .gitignore
├── LICENSE
├── MANIFEST.in
├── Makefile
├── README.md
├── README.rst
├── oobt
    └── oobt.py
├── requirements.txt
├── serpapi
    ├── __init__.py
    ├── apple_app_store_search.py
    ├── baidu_search.py
    ├── bing_search.py
    ├── constant.py
    ├── duck_duck_go_search.py
    ├── ebay_search.py
    ├── google_scholar_search.py
    ├── google_search.py
    ├── home_depot_search.py
    ├── naver_search.py
    ├── pagination.py
    ├── serp_api_client.py
    ├── serp_api_client_exception.py
    ├── walmart_search.py
    ├── yahoo_search.py
    ├── yandex_search.py
    └── youtube_search.py
├── setup.py
├── tests
    ├── __init__.py
    ├── test_account_api.py
    ├── test_apple_app_store_search.py
    ├── test_baidu_search.py
    ├── test_bing_search.py
    ├── test_duck_duck_go_search.py
    ├── test_ebay_search.py
    ├── test_example.py
    ├── test_example_paginate.py
    ├── test_google_scholar_search_api.py
    ├── test_google_search.py
    ├── test_home_depot_search.py
    ├── test_location_api.py
    ├── test_naver_search.py
    ├── test_search_archive_api.py
    ├── test_serp_api_client.py
    ├── test_walmart_search.py
    ├── test_yahoo_search.py
    ├── test_yandex_search.py
    └── test_youtube_search.py
└── testwrapper.py


/.flake8:
--------------------------------------------------------------------------------
1 | [flake8]
2 | exclude =
3 |     build
4 |     dist
5 |     .git
6 |     .env
7 |     .pytest_cache
8 | 


--------------------------------------------------------------------------------
/.github/workflows/python-package.yml:
--------------------------------------------------------------------------------
 1 | # This workflow will install Python dependencies, run tests and lint with a variety of Python versions
 2 | # For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions
 3 | 
 4 | name: Python package
 5 | 
 6 | on:
 7 |   push:
 8 |     branches: [ master ]
 9 |   pull_request:
10 |     branches: [ master ]
11 | 
12 | jobs:
13 |   build:
14 |     runs-on: ubuntu-latest
15 |     strategy:
16 |       matrix:
17 |         python-version: [3.7, 3.8, 3.9, '3.10']
18 | 
19 |     steps:
20 |     - uses: actions/checkout@v3
21 |     - name: Set up Python ${{ matrix.python-version }}
22 |       uses: actions/setup-python@v4
23 |       with:
24 |         python-version: ${{ matrix.python-version }}
25 |         cache: pip
26 | 
27 |     - name: Install dependencies
28 |       run: make install build_dep
29 | 
30 |     - name: Lint with flake8
31 |       run: make lint
32 | 
33 |     - name: Test with pytest
34 |       run: make test
35 |       env:
36 |         API_KEY: ${{secrets.API_KEY}}
37 | 


--------------------------------------------------------------------------------
/.gitignore:
--------------------------------------------------------------------------------
 1 | # ignore files
 2 | build/
 3 | .pytest_cache/
 4 | 
 5 | # Compiled python modules.
 6 | *.pyc
 7 | 
 8 | # Setuptools distribution folder.
 9 | /dist/
10 | 
11 | # Python egg metadata, regenerated from source files by setuptools.
12 | /*.egg-info/*
13 | google_search_results.egg-info/PKG-INFO
14 | google_search_results.egg-info/SOURCES.txt
15 | 
16 | # Python virtual environment
17 | .env
18 | 


--------------------------------------------------------------------------------
/LICENSE:
--------------------------------------------------------------------------------
 1 | MIT License
 2 | 
 3 | Copyright (c) 2018-2021 SerpApi
 4 | 
 5 | Permission is hereby granted, free of charge, to any person obtaining a copy
 6 | of this software and associated documentation files (the "Software"), to deal
 7 | in the Software without restriction, including without limitation the rights
 8 | to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 9 | copies of the Software, and to permit persons to whom the Software is
10 | furnished to do so, subject to the following conditions:
11 | 
12 | The above copyright notice and this permission notice shall be included in all
13 | copies or substantial portions of the Software.
14 | 
15 | THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
16 | IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
17 | FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
18 | AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
19 | LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
20 | OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
21 | SOFTWARE.
22 | 


--------------------------------------------------------------------------------
/MANIFEST.in:
--------------------------------------------------------------------------------
1 | include README.md
2 | 


--------------------------------------------------------------------------------
/Makefile:
--------------------------------------------------------------------------------
 1 | # Automate pip package development
 2 | #
 3 | # current version
 4 | version=$(shell grep version setup.py | cut -d"'" -f2)
 5 | 
 6 | .PHONY: build
 7 | 
 8 | all: clean install lint test
 9 | 
10 | clean:
11 | 	find . -name '*.pyc' -delete
12 | 	find . -type d -name "__pycache__" -delete
13 | 	pip3 uninstall google_search_results
14 | 
15 | create_env:
16 | 	python -m venv .env
17 | 	source .env/bin/activate
18 | 
19 | install:
20 | 	python3 -m pip install --upgrade pip
21 | 	if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi
22 | 
23 | lint: build_dep
24 | 	# stop the build if there are Python syntax errors or undefined names
25 | 	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
26 | 	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
27 | 	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
28 | 
29 | # Test with Python 3
30 | test: build_dep
31 | 	pytest --workers auto --tests-per-worker auto
32 | 
33 | # run example only 
34 | #  and display output (-s)
35 | example:
36 | 	pytest -s "tests/test_example.py::TestExample::test_async"
37 | 
38 | build_dep:
39 | 	pip3 install -U setuptools pytest py pytest-parallel flake8 twine
40 | 
41 | # https://packaging.python.org/tutorials/packaging-projects/
42 | build: build_dep
43 | 	python3 setup.py sdist
44 | 
45 | oobt: build
46 | 	pip3 install ./dist/google_search_results-$(version).tar.gz
47 | 	python3 oobt/oobt.py
48 | 
49 | check: oobt
50 | 	twine check dist/google_search_results-$(version).tar.gz
51 | 
52 | release: # check
53 | 	twine upload dist/google_search_results-$(version).tar.gz
54 | 


--------------------------------------------------------------------------------
/README.md:
--------------------------------------------------------------------------------
  1 | # Google Search Results in Python
  2 | 
  3 | [![Package](https://badge.fury.io/py/google-search-results.svg)](https://badge.fury.io/py/google-search-results)
  4 | [![Build](https://github.com/serpapi/google-search-results-python/actions/workflows/python-package.yml/badge.svg)](https://github.com/serpapi/google-search-results-python/actions/workflows/python-package.yml)
  5 | 
  6 | This Python package is meant to scrape and parse search results from Google, Bing, Baidu, Yandex, Yahoo, Home Depot, eBay and more, using [SerpApi](https://serpapi.com). 
  7 | 
  8 | The following services are provided:
  9 | - [Search API](https://serpapi.com/search-api)
 10 | - [Search Archive API](https://serpapi.com/search-archive-api)
 11 | - [Account API](https://serpapi.com/account-api)
 12 | - [Location API](https://serpapi.com/locations-api) (Google Only)
 13 | 
 14 | SerpApi provides a [script builder](https://serpapi.com/demo) to get you started quickly.
 15 | 
 16 | ## Installation
 17 | 
 18 | Python 3.7+
 19 | ```bash
 20 | pip install google-search-results
 21 | ```
 22 | 
 23 | [Link to the python package page](https://pypi.org/project/google-search-results/)
 24 | 
 25 | ## Quick start
 26 | 
 27 | ```python
 28 | from serpapi import GoogleSearch
 29 | search = GoogleSearch({
 30 |     "q": "coffee", 
 31 |     "location": "Austin,Texas",
 32 |     "api_key": "<your secret api key>"
 33 |   })
 34 | result = search.get_dict()
 35 | ```
 36 | 
 37 | This example runs a search for "coffee" using your secret API key.
 38 | 
 39 | The SerpApi service (backend)
 40 | - Searches Google using the search: q = "coffee"
 41 | - Parses the messy HTML responses
 42 | - Returns a standardized JSON response
 43 | The GoogleSearch class
 44 | - Formats the request
 45 | - Executes a GET http request against SerpApi service
 46 | - Parses the JSON response into a dictionary
 47 | 
 48 | Et voilà...
 49 | 
 50 | Alternatively, you can search:
 51 | - Bing using BingSearch class
 52 | - Baidu using BaiduSearch class
 53 | - Yahoo using YahooSearch class
 54 | - DuckDuckGo using DuckDuckGoSearch class
 55 | - eBay using EbaySearch class
 56 | - Yandex using YandexSearch class
 57 | - HomeDepot using HomeDepotSearch class
 58 | - GoogleScholar using GoogleScholarSearch class
 59 | - Youtube using YoutubeSearch class
 60 | - Walmart using WalmartSearch
 61 | - Apple App Store using AppleAppStoreSearch class
 62 | - Naver using NaverSearch class
 63 | 
 64 | 
 65 | See the [playground to generate your code.](https://serpapi.com/playground)
 66 | 
 67 | ## Summary
 68 | - [Google Search Results in Python](#google-search-results-in-python)
 69 |   - [Installation](#installation)
 70 |   - [Quick start](#quick-start)
 71 |   - [Summary](#summary)
 72 |     - [Google Search API capability](#google-search-api-capability)
 73 |     - [How to set SerpApi key](#how-to-set-serp-api-key)
 74 |     - [Example by specification](#example-by-specification)
 75 |     - [Location API](#location-api)
 76 |     - [Search Archive API](#search-archive-api)
 77 |     - [Account API](#account-api)
 78 |     - [Search Bing](#search-bing)
 79 |     - [Search Baidu](#search-baidu)
 80 |     - [Search Yandex](#search-yandex)
 81 |     - [Search Yahoo](#search-yahoo)
 82 |     - [Search Ebay](#search-ebay)
 83 |     - [Search Home depot](#search-home-depot)
 84 |     - [Search Youtube](#search-youtube)
 85 |     - [Search Google Scholar](#search-google-scholar)
 86 |     - [Generic search with SerpApiClient](#generic-search-with-serpapiclient)
 87 |     - [Search Google Images](#search-google-images)
 88 |     - [Search Google News](#search-google-news)
 89 |     - [Search Google Shopping](#search-google-shopping)
 90 |     - [Google Search By Location](#google-search-by-location)
 91 |     - [Batch Asynchronous Searches](#batch-asynchronous-searches)
 92 |     - [Python object as a result](#python-object-as-a-result)
 93 |     - [Python paginate using iterator](#pagination-using-iterator)
 94 |     - [Error management](#error-management)
 95 |   - [Change log](#change-log)
 96 |   - [Conclusion](#conclusion)
 97 | 
 98 | ### Google Search API capability
 99 | Source code.
100 | ```python
101 | params = {
102 |   "q": "coffee",
103 |   "location": "Location Requested", 
104 |   "device": "desktop|mobile|tablet",
105 |   "hl": "Google UI Language",
106 |   "gl": "Google Country",
107 |   "safe": "Safe Search Flag",
108 |   "num": "Number of Results",
109 |   "start": "Pagination Offset",
110 |   "api_key": "Your SerpApi Key", 
111 |   # To be match
112 |   "tbm": "nws|isch|shop", 
113 |   # To be search
114 |   "tbs": "custom to be search criteria",
115 |   # allow async request
116 |   "async": "true|false",
117 |   # output format
118 |   "output": "json|html"
119 | }
120 | 
121 | # define the search search
122 | search = GoogleSearch(params)
123 | # override an existing parameter
124 | search.params_dict["location"] = "Portland"
125 | # search format return as raw html
126 | html_results = search.get_html()
127 | # parse results
128 | #  as python Dictionary
129 | dict_results = search.get_dict()
130 | #  as JSON using json package
131 | json_results = search.get_json()
132 | #  as dynamic Python object
133 | object_result = search.get_object()
134 | ```
135 | [Link to the full documentation](https://serpapi.com/search-api)
136 | 
137 | See below for more hands-on examples.
138 | 
139 | ### How to set SerpApi key
140 | 
141 | You can get an API key here if you don't already have one: https://serpapi.com/users/sign_up
142 | 
143 | The SerpApi `api_key` can be set globally:
144 | ```python
145 | GoogleSearch.SERP_API_KEY = "Your Private Key"
146 | ```
147 | The SerpApi `api_key` can be provided for each search:
148 | ```python
149 | query = GoogleSearch({"q": "coffee", "serp_api_key": "Your Private Key"})
150 | ```
151 | 
152 | ### Example by specification
153 | 
154 | We love true open source, continuous integration and Test Driven Development (TDD). 
155 |  We are using RSpec to test [our infrastructure around the clock](https://travis-ci.org/serpapi/google-search-results-python) to achieve the best Quality of Service (QoS).
156 |  
157 | The directory test/ includes specification/examples.
158 | 
159 | Set your API key.
160 | ```bash
161 | export API_KEY="your secret key"
162 | ```
163 | 
164 | Run test
165 | ```python
166 | make test
167 | ```
168 | 
169 | ### Location API
170 | 
171 | ```python
172 | from serpapi import GoogleSearch
173 | search = GoogleSearch({})
174 | location_list = search.get_location("Austin", 3)
175 | print(location_list)
176 | ```
177 | 
178 | This prints the first 3 locations matching Austin (Texas, Texas, Rochester).
179 | ```python
180 | [   {   'canonical_name': 'Austin,TX,Texas,United States',
181 |         'country_code': 'US',
182 |         'google_id': 200635,
183 |         'google_parent_id': 21176,
184 |         'gps': [-97.7430608, 30.267153],
185 |         'id': '585069bdee19ad271e9bc072',
186 |         'keys': ['austin', 'tx', 'texas', 'united', 'states'],
187 |         'name': 'Austin, TX',
188 |         'reach': 5560000,
189 |         'target_type': 'DMA Region'},
190 |         ...]
191 | ```
192 | 
193 | ### Search Archive API
194 | 
195 | The search results are stored in a temporary cache.
196 | The previous search can be retrieved from the cache for free.
197 | 
198 | ```python
199 | from serpapi import GoogleSearch
200 | search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
201 | search_result = search.get_dictionary()
202 | assert search_result.get("error") == None
203 | search_id = search_result.get("search_metadata").get("id")
204 | print(search_id)
205 | ```
206 | 
207 | Now let's retrieve the previous search from the archive.
208 | 
209 | ```python
210 | archived_search_result = GoogleSearch({}).get_search_archive(search_id, 'json')
211 | print(archived_search_result.get("search_metadata").get("id"))
212 | ```
213 | This prints the search result from the archive.
214 | 
215 | ### Account API
216 | ```python
217 | from serpapi import GoogleSearch
218 | search = GoogleSearch({})
219 | account = search.get_account()
220 | ```
221 | This prints your account information.
222 | 
223 | ### Search Bing
224 | ```python
225 | from serpapi import BingSearch
226 | search = BingSearch({"q": "Coffee", "location": "Austin,Texas"})
227 | data = search.get_dict()
228 | ```
229 | This code prints Bing search results for coffee as a Dictionary. 
230 | 
231 | https://serpapi.com/bing-search-api
232 | 
233 | ### Search Baidu
234 | ```python
235 | from serpapi import BaiduSearch
236 | search = BaiduSearch({"q": "Coffee"})
237 | data = search.get_dict()
238 | ```
239 | This code prints Baidu search results for coffee as a Dictionary. 
240 | https://serpapi.com/baidu-search-api
241 | 
242 | ### Search Yandex
243 | ```python
244 | from serpapi import YandexSearch
245 | search = YandexSearch({"text": "Coffee"})
246 | data = search.get_dict()
247 | ```
248 | This code prints Yandex search results for coffee as a Dictionary. 
249 | 
250 | https://serpapi.com/yandex-search-api
251 | 
252 | ### Search Yahoo
253 | ```python
254 | from serpapi import YahooSearch
255 | search = YahooSearch({"p": "Coffee"})
256 | data = search.get_dict()
257 | ```
258 | This code prints Yahoo search results for coffee as a Dictionary. 
259 | 
260 | https://serpapi.com/yahoo-search-api
261 | 
262 | 
263 | ### Search eBay
264 | ```python
265 | from serpapi import EbaySearch
266 | search = EbaySearch({"_nkw": "Coffee"})
267 | data = search.get_dict()
268 | ```
269 | This code prints eBay search results for coffee as a Dictionary. 
270 | 
271 | https://serpapi.com/ebay-search-api
272 | 
273 | ### Search Home Depot
274 | ```python
275 | from serpapi import HomeDepotSearch
276 | search = HomeDepotSearch({"q": "chair"})
277 | data = search.get_dict()
278 | ```
279 | This code prints Home Depot search results for chair as Dictionary. 
280 | 
281 | https://serpapi.com/home-depot-search-api
282 | 
283 | ### Search Youtube
284 | ```python
285 | from serpapi import YoutubeSearch
286 | search = YoutubeSearch({"q": "chair"})
287 | data = search.get_dict()
288 | ```
289 | This code prints Youtube search results for chair as Dictionary. 
290 | 
291 | https://serpapi.com/youtube-search-api
292 | 
293 | ### Search Google Scholar
294 | ```python
295 | from serpapi import GoogleScholarSearch
296 | search = GoogleScholarSearch({"q": "Coffee"})
297 | data = search.get_dict()
298 | ```
299 | This code prints Google Scholar search results.
300 | 
301 | ### Search Walmart
302 | ```python
303 | from serpapi import WalmartSearch
304 | search = WalmartSearch({"query": "chair"})
305 | data = search.get_dict()
306 | ```
307 | This code prints Walmart search results.
308 | 
309 | ### Search Youtube
310 | ```python
311 | from serpapi import YoutubeSearch
312 | search = YoutubeSearch({"search_query": "chair"})
313 | data = search.get_dict()
314 | ```
315 | This code prints Youtube search results.
316 | 
317 | ### Search Apple App Store
318 | ```python
319 | from serpapi import AppleAppStoreSearch
320 | search = AppleAppStoreSearch({"term": "Coffee"})
321 | data = search.get_dict()
322 | ```
323 | This code prints Apple App Store search results.
324 | 
325 | ### Search Naver
326 | ```python
327 | from serpapi import NaverSearch
328 | search = NaverSearch({"query": "chair"})
329 | data = search.get_dict()
330 | ```
331 | This code prints Naver search results.
332 | 
333 | ### Generic search with SerpApiClient
334 | ```python
335 | from serpapi import SerpApiClient
336 | query = {"q": "Coffee", "location": "Austin,Texas", "engine": "google"}
337 | search = SerpApiClient(query)
338 | data = search.get_dict()
339 | ```
340 | This class enables interaction with any search engine supported by SerpApi.com 
341 | 
342 | ### Search Google Images
343 | 
344 | ```python
345 | from serpapi import GoogleSearch
346 | search = GoogleSearch({"q": "coffe", "tbm": "isch"})
347 | for image_result in search.get_dict()['images_results']:
348 |     link = image_result["original"]
349 |     try:
350 |         print("link: " + link)
351 |         # wget.download(link, '.')
352 |     except:
353 |         pass
354 | ```
355 | 
356 | This code prints all the image links, 
357 |  and downloads the images if you un-comment the line with wget (Linux/OS X tool to download files).
358 | 
359 | This tutorial covers more ground on this topic.
360 | https://github.com/serpapi/showcase-serpapi-tensorflow-keras-image-training
361 | 
362 | ### Search Google News
363 | 
364 | ```python
365 | from serpapi import GoogleSearch
366 | search = GoogleSearch({
367 |     "q": "coffe",   # search search
368 |     "tbm": "nws",  # news
369 |     "tbs": "qdr:d", # last 24h
370 |     "num": 10
371 | })
372 | for offset in [0,1,2]:
373 |     search.params_dict["start"] = offset * 10
374 |     data = search.get_dict()
375 |     for news_result in data['news_results']:
376 |         print(str(news_result['position'] + offset * 10) + " - " + news_result['title'])
377 | ```
378 | 
379 | This script prints the first 3 pages of the news headlines for the last 24 hours.
380 | 
381 | ### Search Google Shopping
382 | 
383 | ```python
384 | from serpapi import GoogleSearch
385 | search = GoogleSearch({
386 |     "q": "coffe",   # search search
387 |     "tbm": "shop",  # shopping
388 |     "tbs": "p_ord:rv", # ordered by review
389 |     "num": 100
390 | })
391 | data = search.get_dict()
392 | for shopping_result in data['shopping_results']:
393 |     print(shopping_result['position']) + " - " + shopping_result['title'])
394 | 
395 | ```
396 | 
397 | This script prints all the shopping results, ordered by review order.
398 | 
399 | ### Google Search By Location
400 | 
401 | With SerpApi, we can build a Google search from anywhere in the world.
402 | This code looks for the best coffee shop for the given cities.
403 | 
404 | ```python
405 | from serpapi import GoogleSearch
406 | for city in ["new york", "paris", "berlin"]:
407 |   location = GoogleSearch({}).get_location(city, 1)[0]["canonical_name"]
408 |   search = GoogleSearch({
409 |       "q": "best coffee shop",   # search search
410 |       "location": location,
411 |       "num": 1,
412 |       "start": 0
413 |   })
414 |   data = search.get_dict()
415 |   top_result = data["organic_results"][0]["title"]
416 | ```
417 | 
418 | ### Batch Asynchronous Searches
419 | 
420 | We offer two ways to boost your searches thanks to the`async` parameter.
421 |  - Blocking - async=false - more compute intensive because the search needs to maintain many connections. (default) 
422 | - Non-blocking - async=true - the way to go for large batches of queries  (recommended)
423 | 
424 | ```python
425 | # Operating system
426 | import os
427 | 
428 | # regular expression library
429 | import re
430 | 
431 | # safe queue (named Queue in python2)
432 | from queue import Queue
433 | 
434 | # Time utility
435 | import time
436 | 
437 | # SerpApi search
438 | from serpapi import GoogleSearch
439 | 
440 | # store searches
441 | search_queue = Queue()
442 | 
443 | # SerpApi search
444 | search = GoogleSearch({
445 |     "location": "Austin,Texas",
446 |     "async": True,
447 |     "api_key": os.getenv("API_KEY")
448 | })
449 | 
450 | # loop through a list of companies
451 | for company in ['amd', 'nvidia', 'intel']:
452 |     print("execute async search: q = " + company)
453 |     search.params_dict["q"] = company
454 |     result = search.get_dict()
455 |     if "error" in result:
456 |         print("oops error: ", result["error"])
457 |         continue
458 |     print("add search to the queue where id: ", result['search_metadata'])
459 |     # add search to the search_queue
460 |     search_queue.put(result)
461 | 
462 | print("wait until all search statuses are cached or success")
463 | 
464 | # Create regular search
465 | while not search_queue.empty():
466 |     result = search_queue.get()
467 |     search_id = result['search_metadata']['id']
468 | 
469 |     # retrieve search from the archive - blocker
470 |     print(search_id + ": get search from archive")
471 |     search_archived = search.get_search_archive(search_id)
472 |     print(search_id + ": status = " +
473 |           search_archived['search_metadata']['status'])
474 | 
475 |     # check status
476 |     if re.search('Cached|Success',
477 |                  search_archived['search_metadata']['status']):
478 |         print(search_id + ": search done with q = " +
479 |               search_archived['search_parameters']['q'])
480 |     else:
481 |         # requeue search_queue
482 |         print(search_id + ": requeue search")
483 |         search_queue.put(result)
484 | 
485 |         # wait 1s
486 |         time.sleep(1)
487 | 
488 | print('all searches completed')
489 | ```
490 | 
491 | This code shows how to run searches asynchronously.
492 | The search parameters must have {async: True}. This indicates that the client shouldn't wait for the search to be completed.
493 | The current thread that executes the search is now non-blocking, which allows it to execute thousands of searches in seconds. The SerpApi backend will do the processing work.
494 | The actual search result is deferred to a later call from the search archive using get_search_archive(search_id).
495 | In this example the non-blocking searches are persisted in a queue: search_queue.
496 | A loop through the search_queue allows it to fetch individual search results.
497 | This process can easily be multithreaded to allow a large number of concurrent search requests.
498 | To keep things simple, this example only explores search results one at a time (single threaded).
499 | 
500 | [See example.](https://github.com/serpapi/google-search-results-python/blob/master/tests/test_example.py)
501 | 
502 | ### Python object as a result
503 | 
504 | The search results can be automatically wrapped in dynamically generated Python object.
505 | This solution offers a more dynamic, fully Oriented Object Programming approach over the regular Dictionary / JSON data structure.
506 | 
507 | ```python
508 | from serpapi import GoogleSearch
509 | search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
510 | r = search.get_object()
511 | assert type(r.organic_results) == list
512 | assert r.organic_results[0].title
513 | assert r.search_metadata.id
514 | assert r.search_metadata.google_url
515 | assert r.search_parameters.q, "Coffee"
516 | assert r.search_parameters.engine, "google"
517 | ```
518 | 
519 | ### Pagination using iterator
520 | Let's collect links across multiple search results pages.
521 | ```python
522 | # to get 2 pages
523 | start = 0
524 | end = 40
525 | page_size = 10
526 | 
527 | # basic search parameters
528 | parameter = {
529 |   "q": "coca cola",
530 |   "tbm": "nws",
531 |   "api_key": os.getenv("API_KEY"),
532 |   # optional pagination parameter
533 |   #  the pagination method can take argument directly
534 |   "start": start,
535 |   "end": end,
536 |   "num": page_size
537 | }
538 | 
539 | # as proof of concept 
540 | # urls collects
541 | urls = []
542 | 
543 | # initialize a search
544 | search = GoogleSearch(parameter)
545 | 
546 | # create a python generator using parameter
547 | pages = search.pagination()
548 | # or set custom parameter
549 | pages = search.pagination(start, end, page_size)
550 | 
551 | # fetch one search result per iteration 
552 | # using a basic python for loop 
553 | # which invokes python iterator under the hood.
554 | for page in pages:
555 |   print(f"Current page: {page['serpapi_pagination']['current']}")
556 |   for news_result in page["news_results"]:
557 |     print(f"Title: {news_result['title']}\nLink: {news_result['link']}\n")
558 |     urls.append(news_result['link'])
559 |   
560 | # check if the total number pages is as expected
561 | # note: the exact number if variable depending on the search engine backend
562 | if len(urls) == (end - start):
563 |   print("all search results count match!")
564 | if len(urls) == len(set(urls)):
565 |   print("all search results are unique!")
566 | ```
567 | 
568 | Examples to fetch links with pagination: [test file](https://github.com/serpapi/google-search-results-python/blob/master/tests/test_example_paginate.py), [online IDE](https://replit.com/@DimitryZub1/Scrape-Google-News-with-Pagination-python-serpapi)
569 | 
570 | ### Error management
571 | 
572 | SerpApi keeps error management simple.
573 |  - backend service error or search fail
574 |  - client error
575 | 
576 | If it's a backend error, a simple error message is returned as string in the server response.
577 | ```python
578 | from serpapi import GoogleSearch
579 | search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas", "api_key": "<secret_key>"})
580 | data = search.get_json()
581 | assert data["error"] == None
582 | ```
583 | In some cases, there are more details available in the data object.
584 | 
585 | If it's a client error, then a SerpApiClientException is raised.
586 | 
587 | ## Change log
588 | 2023-03-10 @ 2.4.2
589 |  - Change long description to README.md
590 | 
591 | 2021-12-22 @ 2.4.1
592 |  - add more search engine 
593 |    - youtube
594 |    - walmart
595 |    - apple_app_store
596 |    - naver
597 |  - raise SerpApiClientException instead of raw string in order to follow Python guideline 3.5+
598 |  - add more unit error tests for serp_api_client
599 | 
600 | 2021-07-26 @ 2.4.0
601 |  - add page size support using num parameter
602 |  - add youtube search engine
603 | 
604 | 2021-06-05 @ 2.3.0
605 |  - add pagination support
606 | 
607 | 2021-04-28 @ 2.2.0
608 |  - add get_response method to provide raw requests.Response object
609 | 
610 | 2021-04-04 @ 2.1.0
611 |  - Add home depot search engine
612 |  - get_object() returns dynamic Python object
613 |  
614 | 2020-10-26 @ 2.0.0
615 |  - Reduce class name to <engine>Search
616 |  - Add get_raw_json
617 | 
618 | 2020-06-30 @ 1.8.3
619 |  - simplify import
620 |  - improve package for python 3.5+
621 |  - add support for python 3.5 and 3.6
622 | 
623 | 2020-03-25 @ 1.8
624 |  - add support for Yandex, Yahoo, Ebay
625 |  - clean-up test
626 | 
627 | 2019-11-10 @ 1.7.1
628 |  - increase engine parameter priority over engine value set in the class
629 | 
630 | 2019-09-12 @ 1.7
631 |  - Change  namespace "from lib." instead: "from serpapi import GoogleSearch"
632 |  - Support for Bing and Baidu
633 | 
634 | 2019-06-25 @ 1.6
635 |  - New search engine supported: Baidu and Bing
636 | 
637 | ## Conclusion
638 | SerpApi supports all the major search engines. Google has the more advance support with all the major services available: Images, News, Shopping and more..
639 | To enable a type of search, the field tbm (to be matched) must be set to:
640 | 
641 |  * isch: Google Images API.
642 |  * nws: Google News API.
643 |  * shop: Google Shopping API.
644 |  * any other Google service should work out of the box.
645 |  * (no tbm parameter): regular Google search.
646 | 
647 | The field `tbs` allows to customize the search even more.
648 | 
649 | [The full documentation is available here.](https://serpapi.com/search-api)
650 | 


--------------------------------------------------------------------------------
/README.rst:
--------------------------------------------------------------------------------
 1 | ===============================================
 2 | Google / Bing / Baidu Search Results in Python
 3 | ===============================================
 4 | 
 5 | This Python package is meant to scrape and parse Google, Google Scholar, Bing, Baidu, Yandex, Yahoo, Ebay results using `SerpApi <https://serpapi.com>`_. 
 6 | The following services are provided:
 7 | 
 8 | * `Search API <https://serpapi.com/search-api>`_ 
 9 | * `Search Archive API <https://serpapi.com/search-archive-api>`_
10 | * `Account API <https://serpapi.com/account-api>`_ 
11 | * `Location API <https://serpapi.com/locations-api>`_
12 | 
13 | SerpApi provides a `script builder <https://serpapi.com/demo/>`_ to get you started quickly.
14 | 
15 | 
16 | Installation
17 | -------------
18 | 
19 | Compatible with Python 3.7+
20 | 
21 | .. code-block:: shell
22 | 
23 |     pip install google-search-results
24 | 
25 | `Link to the python package page <https://pypi.org/project/google-search-results>`_
26 | 
27 | Quick start
28 | -------------
29 | 
30 | .. code-block:: python
31 | 
32 |     from serpapi import GoogleSearch
33 |     search = GoogleSearch({"q": "coffee", "location": "Austin,Texas", "api_key": "secretKey"})
34 |     result = search.get_dict()
35 | 
36 | This example runs a search about "coffee" using your secret api key.
37 | 
38 | The SerpApi service (backend)
39 | 
40 | * searches on Google using the query: q = "coffee"
41 | * parses the messy HTML responses
42 | * return a standardizes JSON response
43 | 
44 | The GoogleSearch class
45 | 
46 | * Format the request
47 | * Execute GET http request against SerpApi service
48 | * Parse JSON response into a dictionary
49 | 
50 | Et voila..
51 | 
52 | Alternatively, you can search:
53 | 
54 | - Bing using BingSearch class
55 | - Baidu using BaiduSearch class
56 | - Yahoo using YahooSearch class
57 | - duckduckgo using DuckDuckGoSearch class
58 | - Ebay using EbaySearch class
59 | - Yandex using YandexSearch class
60 | - HomeDepot using HomeDepotSearch class
61 | - GoogleScholar using GoogleScholarSearch class
62 | - Youtube using YoutubeSearch class
63 | - Walmart using WalmartSearch
64 | - Apple App Store using AppleAppStoreSearch class
65 | - Naver using NaverSearch class
66 | 
67 | See the `playground to generate your code. <https://serpapi.com/playground>`_
68 | 
69 | `Documentation available here <https://github.com/serpapi/google-search-results-python/blob/master/README.md>`_
70 | 


--------------------------------------------------------------------------------
/oobt/oobt.py:
--------------------------------------------------------------------------------
 1 | import sys
 2 | import os
 3 | from serpapi import GoogleSearch
 4 | 
 5 | # Run Out Of Box testing
 6 | #  Load package
 7 | #  Run simple query
 8 | #
 9 | import pprint
10 | print("initialize serpapi search")
11 | search = GoogleSearch({
12 |         "q": "coffee",
13 |         "location": "Austin,Texas", 
14 |         "api_key": os.getenv("API_KEY","demo")
15 | })
16 | print("execute search")
17 | result = search.get_dict()
18 | print("display result")
19 | pp = pprint.PrettyPrinter(indent=2)
20 | pp.pprint(result)
21 | print("------")
22 | if len(result) > 0:
23 |         print("OK: Out of box tests passed")
24 |         sys.exit(0)
25 | 
26 | print("FAIL: Out of box tests failed: no result")
27 | sys.exit(1)
28 | 


--------------------------------------------------------------------------------
/requirements.txt:
--------------------------------------------------------------------------------
1 | -i https://pypi.org/simple
2 | certifi==2022.5.18
3 | chardet==4.0.0
4 | -e .
5 | idna==2.10
6 | requests==2.25.1
7 | urllib3==1.26.9
8 | 


--------------------------------------------------------------------------------
/serpapi/__init__.py:
--------------------------------------------------------------------------------
 1 | from .serp_api_client import SerpApiClient
 2 | from .baidu_search import BaiduSearch
 3 | from .google_search import GoogleSearch
 4 | from .yahoo_search import YahooSearch
 5 | from .bing_search import BingSearch
 6 | from .yandex_search import YandexSearch
 7 | from .google_scholar_search import GoogleScholarSearch
 8 | from .ebay_search import EbaySearch
 9 | from .home_depot_search import HomeDepotSearch
10 | from .youtube_search import YoutubeSearch
11 | from .duck_duck_go_search import DuckDuckGoSearch
12 | from .walmart_search import WalmartSearch
13 | from .naver_search import NaverSearch
14 | from .apple_app_store_search import AppleAppStoreSearch
15 | 
16 | 


--------------------------------------------------------------------------------
/serpapi/apple_app_store_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | from serpapi.constant import *
 4 | 
 5 | class AppleAppStoreSearch(SerpApiClient):
 6 |     """AppleAppStoreSearch enables to search google scholar and parse the result.
 7 |     ```python
 8 |     from serpapi import AppleAppStoreSearch
 9 |     search = AppleAppStoreSearch({"term": "ipad"})
10 |     data = search.get_dct()
11 |     ```
12 |     
13 |     doc: https://serpapi.com/apple-app-store
14 |     """
15 | 
16 |     def __init__(self, params_dict):
17 |         super(AppleAppStoreSearch, self).__init__(params_dict, APPLE_APP_STORE_ENGINE)
18 | 
19 |     def get_location(self, q, limit = 5):
20 |         raise SerpApiClientException("location is not supported by youtube search engine")
21 | 


--------------------------------------------------------------------------------
/serpapi/baidu_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | 
 4 | class BaiduSearch(SerpApiClient):
 5 |     """BaiduSearch enables to search baidu and parse the result.
 6 |     ```python
 7 |     from serpapi import BaiduSearch
 8 |     query = BaiduSearch({"q": "coffee"})
 9 |     data = query.get_json()
10 |     ```
11 | 
12 |     doc: https://serpapi.com/baidu-search-api
13 |     """
14 | 
15 |     def __init__(self, params_dict):
16 |         super(BaiduSearch, self).__init__(params_dict, BAIDU_ENGINE)
17 | 
18 |     def get_location(self, q, limit = 5):
19 |         raise SerpApiClientException("location is not supported by Baidu search engine at this time")
20 | 


--------------------------------------------------------------------------------
/serpapi/bing_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | 
 3 | class BingSearch(SerpApiClient):
 4 |     """BingSearch enables to search bing and parse the result.
 5 |     ```python
 6 |     from serpapi import BingSearch
 7 |     query = BingSearch({"q": "coffee", "location": "Austin,Texas"})
 8 |     data = query.get_json()
 9 |     ```
10 | 
11 |     doc: https://serpapi.com/bing-search-api
12 |     """
13 | 
14 |     def __init__(self, params_dict):
15 |         super(BingSearch, self).__init__(params_dict, BING_ENGINE)
16 | 


--------------------------------------------------------------------------------
/serpapi/constant.py:
--------------------------------------------------------------------------------
 1 | 
 2 | # Pagination constant
 3 | DEFAULT_START = 0
 4 | DEFAULT_END = 1000000000
 5 | DEFAULT_PAGE_SIZE = 10
 6 | DEFAULT_LIMIT = 1000
 7 | 
 8 | # Supported earch engine
 9 | GOOGLE_ENGINE = 'google'
10 | GOOGLE_SCHOLAR_ENGINE = 'google_scholar'
11 | BAIDU_ENGINE = 'baidu'
12 | BING_ENGINE = 'bing'
13 | YANDEX_ENGINE = 'yandex'
14 | EBAY_ENGINE = 'ebay'
15 | YAHOO_ENGINE = 'yahoo'
16 | HOME_DEPOT_ENGINE = 'home_depot'
17 | YOUTUBE_ENGINE = 'youtube'
18 | DUCKDUCKGO_ENGINE = 'duckduckgo'
19 | WALMART_ENGINE = "walmart"
20 | NAVER_ENGINE = "naver"
21 | APPLE_APP_STORE_ENGINE = "apple_app_store"
22 | 
23 | # from serpapi.constant import *
24 | 


--------------------------------------------------------------------------------
/serpapi/duck_duck_go_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | from serpapi.constant import *
 4 | 
 5 | class DuckDuckGoSearch(SerpApiClient):
 6 |     """DuckDuckGoSearch enables to search google scholar and parse the result.
 7 |     ```python
 8 |     from serpapi import DuckDuckGoSearch
 9 |     search = DuckDuckGoSearch({"query": "chair"})
10 |     data = search.get_json()
11 |     ```
12 | 
13 |     doc: https://serpapi.com/duckduckgo-search-api
14 |     """
15 | 
16 |     def __init__(self, params_dict):
17 |         super(DuckDuckGoSearch, self).__init__(params_dict, DUCKDUCKGO_ENGINE)
18 | 
19 |     def get_location(self, q, limit = 5):
20 |         raise SerpApiClientException("location is not supported by walmart search engine")
21 | 


--------------------------------------------------------------------------------
/serpapi/ebay_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | 
 4 | class EbaySearch(SerpApiClient):
 5 |     """EbaySearch enables to search ebay and parse the result.
 6 |     ```python
 7 |     from serpapi import EbaySearch
 8 |     query = EbaySearch({"_nkw": "coffee"})
 9 |     data = query.get_json()
10 |     ```
11 | 
12 |     doc: https://serpapi.com/ebay-search-api
13 |     """
14 | 
15 |     def __init__(self, params_dict):
16 |         super(EbaySearch, self).__init__(params_dict, EBAY_ENGINE)
17 | 
18 |     def get_location(self, q, limit = 5):
19 |         raise SerpApiClientException("location is not supported by Ebay search engine at this time")
20 | 


--------------------------------------------------------------------------------
/serpapi/google_scholar_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | 
 4 | class GoogleScholarSearch(SerpApiClient):
 5 |     """GoogleScholarSearch enables to search google scholar and parse the result.
 6 |     ```python
 7 |     from serpapi import GoogleScholarSearch
 8 |     query = GoogleScholarSearch({"q": "coffee"})
 9 |     data = query.get_json()
10 |     ```
11 | 
12 |     doc: https://serpapi.com/google-scholar-api
13 |     """
14 | 
15 |     def __init__(self, params_dict):
16 |         super(GoogleScholarSearch, self).__init__(params_dict, GOOGLE_SCHOLAR_ENGINE)
17 | 
18 |     def get_location(self, q, limit = 5):
19 |         raise SerpApiClientException("location is not supported by Google scholar search engine")
20 | 


--------------------------------------------------------------------------------
/serpapi/google_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | 
 3 | class GoogleSearch(SerpApiClient):
 4 |     """GoogleSearch enables to search google and parse the result.
 5 |     ```python
 6 |     from serpapi import GoogleSearch
 7 |     query = GoogleSearch({"q": "coffee", "location": "Austin,Texas"})
 8 |     data = query.get_json()
 9 |     ```
10 | 
11 |     https://github.com/serpapi/google-search-results-python
12 |     """
13 | 
14 |     def __init__(self, params_dict):
15 |         super(GoogleSearch, self).__init__(params_dict, GOOGLE_ENGINE)
16 | 


--------------------------------------------------------------------------------
/serpapi/home_depot_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | 
 4 | class HomeDepotSearch(SerpApiClient):
 5 |     """HomeDepotSearch enables to search home depot and parse the result.
 6 |     ```python
 7 |     from serpapi import HomeDepotSearch
 8 |     query = HomeDepotSearch({"q": "chair"})
 9 |     data = query.get_json()
10 |     ```
11 | 
12 |     doc: https://serpapi.com/home-depot-search-api
13 |     """
14 | 
15 |     def __init__(self, params_dict):
16 |         super(HomeDepotSearch, self).__init__(params_dict, HOME_DEPOT_ENGINE)
17 | 
18 |     def get_location(self, q, limit = 5):
19 |         raise SerpApiClientException("location is not supported by Home Depot search engine")
20 | 


--------------------------------------------------------------------------------
/serpapi/naver_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | from serpapi.constant import *
 4 | 
 5 | class NaverSearch(SerpApiClient):
 6 |     """NaverSearch enables to search google scholar and parse the result.
 7 |     ```python
 8 |     from serpapi import NaverSearch
 9 |     search = NaverSearch({"query": "chair"})
10 |     data = search.get_dict()
11 |     ```
12 | 
13 |     doc: https://serpapi.com/naver-search-api
14 |     """
15 | 
16 |     def __init__(self, params_dict):
17 |         super(NaverSearch, self).__init__(params_dict, NAVER_ENGINE)
18 | 
19 |     def get_location(self, q, limit = 5):
20 |         raise SerpApiClientException("location is not supported by youtube search engine")
21 | 


--------------------------------------------------------------------------------
/serpapi/pagination.py:
--------------------------------------------------------------------------------
 1 | from urllib import parse
 2 | from serpapi import constant
 3 | 
 4 | # Paginate response in SerpApi
 5 | class Pagination:
 6 | 
 7 |   def __init__(self, client, start = constant.DEFAULT_START, end = constant.DEFAULT_END, num = constant.DEFAULT_PAGE_SIZE, limit = constant.DEFAULT_LIMIT):
 8 |     # SerpApi client
 9 |     self.client = client
10 | 
11 |     self.limit = limit
12 | 
13 |     """Backwards-compatible workaround.
14 |     `start`, `num`, and `end` parameters to `Pagination#__init__` are deprecated.
15 | 
16 |     Set `start` and `num` search parameters.
17 |     It works for Google Search API only.
18 |     A correct way to set an offset, limit, and page size is in search parameters directly.
19 |     (A hash that is passed to `SerpApi#__init__`.)
20 |     """
21 |     if start != constant.DEFAULT_START:
22 |       self.client.params_dict['start'] = start
23 | 
24 |     if end != constant.DEFAULT_END:
25 |       self.client.params_dict['end'] = end
26 | 
27 |     if num != constant.DEFAULT_PAGE_SIZE:
28 |       self.client.params_dict['num'] = num
29 | 
30 | 
31 |     self.page_number = 0
32 | 
33 |   def __iter__(self):
34 |     return self
35 | 
36 |   def __next__(self):
37 |     if self.page_number >= self.limit:
38 |       raise StopIteration
39 | 
40 |     # execute request
41 |     result = self.client.get_dict()
42 | 
43 |     pagination = result.get('serpapi_pagination', result.get('pagination'))
44 | 
45 |     # stop if backend miss to return `serpapi_pagination` or `pagination`
46 |     if not pagination:
47 |       raise StopIteration
48 | 
49 |     # stop if no next page
50 |     if not 'next' in pagination:
51 |       raise StopIteration
52 | 
53 |     # Get actual parameters from next page of target website
54 |     params_from_target_website = dict(
55 |       parse.parse_qsl(parse.urlsplit(pagination['next']).query)
56 |     )
57 | 
58 |     # stop if parameters from the target website were not changed
59 |     if params_from_target_website.items() <= self.client.params_dict.items():
60 |       raise StopIteration
61 | 
62 |     self.client.params_dict.update(params_from_target_website)
63 | 
64 |     self.page_number += 1
65 | 
66 |     return result
67 | 


--------------------------------------------------------------------------------
/serpapi/serp_api_client.py:
--------------------------------------------------------------------------------
  1 | import requests
  2 | import json
  3 | from serpapi.constant import *
  4 | from serpapi.pagination import Pagination
  5 | from serpapi.serp_api_client_exception import SerpApiClientException
  6 | 
  7 | 
  8 | class SerpApiClient(object):
  9 |     """SerpApiClient enables to query any search engines supported by SerpApi and parse the results.
 10 |     ```python
 11 |     from serpapi import GoogleSearch
 12 |     search = SerpApiClient({
 13 |         "q": "Coffee", 
 14 |         "location": "Austin,Texas", 
 15 |         "engine": "google",
 16 |         "api_key": "<your private key>"
 17 |         })
 18 | 	data = search.get_json()
 19 |     ```
 20 | 
 21 |     https://serpapi.com/search-api
 22 |     """
 23 | 
 24 |     BACKEND = "https://serpapi.com"
 25 |     SERP_API_KEY = None
 26 | 
 27 |     def __init__(self, params_dict, engine = None, timeout = 60000):
 28 |         self.params_dict = params_dict
 29 |         self.engine = engine
 30 |         self.timeout = timeout
 31 | 
 32 |     def construct_url(self, path = "/search"):
 33 |         self.params_dict['source'] = 'python'
 34 |         if self.SERP_API_KEY:
 35 |             self.params_dict['serp_api_key'] = self.SERP_API_KEY
 36 |         if self.engine:
 37 |             if not 'engine' in self.params_dict:
 38 |                 self.params_dict['engine'] = self.engine
 39 |         if not 'engine' in self.params_dict:
 40 |             raise SerpApiClientException("engine must be defined in params_dict or engine")
 41 |         return self.BACKEND + path, self.params_dict
 42 | 
 43 |     def get_response(self, path = '/search'):
 44 |         """Returns:
 45 |             Response object provided by requests.get
 46 |         """
 47 |         url = None
 48 |         try:
 49 |             url, parameter = self.construct_url(path)
 50 |             # print(url)
 51 |             response = requests.get(url, parameter, timeout=self.timeout)
 52 |             return response
 53 |         except requests.HTTPError as e:
 54 |             print("fail: " + url)
 55 |             print(e, e.response.status_code)
 56 |             raise e
 57 | 
 58 |     def get_results(self, path='/search'):
 59 |         """Returns:
 60 |             Response text field
 61 |         """
 62 |         return self.get_response(path).text
 63 | 
 64 |     def get_html(self):
 65 |         """Returns:
 66 |             Raw HTML search result from Google
 67 |         """
 68 |         self.params_dict["output"] = "html"
 69 |         return self.get_results()
 70 | 
 71 |     def get_json(self):
 72 |         """Returns:
 73 |             Formatted JSON search results using json package
 74 |         """
 75 |         self.params_dict["output"] = "json"
 76 |         return json.loads(self.get_results())
 77 | 
 78 |     def get_raw_json(self):
 79 |         """Returns:
 80 |             Formatted JSON search result as string
 81 |         """
 82 |         self.params_dict["output"] = "json"
 83 |         return self.get_results()
 84 | 
 85 |     def get_dictionary(self):
 86 |         """Returns:
 87 |             Dict with the formatted response content
 88 |         """
 89 |         return dict(self.get_json())
 90 | 
 91 |     def get_dict(self):
 92 |         """Returns:
 93 |             Dict with the formatted response content
 94 |             (alias for get_dictionary)
 95 |         """
 96 |         return self.get_dictionary()
 97 | 
 98 |     def get_object(self):
 99 |         """Returns: 
100 |             Dynamically created python object wrapping the result data structure
101 |         """
102 |         # iterative over response hash
103 |         node = self.get_dictionary()
104 |         # create dynamic python object
105 |         return self.make_pyobj("response", node)
106 | 
107 |     def make_pyobj(self, name, node):
108 |         pytype = type(name, (object, ), {})
109 |         pyobj = pytype()
110 | 
111 |         if isinstance(node, list):
112 |             setattr(pyobj, name, [])
113 |             for el in node:
114 |                 getattr(pyobj, name).append(self.make_pyobj(name, el))
115 |             return pyobj
116 |         elif isinstance(node, dict):
117 |             for name, child in node.items():
118 |                 if isinstance(child, list):
119 |                     setattr(pyobj, name, [])
120 |                     for el in child:
121 |                         getattr(pyobj, name).append(self.make_pyobj(name, el))
122 |                 elif isinstance(child, dict):
123 |                     setattr(pyobj, name, self.make_pyobj(name, child))
124 |                 else:
125 |                     setattr(pyobj, name, child)
126 |         else:
127 |             setattr(pyobj, name, node)
128 | 
129 |         return pyobj
130 | 
131 |     def get_search_archive(self, search_id, format = 'json'):
132 |         """Retrieve search result from the Search Archive API
133 |         Parameters:
134 |             search_id (int): unique identifier for the search provided by metadata.id 
135 |             format (string): search format: json or html [optional]
136 |         Returns:
137 |             dict|string: search result from the archive
138 |         """
139 |         result = self.get_results("/searches/{0}.{1}".format(search_id, format))
140 |         if format == 'json':
141 |             result = json.loads(result)
142 |         return result
143 | 
144 |     def get_account(self):
145 |         """Get account information using Account API
146 |         Returns:
147 |             dict: account information
148 |         """
149 |         return json.loads(self.get_results("/account"))
150 | 
151 |     def get_location(self, q, limit = 5):
152 |         """Get location using Location API
153 |         Parameters:
154 |             q (string): location (like: city name..)
155 |             limit (int): number of matches returned
156 |         Returns:
157 |             dict: Location matching q
158 |         """
159 |         self.params_dict = {}
160 |         self.params_dict["output"] = "json"
161 |         self.params_dict["q"] = q
162 |         self.params_dict["limit"] = limit
163 |         buffer = self.get_results('/locations.json')
164 |         return json.loads(buffer)
165 | 
166 |     def pagination(self, start = DEFAULT_START, end = DEFAULT_END, page_size = DEFAULT_PAGE_SIZE, limit = DEFAULT_LIMIT):
167 |         """Return:
168 |             Generator to iterate the search results pagination
169 |         """
170 |         return Pagination(self, start, end, page_size, limit)
171 | 


--------------------------------------------------------------------------------
/serpapi/serp_api_client_exception.py:
--------------------------------------------------------------------------------
1 | class SerpApiClientException(Exception):
2 |     pass


--------------------------------------------------------------------------------
/serpapi/walmart_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | from serpapi.constant import *
 4 | 
 5 | class WalmartSearch(SerpApiClient):
 6 |     """WalmartSearch enables to search google scholar and parse the result.
 7 |     ```python
 8 |     from serpapi import WalmartSearch
 9 |     search = WalmartSearch({"query": "chair"})
10 |     data = search.get_dict()
11 |     ```
12 | 
13 |     doc: https://serpapi.com/walmart-search-api
14 |     """
15 | 
16 |     def __init__(self, params_dict):
17 |         super(WalmartSearch, self).__init__(params_dict, WALMART_ENGINE)
18 | 
19 |     def get_location(self, q, limit = 5):
20 |         raise SerpApiClientException("location is not supported by walmart search engine")
21 | 


--------------------------------------------------------------------------------
/serpapi/yahoo_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | 
 4 | class YahooSearch(SerpApiClient):
 5 |     """YahooSearch enables to search yahoo and parse the result.
 6 |     ```python
 7 |     from serpapi import YahooSearch
 8 |     query = YahooSearch({"p": "coffee"})
 9 |     data = query.get_json()
10 |     ```
11 | 
12 |     doc: https://serpapi.com/yahoo-search-api
13 |     """
14 | 
15 |     def __init__(self, params_dict):
16 |         super(YahooSearch, self).__init__(params_dict, YAHOO_ENGINE)
17 | 
18 |     def get_location(self, q, limit = 5):
19 |         raise SerpApiClientException("location is not supported by Yahoo search engine at this time")
20 | 


--------------------------------------------------------------------------------
/serpapi/yandex_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | 
 4 | class YandexSearch(SerpApiClient):
 5 |     """YandexSearch enables to search yandex and parse the result.
 6 |     ```python
 7 |     from serpapi import YandexSearch
 8 |     query = YandexSearch({"text": "coffee"})
 9 |     data = query.get_json()
10 |     ```
11 | 
12 |     doc: https://serpapi.com/yandex-search-api
13 |     """
14 | 
15 |     def __init__(self, params_dict):
16 |         super(YandexSearch, self).__init__(params_dict, YANDEX_ENGINE)
17 | 
18 |     def get_location(self, q, limit = 5):
19 |         raise SerpApiClientException("location is not supported by Yandex search engine at this time")
20 | 


--------------------------------------------------------------------------------
/serpapi/youtube_search.py:
--------------------------------------------------------------------------------
 1 | from serpapi.serp_api_client import *
 2 | from serpapi.serp_api_client_exception import SerpApiClientException
 3 | 
 4 | class YoutubeSearch(SerpApiClient):
 5 |     """YoutubeSearch enables to search google scholar and parse the result.
 6 |     ```python
 7 |     from serpapi import YoutubeSearch
 8 |     query = YoutubeSearch({"search_query": "chair"})
 9 |     data = query.get_dict()
10 |     ```
11 | 
12 |     doc: https://serpapi.com/youtube-search-api
13 |     """
14 | 
15 |     def __init__(self, params_dict):
16 |         super(YoutubeSearch, self).__init__(params_dict, YOUTUBE_ENGINE)
17 | 
18 |     def get_location(self, q, limit = 5):
19 |         raise SerpApiClientException("location is not supported by youtube search engine")
20 | 


--------------------------------------------------------------------------------
/setup.py:
--------------------------------------------------------------------------------
 1 | from setuptools import setup, find_packages
 2 | from codecs import open
 3 | from os import path
 4 | 
 5 | here = path.abspath(path.dirname(__file__))
 6 | 
 7 | with open('README.md', mode='r', encoding='utf-8') as fp:
 8 |     README = fp.read()
 9 | 
10 | setup(name='google_search_results',
11 |       version='2.4.2',
12 |       description='Scrape and search localized results from Google, Bing, Baidu, Yahoo, Yandex, Ebay, Homedepot, youtube at scale using SerpApi.com',
13 |       url='https://github.com/serpapi/google-search-results-python',
14 |       author='vikoky',
15 |       author_email='victor@serpapi.com',
16 |       classifiers=[
17 |         'License :: OSI Approved :: MIT License',
18 |         'Programming Language :: Python :: 3.5',
19 |         'Programming Language :: Python :: 3.6',
20 |         'Programming Language :: Python :: 3.7',
21 |         'Programming Language :: Python :: 3.8',
22 |         'Programming Language :: Python :: 3.9',
23 |         'Natural Language :: English',
24 |         'Topic :: Utilities',
25 |         ],
26 |     python_requires='>=3.5',
27 |     zip_safe=False,
28 |     include_package_data=True,
29 |     license="MIT",
30 |     install_requires = ["requests"],
31 |     packages=find_packages(),
32 |     keywords='scrape,serp,api,json,search,localized,rank,google,bing,baidu,yandex,yahoo,ebay,scale,datamining,training,machine,ml,youtube,naver,walmart,apple,store,app',
33 |     long_description=README,
34 |     long_description_content_type="text/markdown",
35 | )
36 | 


--------------------------------------------------------------------------------
/tests/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/serpapi/google-search-results-python/264be6d62fda3e38114b7df5dfc1d3f480e58507/tests/__init__.py


--------------------------------------------------------------------------------
/tests/test_account_api.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | from serpapi import GoogleSearch
 5 | 
 6 | class TestAccountApi(unittest.TestCase):
 7 | 
 8 |     def setUp(self):
 9 |         GoogleSearch.SERP_API_KEY = os.getenv("API_KEY","demo")
10 | 
11 |     @unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
12 |     def test_get_account(self):
13 |         search = GoogleSearch({})
14 |         account = search.get_account()
15 |         self.assertIsNotNone(account.get("account_id"))
16 |         self.assertEqual(account.get("api_key"), GoogleSearch.SERP_API_KEY)
17 | 
18 | if __name__ == '__main__':
19 |     unittest.main()
20 | 


--------------------------------------------------------------------------------
/tests/test_apple_app_store_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import AppleAppStoreSearch
 6 | 
 7 | class TestAppleAppStoreSearch(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				AppleAppStoreSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = AppleAppStoreSearch({"term": "Coffee"})
15 | 				data = search.get_dict()
16 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
17 | 				#self.assertIsNotNone(data["search_metadata"]["app_store_url"])
18 | 				self.assertIsNotNone(data["search_metadata"]["id"])
19 | 				if "organic_results" in data:
20 | 					self.assertIsNotNone(data["organic_results"][1]["title"])
21 | 				pp = pprint.PrettyPrinter(indent=2)
22 | 				pp.pprint(data)
23 | 				print(data.keys())
24 | 
25 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
26 | 		def test_paginate(self):
27 | 				page_size = 20
28 | 				search = AppleAppStoreSearch({"term": "Coffee", "page": 0, "num": page_size})
29 | 
30 | 				limit = 4
31 | 				pages = search.pagination(limit=limit)
32 | 
33 | 				page_count = 0
34 | 				result_count = 0
35 | 
36 | 				for page in pages:
37 | 					page_count += 1
38 | 					result_count += len(page["organic_results"])
39 | 
40 | 				self.assertEqual(page_count, limit)
41 | 
42 | if __name__ == '__main__':
43 | 		unittest.main()
44 | 


--------------------------------------------------------------------------------
/tests/test_baidu_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import BaiduSearch
 6 | 
 7 | class TestBaiduSearchApi(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				BaiduSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = BaiduSearch({"q": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["baidu_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 				self.assertIsNotNone(data["organic_results"][0]["title"])
21 | 				pp = pprint.PrettyPrinter(indent=2)
22 | 				pp.pprint(data)
23 | 
24 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
25 | 		def test_paginate(self):
26 | 				page_size = 30
27 | 				search = BaiduSearch({"q": "Coffee", "pn": 10, "m": page_size})
28 | 
29 | 				limit = 3
30 | 				pages = search.pagination(limit=limit)
31 | 
32 | 				page_count = 0
33 | 				result_count = 0
34 | 
35 | 				for page in pages:
36 | 					page_count += 1
37 | 					result_count += len(page["organic_results"])
38 | 
39 | 				self.assertEqual(page_count, limit)
40 | 
41 | if __name__ == '__main__':
42 | 		unittest.main()
43 | 


--------------------------------------------------------------------------------
/tests/test_bing_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import BingSearch
 6 | 
 7 | class TestBingSearchApi(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				BingSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = BingSearch({"q": "Coffee", "location": "Austin,Texas"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["bing_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 				self.assertIsNotNone(data["organic_results"][0]["title"])
21 | 				# pp = pprint.PrettyPrinter(indent=2)
22 | 				# pp.pprint(data)
23 | 
24 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
25 | 		def test_paginate(self):
26 | 				page_size = 20
27 | 				search = BingSearch({"q": "Coffee", "location": "Austin,Texas", "first": 10, "count": page_size})
28 | 
29 | 				limit = 4
30 | 				pages = search.pagination(limit=limit)
31 | 
32 | 				page_count = 0
33 | 				result_count = 0
34 | 
35 | 				for page in pages:
36 | 					page_count += 1
37 | 					result_count += len(page["organic_results"])
38 | 
39 | 				self.assertEqual(page_count, limit)
40 | 
41 | if __name__ == '__main__':
42 | 		unittest.main()
43 | 


--------------------------------------------------------------------------------
/tests/test_duck_duck_go_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import DuckDuckGoSearch
 6 | 
 7 | @unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
 8 | class TestDuckDuckGoSearch(unittest.TestCase):
 9 | 
10 | 		def setUp(self):
11 | 				DuckDuckGoSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
12 | 
13 | 		def test_get_json(self):
14 | 				search = DuckDuckGoSearch({"q": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["duckduckgo_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 
21 | 				for organic_result in data.get("organic_results", []):
22 | 						self.assertIsNotNone(organic_result.get("title"))
23 | 
24 | 				# pp = pprint.PrettyPrinter(indent=2)
25 | 				# pp.pprint(data)
26 | 				self.assertTrue(len(data.keys()) > 3)
27 | 
28 | 		def test_paginate_page_size(self):
29 | 				limit = 3
30 | 
31 | 				params = {
32 | 					"q": "coffee",
33 | 				}
34 | 
35 | 				titles = []
36 | 
37 | 				search = DuckDuckGoSearch(params)
38 | 				pages = search.pagination(limit=limit)
39 | 
40 | 				page_number = 0
41 | 				count = 0
42 | 
43 | 				for page in pages:
44 | 					page_number += 1
45 | 
46 | 					for organic_results in page.get("organic_results", []):
47 | 						count += 1
48 | 						title_index = 0
49 | 
50 | 						for title in titles:
51 | 							title_index += 1
52 | 
53 | 							if title == organic_results.get('title'):
54 | 								print("%d duplicated title: %s at index: %d" % (count, title, title_index))
55 | 
56 | 						titles.append(organic_results['title'])
57 | 
58 | 				self.assertEqual(page_number, limit, "Number of pages doesn't match.")
59 | 
60 | 
61 | if __name__ == '__main__':
62 | 		unittest.main()
63 | 


--------------------------------------------------------------------------------
/tests/test_ebay_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import EbaySearch
 6 | 
 7 | class TestEbaySearchApi(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				EbaySearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = EbaySearch({"_nkw": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["ebay_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 				self.assertIsNotNone(data["organic_results"][0]["title"])
21 | 
22 | 				for organic_result in data.get("organic_results", []):
23 | 						self.assertIsNotNone(organic_result.get("title"))
24 | 
25 | 				# pp = pprint.PrettyPrinter(indent=2)
26 | 				# pp.pprint(data)
27 | 
28 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
29 | 		def test_paginate(self):
30 | 			page_size = 60
31 | 
32 | 			params = {
33 | 				"_nkw": "coffee",
34 | 				"_ipg": page_size,
35 | 			}
36 | 
37 | 			search = EbaySearch(params)
38 | 
39 | 			limit = 3
40 | 			pages = search.pagination(limit = limit)
41 | 
42 | 			page_count = 0
43 | 			result_count = 0
44 | 
45 | 			for page in pages:
46 | 				page_count += 1
47 | 				result_count += len(page["organic_results"])
48 | 
49 | 			self.assertEqual(page_count, limit)
50 | 			self.assertEqual(result_count, page_size * limit)
51 | 
52 | if __name__ == '__main__':
53 | 		unittest.main()
54 | 


--------------------------------------------------------------------------------
/tests/test_example.py:
--------------------------------------------------------------------------------
  1 | # Unit testing
  2 | import unittest
  3 | 
  4 | # Operating system
  5 | import os
  6 | 
  7 | # regular expression library
  8 | import re
  9 | 
 10 | # safe queue 
 11 | import sys
 12 | if (sys.version_info > (3, 0)):
 13 |   from queue import Queue
 14 | else:
 15 |   from Queue import Queue
 16 |   
 17 | # Time utility
 18 | import time
 19 | 
 20 | # Serp API search
 21 | from serpapi import GoogleSearch
 22 | 
 23 | # download file with wget
 24 | #import wget
 25 | 
 26 | class TestExample(unittest.TestCase):
 27 | 
 28 |     def setUp(self):
 29 |         GoogleSearch.SERP_API_KEY = os.getenv("API_KEY","demo")
 30 | 
 31 |     @unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
 32 |     def test_get_json(self):
 33 |         search = GoogleSearch({"q": "Coffee", "engine": "google_scholar"})
 34 |         data = search.get_json()
 35 |         print(data['search_metadata'])
 36 |         search_id = data['search_metadata']['id']
 37 |         # retrieve search from the archive - blocker
 38 |         print(search_id + ": get search from archive")
 39 |         raw_html =  search.get_search_archive(search_id, 'html')
 40 |         # print(search_id + ": status = " + search_archived['search_metadata']['status'])
 41 |         print(raw_html)
 42 |         #print(search_html)
 43 | 
 44 |     @unittest.skipIf((os.getenv("DEBUGAPI_KEY") == None), "no api_key provided")
 45 |     def test_search_google_images(self):
 46 |         search = GoogleSearch({"q": "coffe", "tbm": "isch"})
 47 |         for image_result in search.get_json()['images_results']:
 48 |             try:
 49 |                 link = image_result["original"]
 50 |                 print("link is found: " + link)
 51 |                 # uncomment the line below to down the original image
 52 |                 # wget.download(link, '.')
 53 |             except:
 54 |                 print("link is not found.")
 55 |                 pass
 56 |             # https://github.com/serpapi/showcase-serpapi-tensorflow-keras-image-training/blob/master/fetch.py
 57 | 
 58 |     @unittest.skipIf((os.getenv("DEBUGAPI_KEY") == None), "no api_key provided")
 59 |     def test_async(self):
 60 |         # store searches
 61 |         search_queue = Queue()
 62 |         
 63 |         # Serp API search
 64 |         search = GoogleSearch({
 65 |             "location": "Austin,Texas",
 66 |             "async": True
 67 |         })
 68 |         
 69 |         # loop through companies
 70 |         for company in ['amd','nvidia','intel']:
 71 |           print("execute async search: q = " + company)
 72 |           search.params_dict["q"] = company
 73 |           data = search.get_dict()
 74 |           if data is not None:
 75 |               print("oops data is empty for: " + company)
 76 |               continue
 77 |           print("add search to the queue where id: " + data['search_metadata']['id'])
 78 |           # add search to the search_queue
 79 |           search_queue.put(data)
 80 |         
 81 |         print("wait until all search statuses are cached or success")
 82 |         
 83 |         # Create regular search
 84 |         search = GoogleSearch({"async": True})
 85 |         while not search_queue.empty():
 86 |           data = search_queue.get()
 87 |           search_id = data['search_metadata']['id']
 88 | 
 89 |           # retrieve search from the archive - blocker
 90 |           print(search_id + ": get search from archive")
 91 |           search_archived =  search.get_search_archive(search_id)
 92 |           print(search_id + ": status = " + search_archived['search_metadata']['status'])
 93 |           
 94 |           # check status
 95 |           if re.search('Cached|Success', search_archived['search_metadata']['status']):
 96 |             print(search_id + ": search done with q = " + search_archived['search_parameters']['q'])
 97 |           else:
 98 |             # requeue search_queue
 99 |             print(search_id + ": requeue search")
100 |             search_queue.put(search)
101 |             # wait 1s
102 |             time.sleep(1)
103 |         # search is over.
104 |         print('all searches completed')
105 |         
106 |     @unittest.skipIf((os.getenv("DEBUGAPI_KEY") == None), "no api_key provided")
107 |     def test_search_google_news(self):
108 |         search = GoogleSearch({
109 |             "q": "coffe",   # search search
110 |             "tbm": "nws",   # news
111 |             "tbs": "qdr:d", # last 24h
112 |             "num": 10
113 |         })
114 |         for offset in [0,1,2]:
115 |             search.params_dict["start"] = offset * 10
116 |             data = search.get_json()
117 |             for news_result in data['news_results']:
118 |                 print(str(news_result['position'] + offset * 10) + " - " + news_result['title'])
119 | 
120 |     @unittest.skipIf((os.getenv("DEBUGAPI_KEY") == None), "no api_key provided")
121 |     def test_search_google_shopping(self):
122 |         search = GoogleSearch({
123 |             "q": "coffe",   # search search
124 |             "tbm": "shop",  # news
125 |             "tbs": "p_ord:rv", # last 24h
126 |             "num": 100
127 |         })
128 |         data = search.get_json()
129 |         if 'shopping_results' in data:
130 |             for shopping_result in data['shopping_results']:
131 |                 print(str(shopping_result['position']) + " - " + shopping_result['title'])
132 |         else:
133 |             print("WARNING: oops shopping_results is missing from search result with tbm=shop")
134 |     
135 |     @unittest.skipIf((os.getenv("DEBUGAPI_KEY") == None), "no api_key provided")
136 |     def test_search_by_location(self):
137 |         for city in ["new york", "paris", "berlin"]:
138 |             location = GoogleSearch({}).get_location(city, 1)[0]["canonical_name"]
139 |             search = GoogleSearch({
140 |                 "q": "best coffee shop",   # search search
141 |                 "location": location,
142 |                 "num": 10,
143 |                 "start": 0
144 |             })
145 |             data = search.get_json()
146 |             self.assertIsNone(data.get("error"))
147 |             top_result = data['organic_results'][0]["title"]
148 |             print("top coffee result for " + location + " is: " + top_result)
149 | 
150 | 
151 | if __name__ == '__main__':
152 |     unittest.main()
153 | 


--------------------------------------------------------------------------------
/tests/test_example_paginate.py:
--------------------------------------------------------------------------------
 1 | import unittest
 2 | import os
 3 | from serpapi import GoogleSearch
 4 | 
 5 | # original code: https://replit.com/@DimitryZub1/Scrape-Google-News-with-Pagination-python-serpapi
 6 | class TestExamplePaginate(unittest.TestCase):
 7 |     
 8 |     @unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
 9 |     def test_paginate(self):
10 |       # to get 2 pages
11 |       limit = 2
12 |       # basic search parameters
13 |       params = {
14 |         "q": "coca cola",
15 |         "tbm": "nws",
16 |         "api_key": os.getenv("API_KEY")
17 |       }
18 |       # as proof of concept 
19 |       #  title collects
20 |       title = []
21 | 
22 |       # initialize a search
23 |       search = GoogleSearch(params)
24 | 
25 |       # create a python generator
26 |       pages = search.pagination(limit=limit)
27 |       # fetch one search result per iteration 
28 |       #  using a basic python for loop 
29 |       #   which invokes python iterator under the hood.
30 | 
31 |       page_count = 0
32 | 
33 |       for page in pages:
34 |         page_count += 1
35 |         #print(f"Current page: {page['serpapi_pagination']['current']}")
36 |         for news_result in page["news_results"]:
37 |             #print(f"Title: {news_result['title']}\nLink: {news_result['link']}\n")
38 |             title.append(news_result['title'])
39 | 
40 |       # double check if things adds up.
41 |       # total number pages expected
42 |       #  the exact number if variable depending on the search engine backend
43 |       self.assertEqual(page_count, limit)
44 |       # self.assertEqual(len(title), 20, "number of search results")
45 |       #self.assertEqual(len(set(title)), len(title), "duplicated elements detected")
46 | 
47 |     @unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
48 |     def test_paginate_page_size(self):
49 |       # to get 4 pages with each page contains 20 search results
50 |       start = 0
51 |       end = 80
52 |       page_size = 20
53 | 
54 |       limit = (end - start) / page_size
55 | 
56 |       # use parameters in
57 |       params = {
58 |         "q": "coca cola",
59 |         "tbm": "nws",
60 |         "api_key": os.getenv("API_KEY"),
61 |         "start": start,
62 |         "end": end,
63 |         "num": page_size
64 |       }
65 | 
66 |       title = []
67 | 
68 |       search = GoogleSearch(params)
69 | 
70 |       # parameter limit will be used instead of pagination
71 |       pages = search.pagination(limit=limit)
72 | 
73 |       page_count = 0
74 |       count = 0
75 | 
76 |       for page in pages:
77 |         page_count += 1
78 |         # print(f"Current page: {page['serpapi_pagination']['current']}")
79 |         for news_result in page["news_results"]:
80 |             count += 1
81 |             i = 0
82 |             for t in title:
83 |               i += 1
84 |               if t == news_result['title']:
85 |                 print(("%d duplicated title: %s at index: %d" % (count, t, i)))
86 |             #print(f"{count} - title: {news_result['title']}")
87 |             title.append(news_result['title'])
88 | 
89 |       # check number of pages match
90 |       self.assertEqual(page_count, limit, "Number of pages doesn't match.")
91 |       # google randomly duplicated search result
92 |       # self.assertEqual(len(set(title)), end, "duplicated search results")
93 | 


--------------------------------------------------------------------------------
/tests/test_google_scholar_search_api.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import GoogleScholarSearch
 6 |    
 7 | class TestGoogleScholarSearch(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				GoogleScholarSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = GoogleScholarSearch({"q": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["id"])
19 | 				self.assertIsNotNone(data["organic_results"][0]["title"])
20 | 
21 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
22 | 		def test_paginate(self):
23 | 				page_size = 20
24 | 				search = GoogleScholarSearch({"q": "Coffee", "start": 10, "num": page_size})
25 | 
26 | 				limit = 3
27 | 				pages = search.pagination(limit=limit)
28 | 				page_count = 0
29 | 				result_count = 0
30 | 
31 | 				for page in pages:
32 | 						page_count += 1
33 | 						result_count += len(page["organic_results"])
34 | 
35 | 				self.assertEqual(page_count, limit)
36 | 
37 | if __name__ == '__main__':
38 | 		unittest.main()
39 | 


--------------------------------------------------------------------------------
/tests/test_google_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | import requests
 6 | from serpapi import GoogleSearch
 7 | 
 8 | class TestSearchApi(unittest.TestCase):
 9 | 
10 | 		def setUp(self):
11 | 				GoogleSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
12 | 
13 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
14 | 		def test_paginate(self):
15 | 				page_size = 20
16 | 				search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas", "start": 10, "num": page_size})
17 | 
18 | 				limit = 2
19 | 				pages = search.pagination(limit=limit)
20 | 
21 | 				page_count = 0
22 | 
23 | 				for page in pages:
24 | 					page_count += 1
25 | 
26 | 				self.assertEqual(page_count, limit)
27 | 
28 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
29 | 		def test_get_json(self):
30 | 				search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
31 | 				data = search.get_json()
32 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
33 | 				self.assertIsNone(data.get("error"))
34 | 				self.assertIsNotNone(data["search_metadata"]["google_url"])
35 | 				self.assertIsNotNone(data["search_metadata"]["id"])
36 | 				self.assertIsNotNone(data['local_results']['places'][0])
37 | 
38 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
39 | 		def test_get_json(self):
40 | 				search = GoogleSearch({"q": "Coffee", "engine": "google_scholar"})
41 | 				data = search.get_json()
42 | 
43 | 				for organic_result in data["organic_results"]:
44 | 					self.assertIsNotNone(organic_result["title"])
45 | 
46 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
47 | 		def test_get_dict(self):
48 | 				search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
49 | 				data = search.get_dict()
50 | 				self.assertIsNotNone(data.get('local_results'))
51 | 
52 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
53 | 		def test_get_dictionary(self):
54 | 				search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
55 | 				data = search.get_dictionary()
56 | 				self.assertIsNotNone(data.get('local_results'))
57 | 
58 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
59 | 		def test_get_html(self):
60 | 				search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
61 | 				data = search.get_html()
62 | 				self.assertGreater(len(data), 10)
63 | 				self.assertIn("<html", data)
64 | 				
65 | 				data = search.get_dict()
66 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
67 | 				self.assertIsNone(data.get("error"))
68 | 
69 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
70 | 		def test_get_response(self):
71 | 				search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
72 | 				response = search.get_response()
73 | 				self.assertEqual(type(response), requests.Response)
74 | 				self.assertGreater(len(response.text), 10)
75 | 
76 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
77 | 		def test_get_object(self):
78 | 				search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
79 | 				r = search.get_object()
80 | 				self.assertEqual(type(r.organic_results), list)
81 | 				self.assertIsNotNone(r.organic_results[0].title)
82 | 				self.assertIsNotNone(r.search_metadata.id)
83 | 				self.assertIsNotNone(r.search_metadata.google_url)
84 | 				self.assertEqual(r.search_parameters.q, "Coffee")
85 | 				self.assertEqual(r.search_parameters.engine, "google")
86 | 				self.assertGreater(r.search_information.total_results, 10)
87 | 
88 | if __name__ == '__main__':
89 | 		unittest.main()
90 | 


--------------------------------------------------------------------------------
/tests/test_home_depot_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import HomeDepotSearch
 6 | 
 7 | class TestHomeDepotSearchApi(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				HomeDepotSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = HomeDepotSearch({"q": "chair"})
15 | 				data = search.get_dict()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["home_depot_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 				self.assertTrue(len(data["products"]) > 5)
21 | 
22 | 				for product in data.get("products", []):
23 | 					self.assertIsNotNone(product["title"])
24 | 
25 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
26 | 		def test_get_object(self):
27 | 				search = HomeDepotSearch({"q": "chair"})
28 | 				data = search.get_object()
29 | 				self.assertEqual(data.search_metadata.status, "Success")
30 | 				self.assertEqual(type(data.products), list)
31 | 				self.assertIsNotNone(data.products[0].title)
32 | 				self.assertIsNotNone(data.search_metadata.id)
33 | 				self.assertIsNotNone(data.search_metadata.home_depot_url)
34 | 				self.assertEqual(data.search_parameters.q, "chair")
35 | 				self.assertEqual(data.search_parameters.engine, "home_depot")
36 | 				self.assertGreater(data.search_information.total_results, 10)
37 | 
38 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
39 | 		def test_paginate_page_size(self):
40 | 			start = 24
41 | 			limit = 3
42 | 
43 | 			# use parameters in
44 | 			params = {
45 | 				"q": "coffee",
46 | 				"start": start,
47 | 			}
48 | 
49 | 			titles = []
50 | 
51 | 			search = HomeDepotSearch(params)
52 | 			pages = search.pagination(limit=limit)
53 | 
54 | 			page_number = 0
55 | 			count = 0
56 | 
57 | 			for page in pages:
58 | 				page_number += 1
59 | 
60 | 				for product in page.get("products", []):
61 | 					count += 1
62 | 					i = 0
63 | 
64 | 					for t in titles:
65 | 						i += 1
66 | 
67 | 						if t == product.get('title'):
68 | 							print("%d duplicated title: %s at index: %d" % (count, t, i))
69 | 
70 | 					titles.append(product['title'])
71 | 
72 | 			self.assertEqual(page_number, limit, "Number of pages doesn't match.")
73 | 
74 | if __name__ == '__main__':
75 | 		unittest.main()
76 | 


--------------------------------------------------------------------------------
/tests/test_location_api.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import pprint
 4 | import os
 5 | from serpapi import GoogleSearch
 6 | 
 7 | class TestLocationApi(unittest.TestCase):
 8 | 
 9 |     def setUp(self):
10 |         GoogleSearch.SERP_API_KEY = os.getenv("API_KEY","demo")
11 | 
12 |     def test_get_location(self):
13 |         search = GoogleSearch({"q": None, "async": True})
14 |         location_list = search.get_location("Austin", 3)
15 |         pp = pprint.PrettyPrinter(indent=2)
16 |         pp.pprint(location_list)
17 |         self.assertIsNotNone(location_list[0].get("id"))
18 | 
19 | if __name__ == '__main__':
20 |     unittest.main()
21 | 


--------------------------------------------------------------------------------
/tests/test_naver_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import NaverSearch
 6 | 
 7 | class TestNaverSearchApi(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				NaverSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = NaverSearch({"query": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["naver_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 
21 | 				for ad in data.get("ads_results", []):
22 | 					self.assertIsNotNone(ad["title"])
23 | 
24 | 				for organic_result in data.get("web_results", []):
25 | 					self.assertIsNotNone(organic_result["title"])
26 | 
27 | 				pp = pprint.PrettyPrinter(indent=2)
28 | 				pp.pprint(data)
29 | 				print(data.keys())
30 | 
31 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
32 | 		def test_paginate_page_size(self):
33 | 			start = 24
34 | 			limit = 3
35 | 
36 | 			# use parameters in
37 | 			params = {
38 | 				"query": "coffee",
39 | 				"start": start,
40 | 			}
41 | 
42 | 			titles = []
43 | 
44 | 			search = NaverSearch(params)
45 | 			pages = search.pagination(limit=limit)
46 | 
47 | 			page_number = 0
48 | 			count = 0
49 | 
50 | 			for page in pages:
51 | 				page_number += 1
52 | 
53 | 				for result in page.get("web_results", []):
54 | 					count += 1
55 | 					i = 0
56 | 
57 | 					for item in titles:
58 | 						i += 1
59 | 
60 | 						if item == result.get('title'):
61 | 							print("%d duplicated title: %s at index: %d" % (count, item, i))
62 | 
63 | 					titles.append(result['title'])
64 | 
65 | 			self.assertEqual(page_number, limit, "Number of pages doesn't match.")
66 | 
67 | if __name__ == '__main__':
68 | 		unittest.main()
69 | 


--------------------------------------------------------------------------------
/tests/test_search_archive_api.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | from serpapi import GoogleSearch
 5 | 
 6 | class TestSearchArchiveApi(unittest.TestCase):
 7 | 
 8 |     def setUp(self):
 9 |         GoogleSearch.SERP_API_KEY = os.getenv("API_KEY","demo")
10 | 
11 |     @unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
12 |     def test_get_search_archive(self):
13 |         search = GoogleSearch({"q": "Coffee", "location": "Austin,Texas"})
14 |         search_result = search.get_dictionary()
15 |         search_id = search_result.get("search_metadata").get("id")
16 |         archived_search_result = GoogleSearch({}).get_search_archive(search_id, 'json')
17 |         self.assertEqual(archived_search_result.get("search_metadata").get("id"), search_id)
18 |         html_buffer = GoogleSearch({}).get_search_archive(search_id, 'html')
19 |         self.assertGreater(len(html_buffer), 10000)
20 | 
21 | if __name__ == '__main__':
22 |     unittest.main()
23 | 


--------------------------------------------------------------------------------
/tests/test_serp_api_client.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import SerpApiClient
 6 | from serpapi.serp_api_client_exception import SerpApiClientException
 7 | import pytest
 8 | 
 9 | # This test shows how to extends SerpApiClient
10 | #  without using search engine wrapper.
11 | # 
12 | class TestSerpSearchApi(unittest.TestCase):
13 | 
14 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
15 | 		def test_get_json(self):
16 | 			search = SerpApiClient({
17 | 				"q": "Coffee", 
18 | 				"location": "Austin,Texas", 
19 | 				"engine": "google_scholar",
20 | 				"api_key": os.getenv("API_KEY")
21 | 				})
22 | 			data = search.get_json()
23 | 			assert data.get("error") == None
24 | 			self.assertIsNotNone(data["organic_results"][0]["title"])
25 | 
26 | 		def test_invalid_api_key(self):
27 | 			search = SerpApiClient({
28 | 				"q": "Coffee", 
29 | 				"location": "USA", 
30 | 				"engine": "google",
31 | 				"api_key": "invalid_api_key"
32 | 			})
33 | 			data = search.get_json()
34 | 			self.assertIsNotNone(data["error"])
35 | 
36 | 		def test_error_missing_engine(self):
37 | 			search = SerpApiClient({
38 | 				"q": "Coffee", 
39 | 				"api_key": os.getenv("API_KEY")
40 | 			})
41 | 			with pytest.raises(SerpApiClientException):
42 | 				search.get_json()
43 | 
44 | 		def test_missing_(self):
45 | 			search = SerpApiClient({
46 | 				"location": "USA", 
47 | 				"engine": "google",
48 | 				"api_key": os.getenv("API_KEY")
49 | 			})
50 | 			data = search.get_json()
51 | 			self.assertIsNotNone(data["error"])
52 | 			self.assertRegex(data["error"], "Missing query `q`")
53 | 
54 | 		def debug(self, payload):
55 | 			pp = pprint.PrettyPrinter(indent=2)
56 | 			pp.pprint(payload)
57 | 
58 | if __name__ == '__main__':
59 | 		unittest.main()
60 | 


--------------------------------------------------------------------------------
/tests/test_walmart_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import WalmartSearch
 6 | 
 7 | 
 8 | class TestWalmartSearchApi(unittest.TestCase):
 9 | 		def setUp(self):
10 | 				WalmartSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = WalmartSearch({"query": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["walmart_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 
21 | 				for organic_result in data.get("organic_results", []):
22 | 						self.assertIsNotNone(organic_result.get("title"))
23 | 
24 | 				pp = pprint.PrettyPrinter(indent=2)
25 | 				pp.pprint(data)
26 | 				print(data.keys())
27 | 
28 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
29 | 		def test_paginate(self):
30 | 				page_size = 40
31 | 				search = WalmartSearch({"query": "coffee", "ps": page_size})
32 | 
33 | 				limit = 4
34 | 				pages = search.pagination(limit=limit)
35 | 
36 | 				product_ids = []
37 | 				page_number = 0
38 | 
39 | 				for page in pages:
40 | 						organic_results_count = 0
41 | 						page_number += 1
42 | 
43 | 						for organic_result in page.get("organic_results", []):
44 | 								organic_results_count += 1
45 | 								product_id_index = 0
46 | 
47 | 								for id in product_ids:
48 | 										product_id_index += 1
49 | 
50 | 										if id == organic_result.get("product_id"):
51 | 												print("%d duplicated product_id: %s at index: %d" % (organic_results_count, id, product_id_index))
52 | 
53 | 								product_ids.append(organic_result.get("product_id"))
54 | 
55 | 				self.assertEqual(page_number, limit, "Number of pages doesn't match.")
56 | 
57 | 
58 | if __name__ == "__main__":
59 | 		unittest.main()
60 | 


--------------------------------------------------------------------------------
/tests/test_yahoo_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import YahooSearch
 6 | 
 7 | class TestYahooSearchApi(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				YahooSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = YahooSearch({"p": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["yahoo_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 
21 | 				for organic_result in data.get("organic_results", []):
22 | 						self.assertIsNotNone(organic_result.get("title"))
23 | 
24 | 
25 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
26 | 		def test_paginate(self):
27 | 				page_size = 7
28 | 				search = YahooSearch({"p": "Coffee", "b": page_size, "pz": page_size})
29 | 
30 | 				limit = 4
31 | 				pages = search.pagination(limit=limit)
32 | 
33 | 				titles = []
34 | 				page_number = 0
35 | 
36 | 				for page in pages:
37 | 						organic_results_count = 0
38 | 						page_number += 1
39 | 
40 | 						for organic_result in page.get("organic_results", []):
41 | 								organic_results_count += 1
42 | 								title_index = 0
43 | 
44 | 								for title in titles:
45 | 										title_index += 1
46 | 
47 | 										if title == organic_result.get("title"):
48 | 												print("Organic result #%d on page #%d contains duplicated title: %s at index: %d" % (organic_results_count, page_number, title, title_index))
49 | 
50 | 								titles.append(organic_result.get("title"))
51 | 
52 | 				self.assertEqual(page_number, limit, "Number of pages doesn't match.")
53 | 
54 | if __name__ == '__main__':
55 | 		unittest.main()
56 | 


--------------------------------------------------------------------------------
/tests/test_yandex_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import YandexSearch
 6 | 
 7 | class TestYandexSearchApi(unittest.TestCase):
 8 | 
 9 | 		def setUp(self):
10 | 				YandexSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = YandexSearch({"text": "Coffee"})
15 | 				data = search.get_json()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["yandex_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 				pp = pprint.PrettyPrinter(indent=2)
21 | 				pp.pprint(data["organic_results"])
22 | 
23 | 				for organic_result in data.get("organic_results", []):
24 | 						self.assertIsNotNone(organic_result.get("title"))
25 | 
26 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
27 | 		def test_paginate(self):
28 | 				search = YandexSearch({"text": "Coffee"})
29 | 
30 | 				limit = 3
31 | 				pages = search.pagination(limit=limit)
32 | 
33 | 				titles = []
34 | 				page_number = 0
35 | 
36 | 				for page in pages:
37 | 						organic_results_count = 0
38 | 						page_number += 1
39 | 
40 | 						for organic_result in page.get("organic_results", []):
41 | 								organic_results_count += 1
42 | 								title_index = 0
43 | 
44 | 								for title in titles:
45 | 										title_index += 1
46 | 
47 | 										if title == organic_result.get("title"):
48 | 												print("%d duplicated title: %s at index: %d" % (organic_results_count, title, title_index))
49 | 
50 | 								titles.append(organic_result.get("title"))
51 | 
52 | 				self.assertEqual(page_number, limit, "Number of pages doesn't match.")
53 | 
54 | if __name__ == '__main__':
55 | 		unittest.main()
56 | 


--------------------------------------------------------------------------------
/tests/test_youtube_search.py:
--------------------------------------------------------------------------------
 1 | import random
 2 | import unittest
 3 | import os
 4 | import pprint
 5 | from serpapi import YoutubeSearch
 6 | 
 7 | 
 8 | class TestYoutubeSearchApi(unittest.TestCase):
 9 | 		def setUp(self):
10 | 				YoutubeSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
11 | 
12 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
13 | 		def test_get_json(self):
14 | 				search = YoutubeSearch({"search_query": "chair"})
15 | 				data = search.get_dict()
16 | 				self.assertIsNone(data.get("error"))
17 | 				self.assertEqual(data["search_metadata"]["status"], "Success")
18 | 				self.assertIsNotNone(data["search_metadata"]["youtube_url"])
19 | 				self.assertIsNotNone(data["search_metadata"]["id"])
20 | 
21 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
22 | 		def test_get_object(self):
23 | 				search = YoutubeSearch({"search_query": "chair"})
24 | 				data = search.get_object()
25 | 				self.assertEqual(data.search_metadata.status, "Success")
26 | 				self.assertIsNotNone(data.search_metadata.id)
27 | 				self.assertIsNotNone(data.search_metadata.youtube_url)
28 | 				self.assertEqual(data.search_parameters.search_query, "chair")
29 | 				self.assertEqual(data.search_parameters.engine, "youtube")
30 | 				self.assertGreater(data.search_information.total_results, 10)
31 | 
32 | 		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
33 | 		def test_paginate(self):
34 | 				search = YoutubeSearch({"search_query": "chair"})
35 | 
36 | 				limit = 3
37 | 				pages = search.pagination(limit=limit)
38 | 
39 | 				titles = []
40 | 
41 | 				page_count = 0
42 | 				count = 0
43 | 
44 | 				for page in pages:
45 | 						page_count += 1
46 | 
47 | 						for video_result in page.get("video_results", []):
48 | 								count += 1
49 | 								title_index = 0
50 | 
51 | 								for title in titles:
52 | 										title_index += 1
53 | 
54 | 										if title == video_result.get("title"):
55 | 												print("%d duplicated title: %s at index: %d" % (count, title, title_index))
56 | 
57 | 								titles.append(video_result.get("title"))
58 | 
59 | 				self.assertEqual(page_count, limit, "Number of pages doesn't match.")
60 | 
61 | 
62 | if __name__ == "__main__":
63 | 		unittest.main()
64 | 


--------------------------------------------------------------------------------
/testwrapper.py:
--------------------------------------------------------------------------------
 1 | from serpwrapper import QUERY
 2 | import sys
 3 | 
 4 | class NotEnoughArgsError(Exception):
 5 |     pass
 6 | def test_query():
 7 |     """Tests an API call to get a HTML content"""
 8 |     params = {}
 9 |     if len(sys.argv) < 3 :
10 |         raise NotEnoughArgsError(
11 |             "SerpApi requires user to put in Query and Location as command-line arguments"
12 |         )
13 |     params['query'] = sys.argv[1]
14 |     params['location'] = sys.argv[2]
15 |     if len(sys.argv) == 4:
16 |         params['ui_lang'] = sys.argv[3]
17 |     if len(sys.argv) == 5:
18 |         params['country'] = sys.argv[4]
19 |     if len(sys.argv) == 6:
20 |         params['num_results'] = sys.argv[5] if sys.argv[5] else None
21 |     # print query, location
22 |     query_instance = QUERY(None)
23 |     return query_instance.retrieve_html(params)
24 | 
25 |     # assert isinstance(response, dict)
26 |     # assert response['id'] == 1396, "The ID should be in the response"
27 | 
28 | test_query()
29 | 