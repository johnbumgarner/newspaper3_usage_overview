
## Primary objective of this repository
<p align="justify">
This repository was developed to provide technical insights on how to properly utilized the <i>Python</i> library <i>Newspaper3k</i> to query a news source, such as the [Wall Street Journal](https://www.wsj.com)
</p>

### Newspaper Configuration for Querying 

<p align="justify">
<i>Newspaper3k</i> uses the <i>Python requests</i> module to make a connection request to a news website. <i>Python requests</i> allows connections to have HTTP headers information and <i>Newspaper3k</i> includes this capability within its code base. These <i>Newspaper3k</i> configuration parameters include: sending a browser's user agent string as part of the request, establishing a connection timeout period (in seconds) and using proxies.  
           
Some website queried with <i>Newspaper3k</i> will send back status response code indicating a problem with the conenction.  These status response code include:

- HTTP 400 Bad Request error 
- HTTP 403 Forbidden client error
- HTTP 406 Not Acceptable client error

One of the primary root causes of these errors is the lack of a browser's user agent string in the request. 

Another potential issue when making requests with <i>Newspaper3k</i> is a <i>ReadTimeout<i> error.  These error are usually linked to not providing a connection timeout period in your request. The <i>Python requests</i> documentation makes a point that setting a connection timeout is considered best practice.
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
One of the primary purposes of <i>Newspaper3k</i> is text extraction from a news website. Out-of-box <i>Newspaper3k</i> does a good job of extracting content, but it is not flawless.  Several the issues posted to either [Stack Overflow](https://stackoverflow.com/search?q=newspaper3k) or to the GitHub repository for [Newspaper ](https://github.com/codelucas/newspaper/issues)

</p>

