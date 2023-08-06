# NBG Currency py


National Bank of Georgia currency webservice API wrapper in Python

## Installation
You can install this package using pip

```
$ pip install
```

Or just clone it from Github
```
$ git clone git@github.com:ent1c3d/NBG-py.git
```

## How to use package

After installation -  you must import package
```python
from nbg import Nbg
```

Than You can make a choice:

- 1 - Instantiate object from Class and get data from it's properties like this :
```python
try:
    nbg = Nbg("USD")
    print(nbg.description)
    print(nbg.currency_rate)
    print(nbg.change)
    print(nbg.rate)
    print(nbg.date)
except Exception as error:
    print('caught this error: ' + str(error))
```

- 2 - Call static methods of Nbg class
```python
try:
    print(Nbg.get_description('USD'))
    print(Nbg.get_currency_rate('USD'))
    print(Nbg.get_change('USD'))
    print(Nbg.get_rate('USD'))
    print(Nbg.get_date())
except Exception as error:
    print('caught this error: ' + str(error))
```