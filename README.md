
## Primary objective of this repository
<p align="justify">
This repository was developed to provide technical insights on how to properly utilized the <i>Python</i> library <i>Newspaper3k</i> to query a news source, such as the [Wall Street Journal]( https://www.wsj.com)
</p>

### Newspaper Configuration
<p align="justify">
<i>Newspaper3k</i> uses the <i>Python requests</i> module to make a connection request to a news website. <i>Python requests</i> allows connections to have HTTP headers information and <i>Newspaper3k</i> includes this same capability within its code base. These configuration parameters include: sending a browser's user agent string as part of the request, establishing a connection timeout period (in seconds) and using proxies.  
</p>

#### Configuration example

```python
from newspaper import Configuration

config = Configuration()
config.browser_user_agent = string value
config.proxies = dictionary of proxies
config.request_timeout = int value 
```

#### Sample Usage example

```python
from newspaper import Configuration

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

# add your proxy information
PROXIES = {
           'http': "http://ip_address:port_number",
           'https': "https://ip_address:port_number"
          }

config = Configuration()
config.browser_user_agent = USER_AGENT
config.proxies = PROXIES
config.request_timeout = 10
```

#### Realworld Usage example

```python
from newspaper import Configuration
from newspaper import Article

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Configuration()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

url = 'https://www.wsj.com'
article = Article(url, config=config)
 <DO SOMETHING>
```


