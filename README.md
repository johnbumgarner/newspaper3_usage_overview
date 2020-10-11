

This repository was developed to provide technical insights on how to properly utilized the <i>Python</i> library <i>Newspaper3k </i> to query a news source, such as the [Wall Street Journal]( https://www.wsj.com)


#### Newspaper Configuration

```python
from newspaper import Configuration

config = Configuration()
config.browser_user_agent = string value
config.request_timeout = int value 
config.proxies = dictionary of proxies
```


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
config.request_timeout = 10
config.proxies = PROXIES

```





