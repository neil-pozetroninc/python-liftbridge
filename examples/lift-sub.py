import argparse
from datetime import datetime

from python_liftbridge import Lift
from python_liftbridge import Stream


def parse_arguments():
    '''Argument parsing for the script'''
    parser = argparse.ArgumentParser(
        description='Liftbridge sub script.',
    )
    parser.add_argument(
        'subject',
        metavar='subject',
    )
    parser.add_argument(
        'stream',
        metavar='stream',
    )
    parser.add_argument(
        '-s',
        '--server',
        metavar='s',
        nargs='?',
        default='127.0.0.1:9292',
        help='(default: %(default)s)',
    )
    parser.add_argument(
        '-t',
        '--timestamp',
        action='store_true',
        help='Display timestamps',
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    client = Lift(ip_address=args.server)

    count = 0

    for message in client.subscribe(
        Stream(
            args.subject,
            args.stream,
        ).start_at_earliest_received(),
    ):
        print("{} [#{}] Received on [{} - {}]: '{}'".format(
            datetime.fromtimestamp(
                int(message.timestamp) /
                1000000000,
            ), count, args.subject, args.stream, message.value.decode('utf-8'),
        ))
        count = count + 1


main()