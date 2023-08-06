import logging
import sys

from .haproxy import haproxy
from .pull import pull
from .watchgit import watch_git, watch_git_http


def run():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    print('argv---', sys.argv)
    if sys.argv[1] == 'register_kong':
        from .register_kong import register_kong
        register_kong(sys.argv[2:])
    elif sys.argv[1] == 'watch_git':
        watch_git(sys.argv[2:])
    elif sys.argv[1] == 'watch_git_http':
        watch_git_http(sys.argv[2:])
    elif sys.argv[1] == 'haproxy':
        haproxy(sys.argv[2:])
    elif sys.argv[1] == 'pull':
        pull(sys.argv[2:])
    else:
        logging.warning('method not regognize')


if __name__ == '__main__':
    watch_git(['git+ssh://git@github.com/qbtrade/quantlib.git', 'log_rpc.py'])
