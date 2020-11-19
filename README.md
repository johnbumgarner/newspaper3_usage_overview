# Special caveats
<p align="justify">
The code examples in this repository were designed using <a href="https://github.com/codelucas/newspaper">Newspaper version: 0.2.8</a>. The examples might require modification when there is a version update for <i>Newspaper</i>.
           
The last update to this repository was performed on <b>11-19-2020</b>. All the examples worked based on the website structure of the news sources being queried at that time.  If any news source modifies their website's navigational structure then the code example for that source might not function correctly.

For instance, the Die Zeit news site recently added an advertisement and tracking acknowledgement button, which will likely require the use of the <i>Python</i> library <i>selenium</i> coupled with <i>Newspaper</i> extraction code within this repository to extract article elements on that website. 

It's worth pointing out that <i>Newspaper</i> has some extraction limitations, but most of these can be overcome with either snippets of addtional code or by including another <i>Python</i> library in the mix.  

For example, the web page for <a href="https://foxbaltimore.com">Fox Baltimore</a> cannot currently be parsed using either <i>newspaper.build</i> or <i>newspaper Source</i>. This is because the <i>Fox Baltimore's</i> page is rendered in JavaScript.  To parse this page, one would need to use the <i>Python</i> module <i>BeautifulSoup</i> to extract the content, which can be further processed with <i>newspaper.</i>

I will update this repository as needed based on extraction questions that I find on either <a href="https://stackoverflow.com/questions/tagged/python-newspaper">Stack Overflow</a> or from <a href="https://github.com/codelucas/newspaper/issues">Newspaper's issue tracker</a> on GitHub. 
</p>

# Primary objective of this repository

<p align="justify">
This repository was developed to provide technical insights on how to properly utilized the <i>Python</i> library <a href="https://github.com/codelucas/newspaper">Newspaper3k</a> to query news sources, such as the <a href="https://www.wsj.com">Wall Street Journal</a>, <a href="https://www.bbc.com">the BBC</a> and <a href="https://www.cnn.com">CNN</a>.
</p>

# Newspaper Configuration for Querying 

<p align="justify">
<i>Newspaper3k</i> uses the <i>Python requests</i> module to make a connection request to a news website. <i>Python requests</i> allows connections to have HTTP headers information and <i>Newspaper3k</i> includes this capability within its code base. These <i>Newspaper3k</i> configuration parameters include: sending a browser's user agent string as part of the request, establishing a connection timeout period (in seconds) and using proxies.  
           
Some websites queried with <i>Newspaper3k</i> will send back status response code indicating that there was a problem with the connection.  These status response codes include:

- HTTP 400 Bad Request error 
- HTTP 403 Forbidden client error
- HTTP 406 Not Acceptable client error

One of the primary root causes of these errors is the lack of a browser's user agent string in the request. 

Another potential issue when making requests with <i>Newspaper3k</i> is a <i>ReadTimeout</i> error.  This error is usually linked to not providing a connection timeout period in the request. The <i>Python requests</i> documentation makes a point that setting a connection timeout is considered best practice.
</p>

## Configuration example

```python
from newspaper import Config

config = Config()
config.browser_user_agent = string value
config.proxies = dictionary of proxies
config.request_timeout = int value 
```

## Sample usage example

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

## Real world usage example

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
           
This example was written in response to this <i>Newspaper</i> issue: <a href="https://github.com/codelucas/newspaper/issues/844">"How to use headers when requesting in Article()func?"</a>, which was posted on 09-16-2020.
</p>

## Real world basic header usage example

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

# Newspaper Source Extraction 

<p align="justify">
One of the primary purposes of <i>Newspaper3k</i> is text extraction from a news website. Out-of-box <i>Newspaper3k</i> does a good job of extracting content, but it is not flawless.  Several of these extraction issues are posted as questions to either <a href="https://stackoverflow.com/search?q=newspaper3k">Stack Overflow</a> or to the GitHub repository for <a href="https://github.com/codelucas/newspaper/issues">Newspaper.</a>  Many of the extraction questions are directly related to an end-user not reviewing the news source's HTML code prior to querying the website with <i>Newspaper3k</i>. Any developer that has used <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">BeautifulSoup</a>, <a href="https://scrapy.org/">Scrapy</a> or <a href="https://selenium-python.readthedocs.io/">Selenium</a> to scrape a website knows that you need to review the portal's structure to properly extract content. 
</p>

## BBC News Extraction 

<p align="justify">
BBC News stores their data elements in multiple locations within its source code.  Some of these data elements can be extracted using <i>article.meta_data</i> and others can be accessed through the <i>Python</i> modules <i>BeautifulSoup</i> and <i>JSON</i>. As previously started <i>BeautifulSoup</i> is a dependency of <i>Newspaper3k</i> and can be accessed through <i>newspaper.utils.</i>    
           
This example was written in response to this <i>Newspaper</i> issue: <a href="https://github.com/codelucas/newspaper/issues/826">"Unable to pick up BBC Dates"</a>, which was posted on 07-11-2020.
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

## CNN Extraction 

<p align="justify">
The example below is querying an article on the CNN website using <i>Newspaper3k</i>.  The article data elements; title, authors and date published are adequately  extracted using <i>Newspaper3k</i>.  The keywords for this article were not initial discovered by <i>Newspaper3k</i>, but modifying the parameter <i>article.keywords</i> to <i>meta_keywords</i> does yield the keywords related to this article. 
           
This example was written in response to this <i>Stack Overflow</i> question: <a href="https://stackoverflow.com/questions/63948084/python-see-timestamp-of-article-provided-by-newspaper3k/64002544#64002544">"Python: See timestamp of article provided by newspaper3k?"</a>, which was posted on 09-18-2020.
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

## Fox Business News Extraction 

<p align="justify">
Extracting specific data elements from Fox News requires querying the meta tags section of the HTML code. The data elements that can be extracted include the title of the article, the published date of the article and a summary of the article.  Fox News does not use keywords, so extracting these is not possble.  Extracting the authors of the article is also problematic, because Fox News does not use a standard tag (e.g., by-line) for this information.  
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

## Fox Baltimore News Extraction 
<p align="justify">
Extracting data elements from the website <i>Fox Baltimore</i> with either <i>Newspaper Build</i> or <i>Newspaper Source</i> is currently not possible. <i>Fox Baltimore</i> embeds the bulk of its content in <i>script</i> tags. This data can be extracted using the <i>Python</i> modules <i>BeautifulSoup</i> and <i>JSON</i>. <i>BeautifulSoup</i> is a dependency of <i>Newspaper3k</i> and can be accessed through <i>newspaper.utils</i>.
           
As of 11-18-2020 the example below can extract content like <i>Newspaper Build</i> or <i>Newspaper Source</i> does from the main page of a news source. 

This example was written in response to this <i>Newspaper</i> issue: <a href="https://github.com/codelucas/newspaper/issues/859">"Newspaper not extracting pages for Fox Baltimore"</a>, which was posted on 11-14-2020.
</p>

```python
import json
import requests
import pandas as pd
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def query_foxbaltimore_news():
    df_foxbaltimore_extraction = pd.DataFrame(columns=['article_category', 'date_published', 'article authors',
                                                       'article title', 'article summary', 'article keywords',
                                                       'article url', 'article text'])

    url = 'http://foxbaltimore.com/'
    response = requests.get(url, headers=HEADERS, allow_redirects=True, verify=True, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')
    fox_soup = soup.find_all("script", {"type": "application/json"})[1]
    fox_json = json.loads(''.join(fox_soup))
    for news in fox_json['content']['page-data']['teaser']:
        for article in news['teasers']:
            article_category = article['categories'][0]
            article_title = article['title']
            article_url = f"https://foxbaltimore.com{article['url']}"
            article_summary = article['summary']
            article_published_date = article['publishedDateISO8601']
            if 'sponsored' not in article_url:
                article_details = query_individual_article_elements(article_url)
                df_foxbaltimore_extraction = df_foxbaltimore_extraction.append({'article category':article_category,
                                                                       'date_published': article_published_date,
                                                                       'article authors': article_details[0],
                                                                       'article title': article_title,
                                                                       'article summary': article_summary,
                                                                       'article keywords': article_details[3],
                                                                       'article url': article_url,
                                                                       'article text': article_details[5]}, ignore_index=True)
    return df_foxbaltimore_extraction


def query_individual_article_elements(url):
    config = Config()
    config.headers = HEADERS
    config.request_timeout = 30
    article = Article(url, config=config, memoize_articles=False)
    article.download()
    article.parse()
    article_meta_data = article.meta_data

    article_author = article.authors

    article_published_date = str({value['published_time'] for (key, value) in article_meta_data.items()
                                  if key == 'article'})

    article_keywords = sorted([value.lower() for (key, value) in article_meta_data.items() if key == 'keywords'])

    article_title = str({value for (key, value) in article_meta_data.items() if key == 'title'})

    article_summary = {value for (key, value) in article_meta_data.items() if key == 'description'}

    soup = BeautifulSoup(article.html, 'html.parser')
    fox_soup = soup.find_all("script", {"type": "application/json"})[1]
    fox_json = json.loads(''.join(fox_soup))
    article_text = ''.join(fox_json['content']['main_content']['story']['richText'])
    article_details = [article_author,
                       article_published_date,
                       article_title,
                       article_keywords,
                       article_summary,
                       article_text]

    return article_details
```

## Wall Street Journal Extraction 

<p align="justify">
The example below is querying an article on the Wall Street Journal and extracting several data elements from the page's HTML code. <i>Newspaper3k</i> was able to 
adequately extract the article's title and author of the article, but failed to extract the published date or the keywords related to this article. 
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
The published date and keywords related to this Wall Street Journal article are located in mutiple meta tags and can be extracted by <i>Newspaper3k</i> using 
<i>article.meta_data.</i>  Addtional article data elements, such as authors, title and article summary are also located within the meta tags section used by the Wall Street Journal.
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

## Extraction from offline HTML files

<p align="justify">
<a href="https://github.com/codelucas/newspaper">Newspaper3k</a> can be used to post-process HTML files that have stored offline. The example below downloads the HTML for a news article from <a href="https://www.cnn.com/2020/10/12/health/johnson-coronavirus-vaccine-pause-bn/index.html">CNN</a>.  After the article is downloaded the file is read into <i>Newspaper</i> and the data elements with the article are extracted.
           
This example was written in response to this <i>Stack Overflow</i> question: <a href="https://stackoverflow.com/questions/43281123/how-to-extract-from-stored-html-using-python-newspaper/64163908#64163908">"how to extract from stored HTML using Python Newspaper"</a>, which was posted on 04-17-2017.
</p>

```python
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

base_url = 'https://www.cnn.com/2020/10/12/health/johnson-coronavirus-vaccine-pause-bn/index.html'
article = Article(url, config=config)
article.download()
article.parse()
with open('cnn.html', 'w') as fileout:
    fileout.write(article.html)


# Read the HTML file created above
with open("cnn.html", 'r') as f:
    # note the empty URL string
    article = Article('', language='en')
    article.download(input_html=f.read())
    article.parse()
    
    print(article.title)
    Johnson & Johnson pauses Covid-19 vaccine trial after 'unexplained illness'
    
    article_meta_data = article.meta_data
    
    article_published_date = {value for (key, value) in article_meta_data.items() if key == 'pubdate'}
    print(article_published_date)
    {'2020-10-13T01:31:25Z'}

    article_author = {value for (key, value) in article_meta_data.items() if key == 'author'}
    print(article_author)
    {'Maggie Fox, CNN'}

    article_summary = {value for (key, value) in article_meta_data.items() if key == 'description'}
    print(article_summary)
    {'Johnson&Johnson said its Janssen arm had paused its coronavirus vaccine trial  after an "unexplained illness" in one 
    of the volunteers testing its experimental Covid-19 shot.'}

    article_keywords = {value for (key, value) in article_meta_data.items() if key == 'keywords'}
    print(article_keywords)
    {"health, Johnson & Johnson pauses Covid-19 vaccine trial after 'unexplained illness' - CNN"}
```

# Newspaper language support
<p align="justify">
<i>Newspaper3k</i> currently supports 37 different languages, as of October 2020.  
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

## China Daily Extraction in Chinese

<p align="justify">
The example below is querying the China Daily news site in the Chinese language. <i>Newspaper3k</i> uses the Chinese Words Segementation Utility <i>jieba</i> when extracting data elements. This <i>Python</i> module was continually building a prefix dict, which displayed build information. Currently the only mechanism to suppress this build information is with this setting <i>jieba.setLogLevel(logging.ERROR)</i>. 
</p>

``` python
from newspaper import Config
from newspaper import Article
import jieba
import logging
jieba.setLogLevel(logging.ERROR)

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
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

## Die Zeit Extraction in German

<p align="justify">
The example below is querying the Die Zeit news site in the German language. <i>Newspaper3k</i> has some difficulties querying and extracting content from this news site.  To bypass these issues, this example uses the <i>Python requests</i> module to query Die Zeit and passes the HTML to <i>Newspaper3k</i> and <i>BeautifulSoup</i> for processing.   
 
This example was written in response to this <i>Newspaper</i> issue: <a href="https://github.com/codelucas/newspaper/issues/841">"Add support for zeit.de"</a>, which was posted on 09-08-2020.
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

# Saving Extracted Data

## CSV files 
<p align="justify">
Writing data to a comma-separated values (CSV) file is a very common practice in <i>Python</i>. The example below extracts content from a <a href="https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1">Wall Street Journal</a> article.  The items extracted include; the publish date for the article, the authors of this article, the title and summary for this article and the associated keywords assigned to this article.  All these data elements are written to an external CSV file. All the data elements were normalized into string variables, which made for easier storage in the CSV file. 
</p>

```python
import csv
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

published_date = {value for (key, value) in article_meta_data.items() if key == 'article.published'}
article_published_date = " ".join(str(x) for x in published_date)

authors = sorted({value for (key, value) in article_meta_data.items()if key == 'author'})
article_author = ', '.join(authors)

title = {value for (key, value) in article_meta_data.items() if key == 'article.headline'}
article_title = " ".join(str(x) for x in title)

summary = {value for (key, value) in article_meta_data.items() if key == 'article.summary'}
article_summary = " ".join(str(x) for x in summary)

keywords = ''.join({value for (key, value) in article_meta_data.items() if key == 'news_keywords'})
keywords_list = sorted(keywords.lower().split(','))
article_keywords = ', '.join(keywords_list)

with open('wsj_extraction_results.csv', 'a', newline='') as csvfile:
    headers = ['date published', 'article authors', 'article title', 'article summary', 'article keywords']
    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
    writer.writeheader()

    writer.writerow({'date published': article_published_date,
                     'article authors': article_author,
                     'article title': article_title,
                     'article summary': article_summary,
                     'article keywords': article_keywords})
```



## JSON files 
<p align="justify">
Writing data to a JSON file is also very common practice in <i>Python</i>. The example below extracts content from a <a href="https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1">Wall Street Journal</a> article.  The items extracted include; the publish date for the article, the authors of this article, the title and summary for this article, the associated keywords assigned to this article and the URL of the article.  All these data elements are written to an external JSON file. All the data elements were normalized into string variables, which made for easier storage in the JSON file. 
</p>

```python
import json
from newspaper import Config
from newspaper import Article

news_extraction_results = {}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

base_url = 'https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1'
article = Article(base_url, config=config)
article.download()
article.parse()
article_meta_data = article.meta_data

published_date = {value for (key, value) in article_meta_data.items() if key == 'article.published'}
article_published_date = " ".join(str(x) for x in published_date)

authors = sorted({value for (key, value) in article_meta_data.items()if key == 'author'})
article_author = ', '.join(authors)

title = {value for (key, value) in article_meta_data.items() if key == 'article.headline'}
article_title = " ".join(str(x) for x in title)

summary = {value for (key, value) in article_meta_data.items() if key == 'article.summary'}
article_summary = " ".join(str(x) for x in summary)

keywords = ''.join({value for (key, value) in article_meta_data.items() if key == 'news_keywords'})
keywords_list = sorted(keywords.lower().split(','))
article_keywords = ', '.join(keywords_list)

news_extraction_results['wsj'] = []
news_extraction_results['wsj'].append({
    'published_date': article_published_date,
    'authors': article_author,
    'summary': article_summary,
    'keywords': article_keywords,
    'source url': article.url})


# write JSON file
with open('wsj.json', 'w') as json_file:
    json.dump(news_extraction_results, json_file)
    
# read JSON file
with open('wsj.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data, indent=4))
    {
      "wsj": [
       {
         "published_date": "2020-10-11T09:30:00.000Z",
         "authors": "Karen Langley",
         "summary": "Investors are entering third-quarter earnings season with brighter expectations for corporate profits, a bet they hope 
         will propel the next leg of the stock market\u2019s rally.",
         "keywords": "c&e exclusion filter, c&e industry news filter, codes_reviewed, commodity/financial market news, 
         content types, corporate/industrial news, earnings, equity markets, factiva filters, financial performance",
         "source url": "https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1"
       }
     ]
   }

```

## Python Pandas 
<p align="justify">
<a href="https://pandas.pydata.org/">Pandas</a> is a powerful <i>Python module</i> that uses a DataFrame object for data manipulation with integrated indexing. This module allows for the efficient reading and writing of data between in-memory data structures and different formats, including CSV, text files, Microsoft Excel and SQL databases.
           
The example below extracts content from a <a href="https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1">Wall Street Journal</a> article.  The items extracted include; the publish date for the article, the authors of this article, the title and summary for this article and the associated keywords assigned to this article.  All these data elements are written to an in-memory data structure. It's worth noting that all these data elements were normalized into string variables, which made for easier storage in the <i>pandas DataFrame</i>.
</p>

```python
import pandas as pd
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

published_date = {value for (key, value) in article_meta_data.items() if key == 'article.published'}
article_published_date = " ".join(str(x) for x in published_date)

authors = sorted({value for (key, value) in article_meta_data.items()if key == 'author'})
article_author = ', '.join(authors)

title = {value for (key, value) in article_meta_data.items() if key == 'article.headline'}
article_title = " ".join(str(x) for x in title)

summary = {value for (key, value) in article_meta_data.items() if key == 'article.summary'}
article_summary = " ".join(str(x) for x in summary)

keywords = ''.join({value for (key, value) in article_meta_data.items() if key == 'news_keywords'})
keywords_list = sorted(keywords.lower().split(','))
article_keywords = ', '.join(keywords_list)

# pandas DataFrame used to store the extraction results
df_wsj_extraction = pd.DataFrame(columns=['date_published', 'article authors', 'article title',
                                          'article summary', 'article keywords'])

df_wsj_extraction = df_wsj_extraction.append({'date_published': article_published_date,
                                              'article authors': article_author,
                                              'article title': article_title,
                                              'article summary': article_summary,
                                              'article keywords': article_keywords}, ignore_index=True)

print(df_wsj_extraction.to_string(index=False))

```

# Newspaper NewsPool Threading 

<p align="justify">
<a href="https://github.com/codelucas/newspaper">Newspaper3k</a> has a threading model named <i>news_pool</i>. This function can be used to extract data elements from mutiple sources.  The example below is querying articles on <a href="https://www.cnn.com">CNN</a> and the <a href="https://www.wsj.com">Wall Street Journal</a>.  
           
Some caveats about using <i>news_pool</i>:

1. Time intensive process - it can take minutes to build the sources, before data elements can be extracted.

2. Additional Erroneous content - <i>newspaper.build</i> is designed to extract all the URLs on a news source, so some of the items parsed needed to be filtered.

3. Redundant content - duplicate content is possible without adding additional data filtering.

4. Different data structures - querying mutiple sources could present problems, especially if the news sources use different data structures, such as summaries being in meta-tags on one site and in script tag on the other site. 

This example was written in response to this <i>Newspaper</i> issue: <a href="https://github.com/codelucas/newspaper/issues/838">"Multithread extraction seems to fail at the news_pool.join section"</a>, which was posted on 08-28-2020.
</p>

```python
import newspaper
from newspaper import Config
from newspaper import news_pool

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

wsj_news = newspaper.build('https://www.wsj.com/', config=config, memoize_articles=False, language='en')
cnn_news = newspaper.build('https://www.cnn.com/', config=config, memoize_articles=False, language='en')
news_sources = [wsj_news, cnn_news]

# the parameters number_threads and thread_timeout_seconds are adjustable
news_pool.config.number_threads = 4
news_pool.config.thread_timeout_seconds = 1
news_pool.set(news_sources)
news_pool.join()

article_urls = set()
for source in news_sources:
    for article_extract in source.articles:
        if article_extract.url not in article_urls:
            article_urls.add(article_extract.url)
            print(article_extract.title)
```

<p align="justify">
Threading is also possible in <a href="https://github.com/codelucas/newspaper">Newspaper3k</a> by calling various parameters when using the Source architecture to query a news source. This method is less time intensive than the <i>news_pool</i> threading model.   
<p>

```python
from newspaper import Config
from newspaper import Source

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

wsj_news = Source(url='https://www.wsj.com/', config=config, memoize_articles=False, language='en',
                  number_threads=20, thread_timeout_seconds=2)

cnn_news = Source(url='https://www.cnn.com', config=config, memoize_articles=False, language='en',
                  number_threads=20, thread_timeout_seconds=2)

news_sites = [cnn_news, wsj_news]
for site in news_sites:
    site.build()
    for article_extract in site.articles:
        article_extract.download()
        article_extract.parse()
        print(article_extract.title)
```

#  Text Extraction and Natural Language Processing
<p align="justify">
<a href="https://github.com/codelucas/newspaper">Newspaper3k</a> can extract the text of articles, but the embedded extraction methodology used by Newspaper has numerous problems. For instance every news source has its own unique coding structure and article tag hierarchy, thus Newspaper has difficulty navigating and parsing some sites. In some circumstances Newspaper will either overlook entire sections of an article or unknowingly extract text that does not belong to the article being parsed. Newspaper will also occasionally extract some image tag text for photos linked to associated with an article. I would highly recommended reviewing the textual information extracted by Newspaper prior to performing any Natural Language Processing(NLP) tasks.
           
Concerning <a href="https://github.com/codelucas/newspaper">Newspaper3k</a> Natural Language Processing capabilities.  The embedded NLP capabilities in my opinion should not be used until the module's owner greatly improves them.

This repository contains a <a href="https://github.com/johnbumgarner/newspaper3_usage_overview/blob/main/utilities/nlp_utilities.py">script</a> that can be used to perform various Natural Language Processing tasks on extracted textual information. Feel free to make suggestions to improve this script. 
<p>

## Basic Text Extraction 

```python
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

url = 'https://www.newsweek.com/facebook-super-spreader-election-misinformation-1543306'
article = Article(url, config=config)
article.download()
article.parse()
# the replace is used to remove newlines
article_text = article.text.replace('\n', '')
print(article_text)
Less than a week ahead of the U.S. presidential election, misinformation relating to voting and 
election security is flourishing on Facebook, despite the platform's pledge to curb such content, 
a NewsGuard investigation has found. NewsGuard has identified 40 Facebook pages that are 
"super-spreaders" of election-related misinformation, meaning that they have shared false content 
about voting or the electoral process to their audiences of at least 100,000 followers. Only three 
of the 53 posts we identified on these pages—which together reach approximately 22.9 million 
followers—were flagged by Facebook as false. Four of the pages have managers based outside the 
U.S.—in Mexico,Vietnam, Australia, and Israel—despite the pages' focus on American politics. 
The myths identified by NewsGuard include false claims of mail-in ballots getting thrown away, 
narratives that dead people's cast ballots count as votes, and false claims about poll watchers. 
The claims about poll watchers cut both ways, with players on both the right and the left pushing 
their own, self-serving myths, NewsGuard found.NewsGuard's analysis also found that election-related 
myths often seize on routine and solvable voting errors as examples of malpractice or deception, 
sowing distrust in the electoral process. Others seem based on either an unintentional or willful 
misunderstanding of rules and practices.The false stories NewsGuard identified sometimes included 
multiple election myths, while other articles did not fit neatly with one particular election myth. 
Nevertheless, all the articles NewsGuard identified advanced inaccurate information about the voting 
process. For example, one popular Facebook post recently claimed that Pennsylvania had rejected 
372,000 ballots, when in fact, Pennsylvania officials had actually rejected 372,000 ballot applications. 
The rejection of absentee ballot applications is not uncommon, nor is it necessarily evidence of anything 
untoward. Moreover, a registered voter whose application to vote by mail was rejected can still vote in 
person. This falsehood appeared in an article published on 100Percent FedUp.com, a NewsGuard Red-rated 
(or generally unreliable) site. Patty McMurray, the co-owner of the site and the author of the article, 
told NewsGuard that her site had corrected the article to reflect the distinction between ballots and 
ballot applications. However, the false, uncorrected post remains accessible on Facebook and appears on 
at least five large Facebook pages. This claim was one of dozens that Facebook did not flag as false. 
When a Utah county accidentally sent out 13,000 absentee ballots without a signature line, the NewsGuard 
Red-rated site LawEnforcementToday.com called this a "cheat-by-mail scheme." The Salt Lake Tribune reported 
that the Sanpete County Clerk quickly learned of the mistake, which was a printing error, and immediately 
put information online explaining to voters how to correctly submit their ballot. There was no evidence 
that the mistake was part of a voter fraud scheme. But on October 15, the post was shared to three connected 
Facebook pages, with a total reach of 1.1 million followers. None of the posts were marked as false by 
Facebook's fact-checkers.Conspiratorial stories abounded, with articles warning of violence or other disastrous 
and unlawful election outcomes with no evidence to support their claims. Greg Palast, a liberal investigative 
journalist, predicted that 6 million people will vote by mail in Florida, but claimed their votes will likely 
not be counted. "The GOP-controlled Florida Legislature will say, we can't count them in time, so we're not 
going to certify the election," Palast wrote, suggesting this move would be part of a ploy to send the decision 
to the U.S. House, which under the 12th Amendment decides the president if no majority is reached in the electoral 
college.There is no evidence to suggest that the Florida legislature will refuse to certify the state's results. 
This article, shared on Facebook to Palast's 109,000 followers, was not flagged as false by Facebook. The three 
Facebook posts that were flagged by fact-checkers did not include such warnings until after the myth had been 
published and shared, due to the platform's practice of not providing advance warnings to users about pages that 
have been known to publish misinformation or hoaxes in the past. Had such warnings existed, Facebook users would 
have known in advance that they might be exposed to misinformation when reading those pages' posts.Despite Facebook's 
announced efforts to stop the spread of this type of misinformation, these pages continue to be allowed to publish 
blatant misinformation about voting and the electoral process — seemingly in violation of the platform's content 
policies. New false stories emerge daily, with inaccurate and deceptive interpretations of events that are perfectly 
normal. The result is that Facebook has exposed tens of millions of Americans to falsehoods about America's 
electoral process.
```

## Basic Text Extraction with NLP
```python
from newspaper import Config
from newspaper import Article
from utilities.nlp_utilities import NLPCustomMethods

nlp = NLPCustomMethods()

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

url = 'https://www.newsweek.com/facebook-super-spreader-election-misinformation-1543306'
article = Article(url, config=config)
article.download()
article.parse()
# the replace is used to remove newlines
article_text = article.text.replace('\n', '')

remove_stopwords = nlp.expunge_stopwords(article_text)
normalize_text = nlp.expunge_punctuations(remove_stopwords)

most_common_words = nlp.get_most_common_words(normalize_text, 20)
print(most_common_words)
[('facebook', 15), ('false', 9), ('newsguard', 8), ('pages', 8), ('election', 6), ('misinformation', 6), 
('voting', 5), ('identified', 5), ('electoral', 5), ('ballots', 5), ('shared', 4), ('process', 4), 
('myths', 4), ('claims', 4), ('ballot', 4), ('evidence', 4), ('article', 4), ('site', 4), ('platform', 3), 
('content', 3)]

# this output was sorted() and put into a set()
# noun types can also be tweak under NLPCustomMethods().get_nouns
nouns = nlp.get_nouns(normalize_text)
print(nouns)
['absentee', 'advance', 'amendment', 'americans', 'analysis', 'anything', 'application', 'applications', 
'article', 'articles', 'audiences', 'author', 'ballot', 'ballots', 'certify', 'cheatbymail', 'claims', 
'clerk', 'content', 'coowner', 'count', 'county', 'curb', 'deception', 'decides', 'decision', 'distinction', 
'dozens', 'efforts', 'election', 'error', 'errors', 'events', 'evidence', 'example', 'facebook', 'fact', 
'factcheckers', 'falsehood', 'falsehoods', 'falsewhen', 'flag', 'florida', 'followers', 'fraud', 'hoaxes', 
'house', 'information', 'interpretations', 'investigation', 'journalist', 'lawenforcementtodaycom', 'legislature', 
'line', 'mail', 'majority', 'malpractice', 'managers', 'mcmurray', 'meaning', 'mexicovietnam', 'millions', 
'misinformation', 'misunderstanding', 'move', 'myth', 'myths', 'narratives', 'officials', 'online', 'others', 
'pages', 'palast', 'part', 'pennsylvania', 'people', 'person', 'platform', 'players', 'pledge', 'policies', 
'politicsthe', 'poll', 'post', 'posts', 'practice', 'president', 'printing', 'process', 'processfor', 'reading', 
'reflect', 'refuse', 'result', 'results', 'rules', 'scheme', 'security', 'send', 'signature', 'site', 'spread', 
'state', 'stories', 'superspreaders', 'support', 'tens', 'time', 'tribune', 'users', 'violation', 'violence', 
'vote', 'voter', 'voters', 'votes', 'voting', 'warnings', 'watchers', 'ways', 'week']


# this output was sorted() and put into a set()
# verb types can also be tweak under NLPCustomMethods().get_verbs
verbs = nlp.get_verbs(normalize_text)
print(verbs)
['abounded', 'allowed', 'announced', 'appeared', 'appears', 'articles', 'australia', 'based', 'called', 
'cast', 'claim', 'claimed', 'connected', 'continue', 'corrected', 'counted', 'cut', 'electionrelated', 
'emerge', 'examples', 'existed', 'explaining', 'exposed', 'fit', 'flagged', 'flourishing', 'focus', 'found', 
'foundnewsguard', 'getting', 'going', 'greg', 'identified', 'include', 'known', 'learned', 'least', 'left', 
'mailin', 'marked', 'mistake', 'october', 'outcomes', 'ploy', 'poll', 'postsdespite', 'practicesthe', 'predicted', 
'providing', 'published', 'pushing', 'put', 'reach', 'reached', 'redrated', 'rejected', 'rejection', 'relating', 
'remains', 'reported', 'salt', 'say', 'seem', 'seize', 'selfserving', 'sent', 'shared', 'sowing', 'stop', 
'submit', 'suggesting', 'thrown', 'told', 'vote', 'voting', 'warning', 'wrote']

word_frequency = nlp.get_frequency_distribution(normalize_text, 20)
print(word_frequency)
[('facebook', 15), ('false', 9), ('newsguard', 8), ('pages', 8), ('election', 6), ('misinformation', 6), 
('voting', 5), ('identified', 5), ('electoral', 5), ('ballots', 5), ('shared', 4), ('process', 4), 
('myths', 4), ('claims', 4), ('ballot', 4), ('evidence', 4), ('article', 4), ('site', 4), ('platform', 3), 
('content', 3)]
```
