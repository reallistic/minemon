import requests

from minemon import utils, db, cli
from minemon.poolclient import PoolClient


def collect(address, db_path):
    client = PoolClient(address=address)
    addy_stats = client.get_address_stats()
    werk_stats = client.get_worker_stats()

    hashrate = round(sum(map(lambda w: w.get('hashrate'), werk_stats)))
    is_down = 1 if hashrate == 0 else 0
    addy_stats = addy_stats.get('stats')
    total_paid = addy_stats.get('paid')
    balance = addy_stats.get('balance')
    date = utils.get_iso8601()

    db.insert(db_path, date=date, hashrate=hashrate, is_down=is_down,
              balance=balance, total_paid=total_paid)


if __name__ == '__main__':
    args = cli.get_stat_args()

    collect(args.address, args.file)
