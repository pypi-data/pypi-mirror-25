pi-bittrex  
==============

[![Build Status](https://travis-ci.org/bealox/p3-bittrex.svg?branch=master)](https://travis-ci.org/bealox/p3-bittrex)

Python 3 API Wrapper for Bittrex.  I am **NOT** associated with Bittrex, please use at your own risk.

Tips are appreciated:
* IOTA:BRTJHYOGVJZULCNMZHJPILPJUNPWGFSBMKHW9VQTHRASCCZFEKQQMIQYMXYCDVAIGRYGFKXMG9W9RKBBCIBAIDOSJ9

Install
-------------
Use pip3 to install the pacakge.
```bash
pip install p3_bittrex
```

Set up Option 1 
-------------
Set your client to BITTREX_KEY env variables.
Set your secret to BITTREX_SECRET env variables.

```bash
 export BITTREX_KEY=<your_key>
 export BITTREX_SECRET=<your_secret>
```

Eaxmple:
```python
from .p3_bittrex import Bittrex
my_bittrex = Bittrex()
my_bittrex.get_markets()
{'success': True, 'message': '', 'result': [{'MarketCurrency': 'LTC', ...
```

Set up Option 2 
-------------
Specify your client and key in the initialisation 

Example:
```python
from .p3_bittrex import Bittrex
my_bittrex = Bittrex(key='your_key', secret='youesecret')
my_bittrex.get_markets()
{'success': True, 'message': '', 'result': [{'MarketCurrency': 'LTC', ...
```



