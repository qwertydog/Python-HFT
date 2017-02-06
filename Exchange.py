from Database import Database
import urllib.request
import json


class Exchange(object):
    """Exchange base class"""

    def __init__(self, db: Database):
        self._db = db


class PoloniexExchange(Exchange):
    """Poloniex Exchange subclass"""

    def __init__(self, db: Database):
        super().__init__(db)
        self.name = "Poloniex"
        self.endpoint = "wss://api.poloniex.com"

        db.execute("INSERT OR IGNORE INTO exchange (name, endpoint) VALUES (?, ?);", (self.name, self.endpoint))

        url = "https://poloniex.com/public?command=returnCurrencies"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf8'))

        for key, value in data.items():
            db.execute("INSERT OR REPLACE INTO currency (id, currency, name) "
                       "VALUES ((SELECT id"
                       "         FROM currency"
                       "         WHERE currency.currency = ?), ?, ?);", (key, key, value['name']))

            db.execute("""INSERT OR REPLACE INTO exchangeCurrency (id, currencyId, exchangeId, txFee, minConf, disabled, delisted, frozen)
                          VALUES ((SELECT id
                                   FROM exchangeCurrency
                                   WHERE currencyId = (SELECT id
                                                       FROM currency
                                                       WHERE currency = ?)
                                   AND exchangeId = (SELECT id
                                                     FROM exchange
                                                     WHERE name = ?)),
                                  (SELECT id
                                   FROM currency
                                   WHERE currency = ?),
                                  (SELECT id
                                   FROM exchange
                                   WHERE name = ?), ?, ?, ?, ?, ?);""", (key,
                                                                         self.name,
                                                                         key,
                                                                         self.name,
                                                                         value['txFee'],
                                                                         value['minConf'],
                                                                         value['disabled'],
                                                                         value['delisted'],
                                                                         value['frozen']))
        db.commit()

    def print(self):
        print(self.endpoint)


