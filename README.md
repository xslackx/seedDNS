# seedDNS
Hotcache your local dns with most visited sites, not ordened list.

seedDNS arose from the need to test my local DNS servers, I am preparing for LPIC2 part 2 and one of the exam topics is DNS server administration.

As I wanted to explore the study tools a little more and needed some load, I wrote this small script that collects the most accessed sites compiled by Alexa and makes a request to the local DNS server.

Feeding the DNS cache.

## what you need?
python3.6+, dig

## usage CLI
Create, activate the environment and install the requirements.txt
```
usage: seed.py [-h] -s HOST -m MODE -t TYPE

Initialize seedDNS

options:
  -h, --help            show this help message and exit
  -s HOST, --host HOST  DNS server address (default: None)
  -m MODE, --mode MODE  0 to asyncio mode or 1 to sync mode (default: None)
  -t TYPE, --type TYPE  Type of DNS message (default: None) 
```

## usage instance
```python
from seedDNS import seedDNS as seed
# Initialize 
client = seed()
# Download the data
client.top1m()
# Format the data
client.fmtfile()
# Query DNS  
# options dns, mode, type_msg
client.consult('127.0.0.1', 0, 'ANY')

```

