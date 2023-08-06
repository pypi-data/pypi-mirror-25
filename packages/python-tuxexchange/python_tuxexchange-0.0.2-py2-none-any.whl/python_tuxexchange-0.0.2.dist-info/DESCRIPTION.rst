# python-tuxechange

![python](https://img.shields.io/badge/python-2.7-blue.svg)

Inspired by [this](https://github.com/Olliecad1/Tux_Exchange_Python) wrapper written by [Olliecad1](https://github.com/Olliecad1) and following the example of [this](https://github.com/ericsomdahl/python-bittrex) wrapper written by [Eric Somdahl](https://github.com/ericsomdahl)

> I ([sneurlax](https://github.com/sneurlax)) am not affiliated with, nor paid by [Tux Exchange](https://tuxexchange.com).  Use at your own risk.

**Superceded by [crypto-exchange-apis](https://github.com/init-industries/crypto-exchange-apis)**

## Installation

Install with `pip` using `pip install python-tuxexchange`

## Usage

See available methods in the [Tux exchange API docs](https://tuxexchange.com/docs)

```python
from tuxexchange import tuxexchange
tuxexchange = tuxexchange.Tuxexchange()

print tuxexchange.api_query('getcoins')
{'PPC': {'website': 'www.peercoin.org', ...
print tuxexchange.api_query('getticker')
{'BTC_ICN': {'last': '0.00040418', ...
```

[test_manual.py](https://github.com/init-industries/python-tuxexchange/blob/master/tuxexchange/test_manual.py):
```python
from tuxexchange import Tuxexchange

tuxexchange = Tuxexchange()

print tuxexchange.api_query('getcoins')
{'PPC': {'website': 'www.peercoin.org', ...
print tuxexchange.api_query('getticker')
{'BTC_ICN': {'last': '0.00040418', ...
```

## Testing

Run unit tests in [test.py](https://github.com/init-industries/python-tuxexchange/blob/master/tuxexchange/test.py)


