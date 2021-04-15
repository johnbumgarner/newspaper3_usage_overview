# Special caveats
<p align="justify">
The code examples in this repository were designed using <a href="https://github.com/codelucas/newspaper">Newspaper version: 0.2.8</a>. The examples might require modification when there is a version update for <i>Newspaper</i>.
           
The last update to this repository was performed on <b>04-15-2021</b>. All the examples worked based on the website structure of the news sources being queried at that time.  If any news source modifies their website's navigational structure then the code example for that source might not function correctly.

For instance, the Die Zeit news site added an advertisement and tracking acknowledgement button, which now requires the use of the <i>Python</i> library <i>selenium</i> coupled with <i>Newspaper</i> extraction code to extract article elements from this news source. 

It's worth pointing out that <i>Newspaper</i> has some extraction limitations, but most of these can be overcome with either snippets of additional code or by including another <i>Python</i> library in the mix.  

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

## Extraction from Wayback Machine archives
<p align="justify">
An unanswered <a href="https://stackoverflow.com/questions/41680013/python-newspaper-with-web-archive-wayback-machine/65476836#65476836">Stack Overflow question</a> from 2017 prompted me to explore how to extract article content from the Wayback Machine archives. 
           
That question was attempting to use <i>newspaper.build</i> to extract the archived articles.  I could not get <i>newspaper.build</i> to work correctly, but I was able to use <i>newspaper Source</i> to query and extract articles from the archives.
           
</p>
           
```python
from time import sleep
from random import randint
from newspaper import Config
from newspaper import Source

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

cnbc_wayback_archive = Source(url='https://web.archive.org/web/20180301012621/https://www.cnbc.com/', config=config,
                      memoize_articles=False, language='en', number_threads=20, thread_timeout_seconds=2)

cnbc_wayback_archive.build()
for article in cnbc_wayback_archive.articles:
    article.download()
    article.parse()
    article_meta_data = article.meta_data

    print(article.publish_date)
    print(article.title)

    article_description = "".join({value for (key, value) in article_meta_data.items() if key == 'description'})
    print(article_description)

    article_keywords = {value for (key, value) in article_meta_data.items() if key == 'keywords'}
    print(list(article_keywords))

    print(article.url)

    # this sleep timer is helping with some timeout issues
    # that happened when querying
    sleep(randint(1, 5))
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

## Common Newspaper Extraction Questions

<p align="justify">
<i>Newspaper3k</i> has some limitations surrounding basic content extraction.  These limitations are normally related to either the hardcoded <i>HTML tags</i> within the extraction source code for <i>Newspaper3k</i> or because a user does not fully understand the capabilities of <i>Newspaper3k</i> when extracting from a specific source.</p>

<b>Question One: <i>Author Name Missing</i></b>

<p align="justify">
From example this <i>Stack Overflow</i> question <a href="https://stackoverflow.com/questions/66122449/newsletter3k-am-i-did-something-wrong-author-function-did-not-pick-up-author-i/66139240">"article.authors not getting author's name"</a> is primarily related to the structure of a news source.

<i>Newspaper3k</i> uses the <i>Python</i> package <i>Beautiful Soup</i> to extract items, such as author names from a news website. The tags that Newspaper3k queries are pre-defined within <i>Newspaper3k</i> source code. <i>Newspaper3k</i> makes a best effort to extract content from these pre-defined tags on a news site.

BUT not all news sources are structured the same, so <i>Newspaper3k</i> will miss certain content, because a tag (e.g., author's name) will be a different place in the HTML structure.

For instance <i>Newspaper3k version: 0.2.8</i> looks for the author name in these tags:

VALS = ['author', 'byline', 'dc.creator', 'byl']

The tags <i>author</i>, <i>byline</i> and <i>byl</i> are normally located in the main body of a webpage. The tag <i>dc.creator</i> is always located in the META tag section of a news source. If your news source has a different author tag in the META section, such as <i>article.author</i>, which the <i>Los Angeles Times</i> uses then you must query that tag like this:

```python
article_meta_data = article.meta_data
article_author = {value for (key, value) in article_meta_data['article'].items() if key == 'author'}
```

The <i>Los Angeles Times</i> also has the author name in the JSON-LD (JavaScript Object Notation for Linked Data) section of the webpage's source code. To extract content from this JSON section you would query the information this way:

```python
from newspaper.utils import BeautifulSoup

article = Article(website, config=config)
article.download()
article.parse()

soup = BeautifulSoup(article.html, 'html.parser')
la_times_dictionary = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
article_author = ''.join([value[0]['name'] for (key, value) in la_times_dictionary.items() if key == 'author'])
```
</p>



# Newspaper Article caching
<p align="justify">
<i>Newspaper3k</i> is designed to caches all previously extracted articles from a specific source.  The primary reason for caching these articles is prevent duplicate querying for a given article. <i>Newspaper3k</i> has a parameter named <i>memoize_articles</i>, which is enabled to <i>"True"</i> by default. 
           
For instance both of these queries have the parameter <i>memoize_articles=True</i> automatically set by <i>Newspaper3k</i>.

``` python
cnn_articles = newspaper.build('https://www.cnn.com/', config=config)

article = Article('https://www.cnn.com/2020/12/05/health/us-hospitals-covid-pandemic/index.html', config=config)
 ```

With this parameter set to <i>"True"</i> newspaper will write information related to these queries to a temporary directory named <i>.newspaper_scraper</i>. This directory will have a minimum of two sub-directories, which are: <i>feed_category_cache</i> and <i>memoized</i>. The URLs for news sources will be written to a text file (e.g., www.cnn.com.txt) in the sub-directory <i>memoized</i>.  The source code for <i>Newspaper3k</i> indicates that this cache will be maintained for 5 days. The cache is automatically updated with each query of given source (e.g. cnn.com).

I noted that even if you set the parameter <i>memoize_articles</i> to <i>"False"</i> these sub-directories are still created and one file is written to sub-directory <i>feed_category_cache</i> when using <i>newspaper.build</i>. So far, I have not found a method to prevent <i>Newspaper3k</i> from creating these sub-directories or redirecting them to a RAMDISK in memory.

``` python
cnn_articles = newspaper.build('https://www.cnn.com/', config=config,  memoize_articles=False)

article = Article('https://www.cnn.com/2020/12/05/health/us-hospitals-covid-pandemic/index.html', config=config, memoize_articles=False)
 ```

Accessing this temporary directory in macOS can be accomplished in the following matter via the terminal. 

``` echo $TMPDIR
cd <path from $TMPDIR>
cd .newspaper_scraper/
cd memoized
ls 
www.cnn.com.txt
cat www.cnn.com.txt 
https://www.cnn.com/business/media
https://www.cnn.com/travel/news
https://www.cnn.com/2020/12/04/entertainment/mariah-carey-christmas-special/index.html
https://www.cnn.com/2020/12/04/entertainment/your-honor-review/index.html
https://www.cnn.com/2020/12/04/entertainment/star-wars-animation-column/index.html
https://www.cnn.com/2020/12/05/entertainment/lgbtq-holiday-movies-trnd/index.html
https://www.cnn.com/2020/12/04/entertainment/saturday-night-live-jason-bateman/index.html
https://www.cnn.com/2020/12/03/entertainment/blackpink-concert-trnd/index.html
```
</p>

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

## Al Arabiya Extraction in Arabic

<p align="justify">
The example below is querying the Al Arabiya news site in the Arabic language. This example was written in response to this <i>Newspaper</i> issue: <a href="https://github.com/codelucas/newspaper/issues/869">"Does not fetch arabic news,"</a> which was posted on 01-16-2021.  The OP (original poster) could not get <i>Newspaper</i> to extract news content from the <a href="https://www.alarabiya.net">Al Arabiya website.</a> The primary reason for <i>Newspaper</i> not being to extract content was because of a cookie acknowledgement button and subscribe button.  Both these buttons require an end-user to click them before browsing the website either manually or with automated techniques.  To bypass these button an end-user using automated techniques would need to use additional <i>Python</i> modules, such as <a href="https://scrapy.org/">Scrapy</a> or <a href="https://www.selenium.dev/">Selenium.</a>.  

The code example below is using <i>Selenium</i>, <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">BeautifulSoup</a> and <i>Newspaper</i>. During testing I noted that the subscribe button has random visibility on the page.  I attempted to deal with this in my code, but I'm sure that section can be improved upon.  It's also worth noting that I could not get <i>Selenium</i> to pass the <i>browser.page_source</i> to either <i>Newspaper Source</i> or <i>newspaper.build</i>.  Because of this I passed <i>browser.page_source</i> to <i>BeautifulSoup.</i> 

As of 01-21-2021 the code example below worked.  I did not fully validate the articles content being extraction, because I do not speak Arabic.  Additionally  individual article element can be extracted from either the META tags or Javascript section of each specific article page.  That code can be easily added with examples provided in this overview document. 

</p>

``` python
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup

from newspaper import Article
from newspaper import Config

# config details for newspaper
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10


def get_chrome_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--headless')

    # window size as an argument is required in headless mode
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    return driver


def get_chrome_browser(url):
    browser = get_chrome_webdriver()
    browser.get(url)
    return browser


def chrome_browser_teardown(browser):
    browser.close()
    browser.quit()
    return


def bypass_popup_warnings(browser):
    try:
        hidden_element = WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, "wzrk-cancel")))
        if hidden_element.is_displayed():
            browser.implicitly_wait(20)
            subscribe_button = browser.find_element_by_xpath("//*[@id='wzrk-cancel']")
            ActionChains(browser).move_to_element(subscribe_button).click(subscribe_button).perform()
            browser.implicitly_wait(20)
            cookie_button = browser.find_element_by_xpath("//span[@onclick='createCookie()']")
            ActionChains(browser).move_to_element(cookie_button).click(cookie_button).perform()
            return True
        else:
            browser.implicitly_wait(20)
            cookie_button = browser.find_element_by_xpath("//span[@onclick='createCookie()']")
            ActionChains(browser).move_to_element(cookie_button).click(cookie_button).perform()
            return True

    except NoSuchElementException:
        print('Webdriver is unable to identify the requested element during runtime.')
        sys.exit(1)

    except WebDriverException:
        print('The Element Click command could not be completed because the element receiving the events is obscuring the element that was requested clicked.')
        sys.exit(1)


def query_al_arabiya_news(browser):
    news_urls = []
    soup = BeautifulSoup(browser.page_source, 'lxml')
    for a in soup.find_all('a', href=True):
        if str(a['href']).startswith('/ar/'):
            news_urls.append(f"https://www.alarabiya.net/{a['href']}")
    for url in news_urls:
        article = Article(url, config=config, language='ar')
        article.download()
        article.parse()
        
        # additional code required to extract article elements
        # please review the page source to determine the techniques 
        # needed
        print(article.title)
        
    return True


news_browser = get_chrome_browser('https://www.alarabiya.net')
warnings_closed = bypass_popup_warnings(news_browser)
if warnings_closed is True:
    finished = query_al_arabiya_news(news_browser)
    if finished is True:
        chrome_browser_teardown(news_browser)

```

##  News sites with a GDPR acknowledgement button

<p align="justify">

This example is a continuation of the Die Zeit Extraction in German example, which was written in response to this <i>Newspaper</i> issue: <a href="https://github.com/codelucas/newspaper/issues/841">"Add support for zeit.de"</a>, which was posted on 09-08-2020.  A new comment posted on 04-15-2-21 indicated that GDPR acknowledgement warnings were preventing <i>Newspaper</i> from being able to extract from some German language news sites.  

The code example below is using <i>Selenium</i>, <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">BeautifulSoup</a> and <i>Newspaper</i>.  Once the GDPR acknowledgement button has been clicked the primary URL is passed as <i>browser.page_source</i> to <i>BeautifulSoup</i> to harvest every article's href attribute for addtional processing with <i>Newspaper</i>.

As of 04-15-2021 the code example below worked for the following German language news sites that have their GPDR warnings in an <i>iframe</i> with the title <i>Notice Message App</i>:

- https://www.welt.de
- https://www.bild.de
- https://www.stern.de
- https://www.faz.net/aktuell
- https://www.sueddeutsche.de
- https://www.tagesspiegel.de
- https://www.handelsblatt.com
- https://www.berliner-zeitung.de

Sites that do not use an <i>iframe</i> are not supported the code below.

Please note that I did not fully extract the article content from any of these news sites listed above, because I do not speak German and the structures vary. 
This extraction code can be easily added with examples provided in this overview document. 
</p>

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

from newspaper import Article
from newspaper import Config

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10


def get_chrome_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--headless')

    # window size as an argument is required in headless mode
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    return driver


def get_chrome_browser(url):
    browser = get_chrome_webdriver()
    browser.get(url)
    return browser


def chrome_browser_teardown(browser):
    browser.close()
    browser.quit()
    return


def bypass_gdpr_acknowledgement(browser):
    if browser.find_elements_by_tag_name('iframe'):
        iframes = browser.find_elements_by_tag_name('iframe')
        number_of_iframes = len(iframes)
        for i in range(number_of_iframes):
            browser.switch_to.frame(i)
            if browser.find_elements_by_tag_name("title"):
                title_element = browser.find_element_by_tag_name("title").get_attribute("innerHTML")
                if title_element == "Notice Message App":
                    warning_labels = ['Akzeptieren', 'Alle akzeptieren', 'ZUSTIMMEN']
                    for label in warning_labels:
                        try:
                            browser.find_element_by_xpath(f'//button[text()="{label}"]').click()
                            browser.switch_to.default_content()
                            browser.implicitly_wait(10)
                            return True
                        except NoSuchElementException:
                            pass
                else:
                    browser.switch_to.default_content()
            else:
                browser.switch_to.default_content()
    else:
        return False


def query_german_news_site(browser):
    """
    This function needs to be configured to harvest from the site that 
    is being queried. Please reference the Al Arabiya Extraction in Arabic example
    for guidance. 
    """
    soup = BeautifulSoup(browser.page_source, 'lxml')
    for a in soup.find_all('a', href=True):
        print(a['href'])
    return True


news_browser = get_chrome_browser('https://www.handelsblatt.com/')
gdpr_status = bypass_gdpr_acknowledgement(news_browser)
if gdpr_status is True:
    finished = query_german_news_site(news_browser)
    if finished is True:
        chrome_browser_teardown(news_browser)
```


# Saving Extracted Data

## CSV files 
<p align="justify">
Writing data to a comma-separated values (CSV) file is a very common practice in <i>Python</i>. The example below extracts content from a <a href="https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1">Wall Street Journal</a> article.  The items being extracted include; the publish date for the article, the authors of this article, the title and summary for this article and the associated keywords assigned to this article.  All these data elements are written to an external CSV file. All the data elements were normalized into string variables, which made for easier storage in the CSV file. 
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


## HTML files 
<p align="justify">
Writing data to a Hypertext Markup Language (HTML) file is a very common practice in <i>Python</i>. The example below extracts content from multiple <a href="https://www.latimes.com/">Los Angeles Times</a> articles.  The items being extracted include; the publish date for the article, the authors of this article, the title, summary and text of this article and the top image for the article. All these data elements are written to an external HTML file. All the data elements were normalized into string variables, which made for easier storage in the HTML file. 
</p>

``` python
import json
import pandas as pd
from datetime import datetime
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10


def path_to_image_html(link):
    """
    Converts image links to HTML tags
    :param link: image URL
    :return: URL wrapped in clickable HTML tag
    """
    return f'<a href="{link}"> <img src="{link}" width="60" > </a>'


def harvest_article_content(website):
    """
    Queries and extracts specific content from a LA Times article.
    :param website: URL for a LA Times article
    :return: pandas dataframe
    """
    df_latimes_extraction = pd.DataFrame(columns=['Date Published', 'URL', 'Author', 'Title',
                                                  'Summary', 'Text', 'Main Image'])

    article = Article(website, config=config)
    article.download()
    article.parse()

    soup = BeautifulSoup(article.html, 'html.parser')
    la_times_dictionary = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))

    date_published = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'datePublished'])
    clean_date = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%Y-%m-%d')

    article_author = ''.join([value[0]['name'] for (key, value) in la_times_dictionary.items() if key == 'author'])
    article_title = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'headline'])
    article_url = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'url'])
    article_description = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'description'])
    article_body = ''.join([value.replace('\n', ' ') for (key, value) in la_times_dictionary.items() if key ==
                            'articleBody'])

    local_df = save_article_data(df_latimes_extraction, clean_date,
                                 f'<a href="{article_url}">{article_url}</a>',
                                 article_author,
                                 article_title,
                                 article_description,
                                 article_body,
                                 article.top_image)
    return local_df


def save_article_data(df, published_date, website, authors, title, summary, text, main_image):
    """
    Writes extracted article content to a pandas dataframe.

    :param df: pandas dataframe
    :param published_date: article's published date
    :param website: article's URL
    :param authors: article's author
    :param title: article's title
    :param summary: article's summary
    :param text: article's text
    :param main_image: article's top image
    :return: pandas dataframe
    """
    local_df = df.append({'Date Published': published_date,
                          'URL': website,
                          'Author': authors,
                          'Title': title,
                          'Summary': summary,
                          'Text': text,
                          'Main Image': path_to_image_html(main_image)}, ignore_index=True)
    return local_df


def create_html_file(df):
    """
    Writes a pandas dataframe that contains extracted article content to a HTML file.

    :param df: pandas dataframe
    :return:
    """
    pd.set_option('colheader_justify', 'center')

    html_string = '''
    <html>
      <head>
      <meta charset="utf-8">
      <title>Los Angeles Times Article Information</title></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <body>
        {table}
      </body>
    </html>.
    '''

    with open('latimes_results.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(index=False, escape=False, classes='mystyle')))

    return None


# List used to store pandas content extracted 
# from articles.
article_data = []

urls = ['https://www.latimes.com/environment/story/2021-02-10/earthquakes-climate-change-threaten-california-dams',
        'https://www.latimes.com/business/story/2021-02-08/tesla-invests-in-bitcoin',
        'https://www.latimes.com/business/story/2021-02-09/joe-biden-wants-100-clean-energy-will-california-show-that-its-possible']

for url in urls:
    results = harvest_article_content(url)
    article_data.append(results)

# concat all the article content into a new pandas dataframe.
df_latimes = pd.concat(article_data)

# Create the HTML file 
create_html_file(df_latimes)

```

<p align="justify"> The custom Cascading Style Sheets(CSS) below is used to override the standard one embedded in the <i>Python</i> module <i>pandas.</i> This CSS file can be easily modified to fit your own style requirements. Save this file as <i>df_style.css</i> on your local system.</p>

``` css
/*  This is a custom Cascading Style Sheets(CSS) that used to format a 
pandas dataframe that is being exported to a HTML file.  
*/


.mystyle {
    font-size: 12pt; 
    font-family: Arial;
    border-collapse: collapse; 
    border: 4px solid silver;
    width: 100%;

}

.mystyle th {
    color: white;
    background: black;
    text-align:left;
    vertical-align:center;
    padding: 5px;
    white-space: nowrap;

}

.mystyle td {
	text-align:left;
	vertical-align:top;
    padding: 5px;

}

/* link color
https://www.colorhexa.com/0076dc
*/
.mystyle a {color:#0076dc}


/* hover link color
https://www.colorhexa.com/0076dc
*/
.mystyle a:hover {color:#dc6600}


/* expand column width for author name using nowrap */
.mystyle td:nth-child(3) {
    text-align:left;
	vertical-align:top;
    padding: 5px;
    white-space: nowrap;

}

/* on-hover for main image column 
https://www.colorhexa.com/0076dc
*/
.mystyle td:nth-child(7) a:hover {
	box-shadow: 5px 5px 2.5px #dc6600;
	-moz-box-shadow: 0px 10px 5px #dc6600;
	-webkit-box-shadow: 0px 10px 5px #dc6600; 

}

/* alternating row color
https://www.colorhexa.com/f0f8ff
*/
.mystyle tr:nth-child(even) {
    background: #f0f8ff;
}

/* on-hover color 
https://www.colorhexa.com/d7ecff
*/
.mystyle tr:hover {
    background: #d7ecff;
    cursor: pointer;

}

```

## JSON files 
<p align="justify">
Writing data to a JSON file is also very common practice in <i>Python</i>. The example below extracts content from a <a href="https://www.wsj.com/articles/investors-are-betting-corporate-earnings-have-turned-a-corner-11602408600?mod=hp_lead_pos1">Wall Street Journal</a> article.  The items being extracted include; the publish date for the article, the authors of this article, the title and summary for this article, the associated keywords assigned to this article and the URL of the article.  All these data elements are written to an external JSON file. All the data elements were normalized into string variables, which made for easier storage in the JSON file. 
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

## Basic Text Extraction with the Natural Language Toolkit (NLTK)
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

## Article summarization methods
<p align="justify">
<a href="https://github.com/codelucas/newspaper">Newspaper3k</a> has the capabilities to create a summary of the article text, but <i>newspaper<i> does not have the flexibility to tweak the the process. 
           
The example directly below shows how to use summarization with <i>newspaper<i>.  The article being summarized is part of The Guardian's "Long Read" essays.  The article's title is <i>The curse of 'white oil': electric vehicles' dirty secret</i> and its length is approximately 4400 words. <i>Newspaper<i> is designed to summarize to 5 lines, which in this case is around 107 words.
           
<p>
           
```python
           
from newspaper import Config
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

base_url = 'https://www.theguardian.com/news/2020/dec/08/the-curse-of-white-oil-electric-vehicles-dirty-secret-lithium'
article = Article(base_url, config=config)
article.download()
article.parse()
article.nlp()
print(article.summary)

The sudden excitement surrounding petróleo branco (“white oil”) derives from an invention rarely seen in these parts: the electric car.
More than half (55%) of global lithium production last year originated in just one country: Australia.
The Portuguese government is preparing to offer licences for lithium mining to international companies in a bid to exploit its “white oil” reserves.
As manufacture has slowed down, a glut of lithium on global markets has dampened the white oil boom, if only temporarily.
If people were better informed, he reasoned, it’s just possible that public opinion could swing to their side, and the country’s lithium mining plans could get shelved.
```

<p align="justify">
The example below uses the <i>Python library</i> <a href="https://pypi.org/project/sumy">sumy</a>, which is an automatic text summarizer.  <i>Sumy</i> has multiple algorithms that can be used to summarize text.  The summarizer being used in ths example is <i>LexRank</i>, which using the <a href=" https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf"> PageRank</a> algorithm in an unsupervised approach.  <i>LexRank</i> creates a summary with 151 words.
<p>

```python
from newspaper import Article
from sumy.utils import get_stop_words
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer

LANGUAGE = "english"

# configurable number of sentences
SENTENCES_COUNT = 5

article = Article('https://www.theguardian.com/news/2020/dec/08/the-curse-of-white-oil-electric-vehicles-dirty-secret-lithium')
article.download()
article.parse()

# text cleaning
text = "".join(article.text).replace("\n", " ").replace('"', "").replace("• Follow the Long Read on Twitter at @gdnlongread, and sign up to the long read weekly email here.", "")

parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)

summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

article_summary = []
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    article_summary.append(str(sentence))

clean_summary = ' '.join([str(elem) for elem in article_summary])
print(clean_summary)

Savannah is just one of several mining companies with an eye on the rich lithium deposits of central and northern Portugal. A series of local and national protests, including a march in Lisbon last year, sought to raise awareness about the impacts of modern mining on the natural environment, including potential industrial-scale habitat destruction, chemical contamination and noise pollution, as well as high levels of water consumption. The extra materials and energy involved in manufacturing a lithium-ion battery mean that, at present, the carbon emissions associated with producing an electric car are higher than those for a vehicle running on petrol or diesel – by as much as 38%, according to some calculations. In the case of Savannah’s mine in northern Portugal, the company concedes there will be local environmental impact, but argues that it will be outweighed by the upsides (inward investment, jobs, community projects). These interior regions need investment.

```
<p align="justify">
The Guardian's article <i>The curse of 'white oil': electric vehicles' dirty secret</i> is about the environmental impact of mining lithium for electric vehicles.
The <i>sumy</i> summarization seems to be more accurate than <i>newspaper's<i> summarization for the same article.      
<p>
	
