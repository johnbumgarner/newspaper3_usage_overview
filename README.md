
## Primary objective of this repository
<p align="justify">
This repository was developed to provide technical insights on how to properly utilized the <i>Python</i> library <i>Newspaper3k</i> to query a news source, such as the <a href="https://www.wsj.com">Wall Street Journal.</a>
           
           
          
</p>

### Newspaper Configuration for Querying 

<p align="justify">
<i>Newspaper3k</i> uses the <i>Python requests</i> module to make a connection request to a news website. <i>Python requests</i> allows connections to have HTTP headers information and <i>Newspaper3k</i> includes this capability within its code base. These <i>Newspaper3k</i> configuration parameters include: sending a browser's user agent string as part of the request, establishing a connection timeout period (in seconds) and using proxies.  
           
Some website queried with <i>Newspaper3k</i> will send back status response code indicating a problem with the conenction.  These status response code include:

- HTTP 400 Bad Request error 
- HTTP 403 Forbidden client error
- HTTP 406 Not Acceptable client error

One of the primary root causes of these errors is the lack of a browser's user agent string in the request. 

Another potential issue when making requests with <i>Newspaper3k</i> is a <i>ReadTimeout</i> error.  These error are usually linked to not providing a connection timeout period in your request. The <i>Python requests</i> documentation makes a point that setting a connection timeout is considered best practice.
</p>

#### Configuration example

```python
from newspaper import Config

config = Config()
config.browser_user_agent = string value
config.proxies = dictionary of proxies
config.request_timeout = int value 
```

#### Sample usage example

```python
from newspaper import Config

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

# add your proxy information
PROXIES = {
           'http': "http://ip_address:port_number",
           'https': "https://ip_address:port_number"
          }

config = Config()
config.browser_user_agent = USER_AGENT
config.proxies = PROXIES
config.request_timeout = 10
```

#### Real world usage example

```python
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

url = 'https://www.wsj.com'
article = Article(url, config=config)
 <DO SOMETHING>
```

<p align="justify">
<i>Newspaper3k</i> also supports the use of HTTP headers via Config(). The headers are passed as a dictionary.     
</p>

#### Real world basic header usage example

```python
from newspaper import Config
from newspaper import Article

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
           
config = Config()
config.headers = HEADERS
config.request_timeout = 10

url = 'https://www.wsj.com'
article = Article(url, config=config)
 <DO SOMETHING>
```

### Newspaper Source Extraction 

<p align="justify">
One of the primary purposes of <i>Newspaper3k</i> is text extraction from a news website. Out-of-box <i>Newspaper3k</i> does a good job of extracting content, but it is not flawless.  Several of these extraction issues are posted as questions to either <a href="https://stackoverflow.com/search?q=newspaper3k">Stack Overflow</a> or to the GitHub repository for <a href="https://github.com/codelucas/newspaper/issues">Newspaper.</a>  Many of the extraction questions are directly related to an end-user not reviewing the news source's HTML code prior to querying the website with <i>Newspaper3k</i>. Any developer that has used <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">BeautifulSoup</a>, <a href="https://scrapy.org/">Scrapy</a> or <a href="https://selenium-python.readthedocs.io/">Selenium</a> to scrape a website knows that you need to review the portal's structure to properly extract content. 
</p>

### Newspaper Wall Street Journal Extraction 

<p align="justify">
The example below is querying an article on the Wall Street Journal and extracting several data elements from the page's HTML code. <i>Newspaper3k</i> was able to 
adequately extract the article's title and author of the article, but failed to extract the published data or the keywords related to this article. 
</p>

```python
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

url = 'https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1'
article = Article(url, config=config)
article.download()
article.parse()

print(article.title)
Investors Are Betting Corporate Earnings Have Turned a Corner

print(article.authors)
['Karen Langley']

print(article.publish_date)
None

print(article.keywords)
[] returned an empty list
```

<p align="justify">
The publish_date and keywords related to this Wall Street Journal article are located in mutiple meta tags and can be extracted by <i>Newspaper3k</i> using 
<i>article.meta_data.</i>  Addtional article data elements, such as authors, title and article summary are located with the meta tags used by the Wall Street Journal.
</p>

```python
from newspaper import Config
from newspaper import Article

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
config = Config()

config.headers = HEADERS
config.request_timeout = 10

url = 'https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1'
article = Article(url, config=config)
article.download()
article.parse()
article_meta_data = article.meta_data

article_published_date = str({value for (key, value) in article_meta_data.items() if key == 'article.published'})
print(article_published_date)
{'2020-10-11T09:30:00.000Z'}

article_author = sorted({value for (key, value) in article_meta_data.items()if key == 'author'})
print(article_author)
['Karen Langley']

article_title = {value for (key, value) in article_meta_data.items() if key == 'article.headline'}
print(article_title)
{'Investors Are Betting Corporate Earnings Have Turned a Corner'}

article_summary = {value for (key, value) in article_meta_data.items() if key == 'article.summary'}
print(article_summary)
{'Investors are entering third-quarter earnings season with brighter expectations for corporate profits, a bet they hope will propel the next leg of the stock market’s rally.'}

keywords = ''.join({value for (key, value) in article_meta_data.items() if key == 'news_keywords'})
article_keywords = sorted(keywords.lower().split(','))
print(article_keywords)
['c&e exclusion filter', 'c&e industry news filter', 'codes_reviewed', 'commodity/financial market news', 'content types', 'corporate/industrial news', 'earnings', 'equity markets', 'factiva filters', 'financial performance']
```
