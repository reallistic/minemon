from argparse import ArgumentParser


def add_db_args(parser):
    parser.add_argument('-f', '--file', help='The location of the db file',
                        required=True)


def add_pool_args(parser):
    parser.add_argument('-a', '--address', help='The monero address',
                        required=True)


def get_db_args():
    parser = ArgumentParser()
    add_db_args(parser)
    args = parser.parse_args()
    return args


def get_stat_args():
    parser = ArgumentParser()
    add_db_args(parser)
    add_pool_args(parser)
    args = parser.parse_args()
    return args
