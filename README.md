
### Last Updated: 10-11-2020

## Primary objective of this repository
<p align="justify">
This repository was developed to provide technical insights on how to properly utilized the <i>Python</i> library <i>Newspaper3k</i> to query news sourcees, such as the <a href="https://www.wsj.com">Wall Street Journal</a>, <a href="https://www.bbc.com">the BBC</a> and <a href="https://www.cnn.com">CNN</a>.
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

base_url = 'https://www.wsj.com'
article = Article(base_url, config=config)
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

base_url = 'https://www.wsj.com'
article = Article(base_url, config=config)
 <DO SOMETHING>
```

### Newspaper Source Extraction 

<p align="justify">
One of the primary purposes of <i>Newspaper3k</i> is text extraction from a news website. Out-of-box <i>Newspaper3k</i> does a good job of extracting content, but it is not flawless.  Several of these extraction issues are posted as questions to either <a href="https://stackoverflow.com/search?q=newspaper3k">Stack Overflow</a> or to the GitHub repository for <a href="https://github.com/codelucas/newspaper/issues">Newspaper.</a>  Many of the extraction questions are directly related to an end-user not reviewing the news source's HTML code prior to querying the website with <i>Newspaper3k</i>. Any developer that has used <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">BeautifulSoup</a>, <a href="https://scrapy.org/">Scrapy</a> or <a href="https://selenium-python.readthedocs.io/">Selenium</a> to scrape a website knows that you need to review the portal's structure to properly extract content. 
</p>

### CNN Extraction 
<p align="justify">
The example below is querying an article on the CNN website using <i>Newspaper3k</i>.  The article data elements; title, authors and date published are adequately  extracted using <i>Newspaper3k</i>.  The keywords for this article were not initial discovered by <i>Newspaper3k</i>, but modifying the parameter <i>article.keywords</i> to <i>meta_keywords</i> did yield the keywords related to this article. 
</p>

```python
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

url = 'https://www.cnn.com/2020/10/09/business/edinburgh-woollen-mill-job-cuts/index.html'
article = Article(url, config=config)
article.download()
article.parse()

print(article.title)
Another 24,000 retail jobs at risk as UK fashion group faces collapse

print(article.publish_date)
2020-10-09 00:00:00

print(article.authors)
['Hanna Ziady', 'Cnn Business']

print(article.keywords)
[] returned an empty list

print(article.meta_keywords)
['business', 'Edinburgh Woollen Mill: 24', '000 jobs at risk as company appoints administrators - CNN']
```

### Wall Street Journal Extraction 

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

base_url = 'https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1'
article = Article(base_url, config=config)
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
<i>article.meta_data.</i>  Addtional article data elements, such as authors, title and article summary are also located within the meta tags used by the Wall Street Journal.
</p>

```python
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

base_url = 'https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1'
article = Article(base_url, config=config)
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
{'Investors are entering third-quarter earnings season with brighter expectations for corporate profits, 
a bet they hope will propel the next leg of the stock market’s rally.'}

keywords = ''.join({value for (key, value) in article_meta_data.items() if key == 'news_keywords'})
article_keywords = sorted(keywords.lower().split(','))
print(article_keywords)
['c&e exclusion filter', 'c&e industry news filter', 'codes_reviewed', 'commodity/financial market news', 'content types', 
'corporate/industrial news', 'earnings', 'equity markets', 'factiva filters', 'financial performance']
```

### Fox News Extraction 

<p align="justify">
Extracting specific data elements from Fox News requires querying the meta tags. These data elements that can be obtain in are the title of the article, the published date of the article and a summary of the article.  Fox News does not use keywords, so extracting these is not possble.  Extracting the authors of the article is also problematic, because Fox News does not use a standard tag (e.g., by-line) for this information.  
</p>


```python
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

base_url = 'https://www.foxbusiness.com/economy/white-house-calls-for-interim-coronavirus-relief-as-negotiations-continue'
article = Article(url, config=config)
article.download()
article.parse()
article_meta_data = article.meta_data

article_title = {value for (key, value) in article_meta_data.items() if key == 'dc.title'}
print(article_title)
{'White House pushes for limited coronavirus relief bill as broader effort meets resistance'}

article_published_date = str({value for (key, value) in article_meta_data.items() if key == 'dcterms.created'})
print(article_published_date)
{'2020-10-11T12:51:53-04:00'}

article_summary = {value for (key, value) in article_meta_data.items() if key == 'dc.description'}
print(article_summary)
{'In the letter to House and Senate members, Mnuchin and Meadows said the White House would continue to talk to Senate Democratic Leader Chuck Schumer 
and House Speaker Nancy Pelosi, but that Congress should "immediately vote on a bill" that would enable the use of unused Paycheck Protection Program 
funds while working toward a bigger package.'}
```

<p align="justify">
Fox News stores the data elements article title, article summary, article author and date published in a <i>script</i> tag. These elements can be extracted using the <i>Python</i> modules <i>BeautifulSoup</i> and <i>JSON</i>. <i>BeautifulSoup</i> is a dependency of <i>Newspaper3k</i> and can be accessed through <i>newspaper.utils.</i>
</p>

```python
import json
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

base_url = 'https://www.foxbusiness.com/economy/white-house-calls-for-interim-coronavirus-relief-as-negotiations-continue'
article = Article(base_url, config=config)
article.download()
article.parse()

soup = BeautifulSoup(article.html, 'html.parser')
cnn_dictionary = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

date_published = [value for (key, value) in cnn_dictionary.items() if key == 'datePublished']
print(date_published)
['2020-10-11T12:51:53-04:00']

article_author = [value['name'] for (key, value) in cnn_dictionary.items() if key == 'author']
print(article_author)
['Reuters']

article_title = [value for (key, value) in cnn_dictionary.items() if key == 'headline']
print(article_title)
['White House pushes for limited coronavirus relief bill as broader effort meets resistance']

article_summary = [value for (key, value) in cnn_dictionary.items() if key == 'description']
print(article_summary)
['In the letter to House and Senate members, Mnuchin and Meadows said the White House would continue to talk to Senate Democratic Leader Chuck Schumer 
and House Speaker Nancy Pelosi, but that Congress should "immediately vote on a bill" that would enable the use of unused Paycheck Protection Program 
funds while working toward a bigger package.']
```

### BBC News Extraction 
<p align="justify">
BBC News stores data elements in multiple locations within its source code.  Some of these data elements can be extracted using <i>article.meta_data</i> and others 
can be accessed through the <i>Python</i> modules <i>BeautifulSoup</i> and <i>JSON</i>. As previously started <i>BeautifulSoup</i> is a dependency of <i>Newspaper3k</i> and can be accessed through <i>newspaper.utils.</i>    
</p>

```python
import json
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

base_url = 'https://www.bbc.com/news/health-54500673'
article = Article(base_url, config=config)
article.download()
article.parse()

print(article.title)
['Covid virus ‘survives for 28 days’ in lab conditions']

article_meta_data = article.meta_data

article_summary = {value for (key, value) in article_meta_data.items() if key == 'description'}
print(article_summary)
{'Researchers find SARS-Cov-2 survives for longer than thought - but only under certain conditions.'}

soup = BeautifulSoup(article.html, 'html.parser')
bbc_dictionary = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

date_published = [value for (key, value) in bbc_dictionary.items() if key == 'datePublished']
print(date_published)
['2020-10-11T20:11:33.000Z']

article_author = [value['name'] for (key, value) in bbc_dictionary.items() if key == 'author']
print(article_author)
['BBC News']

# another method to extract the title
article_title = [value for (key, value) in bbc_dictionary.items() if key == 'headline']
print(article_title)
['Covid virus ‘survives for 28 days’ in lab conditions']
```

### Newspaper language support
<p align="justify">
As of October 2020 <i>Newspaper3k</i> supports 37 different languages.      
</p>

``` python
import newspaper
newspaper.languages()

Your available languages are:
input code      full name

  ar              Arabic
  be              Belarusian
  bg              Bulgarian
  da              Danish
  de              German
  el              Greek
  en              English
  es              Spanish
  et              Estonian
  fa              Persian
  fi              Finnish
  fr              French
  he              Hebrew
  hi              Hindi
  hr              Croatian
  hu              Hungarian
  id              Indonesian
  it              Italian
  ja              Japanese
  ko              Korean
  lt              Lithuanian
  mk              Macedonian
  nb              Norwegian (Bokmål)
  nl              Dutch
  no              Norwegian
  pl              Polish
  pt              Portuguese
  ro              Romanian
  ru              Russian
  sl              Slovenian
  sr              Serbian
  sv              Swedish
  sw              Swahili
  th              Thai
  tr              Turkish
  uk              Ukrainian
  vi              Vietnamese
  zh              Chinese
  ```

### China Daily Extraction in Chinese
<p align="justify">
The example below is querying the China Daily news site in the Chinese language. <i>Newspaper3k</i> uses the Chinese Words Segementation Utility <i>jieba</i> when extracting data elements. This <i>Python</i> module was continually building a prefix dict, which displayed build information. Currently the only mechanism to suppress this build information is with this setting <i>jieba.setLogLevel(logging.ERROR)</i>. 
</p>

``` python
from newspaper import Config
from newspaper import Article
import jieba
import logging
jieba.setLogLevel(logging.ERROR)

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
config = Config()

config.headers = HEADERS
config.request_timeout = 10

base_url = 'http://tech.chinadaily.com.cn/a/202009/30/WS5f7414f1a3101e7ce9727a44.html'
article = Article(base_url, config=config, language='zh')
article.download()
article.parse()
article_meta_data = article.meta_data

print(article.title)
中国发布高分多模卫星首批影像成果

print(article.publish_date)
2020-09-30 00:00:00

article_keywords = {value for (key, value) in article_meta_data.items() if key == 'Keywords'}
if article_keywords:
    print(article_keywords)
    {'多模,高分,影像,卫星,成果,发布,中国'}
```

### Die Zeit Extraction in German
<p align="justify">
The example below is querying the Die Zeit news site in the german language. <i>Newspaper3k</i> has some difficulties querying and extracting content from this news site.  To bypass these issues, this example uses the <i>Python requests</i> module to query Die Zeit and passes this content to <i>Newspaper3k</i> and <i>BeautifulSoup</i>.
           
</p>

``` python
import json
import requests
from newspaper import Article
from newspaper.utils import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
           
base_url = 'https://www.zeit.de/politik/ausland/2020-10/us-wahl-donald-trump-gewalt-milizen-protest'
raw_html = requests.get(base_url, headers=HEADERS, timeout=10)
article = Article('', language='de')
article.download(input_html=raw_html.content)
article.parse()

soup = BeautifulSoup(article.html, 'html.parser')
zeit_dictionary = json.loads("".join(soup.findAll("script", {"type": "application/ld+json"})[3].contents))

date_published = [value for (key, value) in zeit_dictionary.items() if key == 'datePublished']
print(date_published)
['2020-10-12T04:53:14+02:00']

article_author = [value['name'] for (key, value) in zeit_dictionary.items() if key == 'author']
print(article_author)
['Rieke Havertz']

article_title = [value for (key, value) in zeit_dictionary.items() if key == 'headline']
print(article_title)
['US-Wahl: Gewalt nicht ausgeschlossen']

article_summary = [value for (key, value) in zeit_dictionary.items() if key == 'description']
print(article_summary)
['Tote bei Protesten zwischen Linken und Rechten, Terrorpläne im eigenen Land: Die Gewaltbereitschaft in den USA ist vor der Wahl hoch. Und der Präsident deeskaliert nicht.']
```
 
