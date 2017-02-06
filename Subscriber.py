import asyncio
from autobahn.asyncio.wamp import ApplicationSession
from Tensorflow import Tensorflow


class Subscriber(ApplicationSession):
    def __init__(self, config=None):
        super().__init__(config)
        self._db = self.config.extra['db']
        self._tf = Tensorflow(self._db)
        self._exchange = self.config.extra['exchange']

    async def onJoin(self, details):
        print("Success!\n")

        def tick(*data, **kwargs):
            currencies = data[0].split("_")

            print("Adding {0} to database".format(data))

            self._db.execute("""INSERT INTO exchangeCurrencyLog (exchangeId,
                                                                 currency1Id,
                                                                 currency2Id,
                                                                 last,
                                                                 lowestAsk,
                                                                 highestBid,
                                                                 percentChange,
                                                                 baseVolume,
                                                                 quoteVolume,
                                                                 isFrozen,
                                                                 last24hrHigh,
                                                                 last24hrLow)
                                 VALUES ((SELECT id
                                          FROM exchange
                                          WHERE name = ?),
                                         (SELECT id
                                          FROM currency
                                          WHERE currency = ?),
                                         (SELECT id
                                          FROM currency
                                          WHERE currency = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (self._exchange.name,
                                                                                                currencies[0],
                                                                                                currencies[1],
                                                                                                data[1],
                                                                                                data[2],
                                                                                                data[3],
                                                                                                data[4],
                                                                                                data[5],
                                                                                                data[6],
                                                                                                data[7],
                                                                                                data[8],
                                                                                                data[9]))
            self._db.commit()

            self._tf.run(currencies)

        await self.subscribe(tick, u'ticker')

    def onDisconnect(self):
        asyncio.get_event_loop().stop()
