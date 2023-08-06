from zeep import Client


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Nbg(object):
    """
    Client for National Bank of Georgia currency api
    """

    _SUPPORTED_CURRENCIES = (
        'AED', 'AMD', 'AUD', 'AZN', 'BGN', 'BYR', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EEK', 'EGP', 'EUR', 'GBP', 'HKD',
        'HUF', 'ILS', 'INR', 'IRR', 'ISK', 'JPY', 'KGS', 'KWD', 'KZT', 'LTL', 'LVL', 'MDL', 'NOK', 'NZD', 'PLN', 'RON',
        'RSD', 'RUB', 'SEK', 'SGD', 'TJS', 'TMT', 'TRY', 'UAH', 'USD', 'UZS')

    WSDL_URL = 'http://nbg.gov.ge/currency.wsdl'

    __client = None

    def __init__(self, currency='USD'):
        self.currency = currency

        self.currency_rate = __class__.get_currency_rate(currency)
        self.description = __class__.get_description(currency)
        self.change = __class__.get_change(currency)
        self.rate = __class__.get_rate(currency)
        self.date = __class__.get_date()

    @classproperty
    def client(cls):
        """Return client of nbg-py webservice"""
        if cls.__client is None:
            cls.__client = Client(cls.WSDL_URL)
        return cls.__client.service

    @classmethod
    def is_supported(cls, currency):
        """Check if currency is supported"""
        if currency in cls._SUPPORTED_CURRENCIES:
            return True
        else:
            return False

    @classmethod
    def validate(cls, currency):
        """if currency is not supported - reutn exception"""
        if not cls.is_supported(currency):
            raise Exception('Currency with name "{}" is not supported'.format(currency))

    @classmethod
    def get_currency_rate(cls, currency):
        """Return the currency rate"""
        cls.validate(currency)
        return cls.client.GetCurrency(currency.upper())

    @classmethod
    def get_description(cls, currency):
        """Return the currency description"""
        cls.validate(currency)
        return cls.client.GetCurrencyDescription(currency.upper())

    @classmethod
    def get_change(cls, currency):
        """Return the difference of currency rate"""
        cls.validate(currency)
        return cls.client.GetCurrencyChange(currency.upper())

    @classmethod
    def get_rate(cls, currency):
        """Return the currency rate change status (-1, 0 or 1)"""
        cls.validate(currency)
        return cls.client.GetCurrencyRate(currency.upper())

    @classmethod
    def get_date(cls):
        """Return the date of exchange rate"""
        return cls.client.GetDate()

