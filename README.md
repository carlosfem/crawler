# WebCrawler

WebCrawler is a simple application focused on scraping a certain domain looking for pages following a specific pattern.

__Highlights__

- Request and parse web pages;
- Crawl entire domains looking for patterns;
- Exports csv files with the data collected;
- Parallelized architecture for more efficient searches.

## Getting Started

This project runs mostly on standard python libraries and is compatible with python 3.x

### Prerequisites

The only library required besides the standard libraries is BeautifulSoup. This library can be installed via pip as follows:

```
pip install beautifulsoup4
```

### Installing

To install WebCrawler run:

```
python setup.py install
```

### Testing

The package contains two test files, **core_unit_tests.py** and **helper_unit_tests.py**. The first is used to test the core functionalities of the project such as creating and parsing a web page and crawling a domain. The latter tests all of the helper functions defined in the **helpers** module.

The test module is doesn't require installation of the package, to test the core functions just run:

```
python tests\core_unit_tests.py
```

__Results:__
```
..............
----------------------------------------------------------------------
Ran 14 tests in 4.288s

OK
```

## Examples

After installing the package, it's very easy to begin scraping the web, the following code snippet shows a simple example of how to scrape the domain https://www.epocacosmeticos.com.br and export a csv file. The program runs with the following specifications:

- The search will be limited to 100 http requests;
- Ten parallel workers will be executing the requests;
- Not Working on "greedy" mode, i.e., inner html and child urls are deleted after parsing (saves memory);
- All pages found have the url, title and target name (if there's a match) stored and exported to a csv file;
- To identify a page as a target a lambda function is specified.

```
import crawler
crawler = crawler.Crawler("https://www.epocacosmeticos.com.br", req_limit=100, greedy=False,
                  indentify_target=lambda page: page.valid_target)
crawler.run(10)
crawler.export_csv("output", only_targets=False)
```

__Output:__
```
20:06:57 Initiating crawl...
Domain: https://www.epocacosmeticos.com.br
Request limit: 100
Greedy mode: No

Reloaded modules: helpers, webpage, decorators, thread_manager
20:06:57 Visited pages: 10; Targets found 0; Running visits 153
20:06:58 Visited pages: 20; Targets found 1; Running visits 153
20:06:59 Visited pages: 30; Targets found 1; Running visits 153
20:07:00 Visited pages: 40; Targets found 4; Running visits 153
20:07:01 Visited pages: 50; Targets found 5; Running visits 153
20:07:02 Visited pages: 60; Targets found 5; Running visits 153
20:07:03 Visited pages: 70; Targets found 5; Running visits 153
20:07:04 Visited pages: 80; Targets found 5; Running visits 153
20:07:05 Visited pages: 90; Targets found 5; Running visits 153
20:07:06 Visited pages: 100; Targets found 5; Running visits 153
20:07:08 Crawling completed...
```


## Code Style

The Python code in this repo is meant to follow the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) (a stylized version http://pep8.org).

## Authors
* **Carlos Monteiro** - [carlosfem](https://github.com/carlosfem)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.