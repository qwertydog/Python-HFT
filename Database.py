import sqlite3


class Database:
    """Database access operations"""

    def __init__(self):
        self._db = sqlite3.connect("HFT.sqlite")
        self.seed()

    def seed(self):
        #self._db.execute("DROP TABLE IF EXISTS exchangeCurrencyLog;")
        #self._db.execute("DROP TABLE IF EXISTS currency;")
        #self._db.execute("DROP TABLE IF EXISTS exchangeCurrency;")
        #self._db.execute("DROP TABLE IF EXISTS exchange;")
        #self._db.commit()

        self._db.execute("PRAGMA foreign_keys = ON;")

        self._db.execute("""CREATE TABLE IF NOT EXISTS currency
                           (id       INTEGER PRIMARY KEY NOT NULL,
                            currency TEXT                NOT NULL  UNIQUE,
                            name     TEXT                NOT NULL);""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS exchangeCurrencyLog
                           (id             INTEGER PRIMARY KEY NOT NULL,
                            timestamp      NUMERIC             NOT NULL  DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'now')),
                            exchangeId     INTEGER             NOT NULL  REFERENCES exchange(id) ON UPDATE CASCADE ON DELETE CASCADE,
                            currency1Id    INTEGER             NOT NULL  REFERENCES currency(id) ON UPDATE CASCADE ON DELETE CASCADE,
                            currency2Id    INTEGER             NOT NULL  REFERENCES currency(id) ON UPDATE CASCADE ON DELETE CASCADE,
                            last           REAL                NOT NULL,
                            lowestAsk      REAL                NOT NULL,
                            highestBid     REAL                NOT NULL,
                            percentChange  REAL                NOT NULL,
                            baseVolume     REAL                NOT NULL,
                            quoteVolume    REAL                NOT NULL,
                            isFrozen       NUMERIC             NOT NULL,
                            last24hrHigh   REAL                NOT NULL,
                            last24hrLow    REAL                NOT NULL);""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS exchange
                           (id       INTEGER PRIMARY KEY NOT NULL,
                            name     TEXT                NOT NULL  UNIQUE,
                            endpoint TEXT                NOT NULL);""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS exchangeCurrency
                           (id           INTEGER PRIMARY KEY NOT NULL,
                            currencyId   INTEGER             NOT NULL    REFERENCES currency(id) ON UPDATE CASCADE   ON DELETE CASCADE,
                            exchangeId   INTEGER             NOT NULL    REFERENCES exchange(id) ON UPDATE CASCADE   ON DELETE CASCADE,
                            txFee        REAL                NOT NULL,
                            minConf      INTEGER             NOT NULL,
                            disabled     NUMERIC             NOT NULL,
                            delisted     NUMERIC             NOT NULL,
                            frozen       NUMERIC             NOT NULL);""")

        self._db.execute("""CREATE TABLE IF NOT EXISTS exchangeCommand
                           (id           INTEGER PRIMARY KEY NOT NULL,
                            exchangeId   INTEGER             NOT NULL    REFERENCES exchange(id) ON UPDATE CASCADE   ON DELETE CASCADE,
                            command      TEXT                NOT NULL);""")
        self._db.commit()

    def execute(self, *args, **kwargs):
        return self._db.execute(*args, **kwargs)

    def commit(self):
        self._db.commit()

    def close(self):
        self._db.close()

    def print(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM currency;")
        for row in cursor.fetchall():
            print(row)
        cursor.execute("SELECT * FROM exchangeCurrencyLog;")
        for row in cursor.fetchall():
            print(row)
        cursor.execute("SELECT * FROM exchange;")
        for row in cursor.fetchall():
            print(row)
        cursor.execute("SELECT * FROM exchangeCurrency;")
        for row in cursor.fetchall():
            print(row)
