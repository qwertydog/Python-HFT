from Database import Database
from Exchange import PoloniexExchange
from autobahn.asyncio.wamp import ApplicationRunner
from Subscriber import Subscriber


if __name__ == '__main__':
    db = Database()
    # db.print()

    exchange = PoloniexExchange(db)


    def get_coin_data():
        runner = ApplicationRunner(url=exchange.endpoint, realm=u"realm1", extra={'db': db, 'exchange': exchange})
        print('Opening connection to exchange: {0}'.format(exchange.name))
        runner.run(Subscriber)


    get_coin_data()

    db.close()
