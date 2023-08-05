import argparse
import time
import sys

from .scryfall import Scryfall


def main():
    parser = argparse.ArgumentParser("scrycli")

    # TODO
    # card_info = parser.add_mutually_exclusive_group()
    # card_info.add_argument(
    #     "--all", "-a",
    #     const="all",
    #     action="store_const",
    #     dest="format",
    #     help="show all information about cards"
    # )
    # card_info.add_argument(
    #     "--full", "-f",
    #     const="full",
    #     action="store_const",
    #     dest="format",
    #     help="show information that the card faces have"
    # )
    # card_info.add_argument(
    #     "--small", "-s",
    #     const="all",
    #     action="store_const",
    #     dest="format",
    #     help="show name, mana cost and type line"
    # )
    # card_info.add_argument(
    #     "--tiny", "-t",
    #     const="tiny",
    #     action="store_const",
    #     dest="format",
    #     default=True,
    #     help="show name and mana cost (default)"
    # )
    # card_info.add_argument(
    #     "--name", "-n",
    #     const="name",
    #     action="store_const",
    #     dest="format",
    #     help="only show the name of the card"
    # )
    # card_info.add_argument(
    #     "--json", "-j",
    #     const="json",
    #     action="store_const",
    #     dest="format",
    #     help="output all information about the card as json"
    # )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command"
    )

    search = subparsers.add_parser("search")
    search.add_argument("query", nargs=argparse.REMAINDER)

    random = subparsers.add_parser("random")
    random.add_argument(
        "count",
        nargs="?",
        type=int,
        default=1,
        help="amount of random cards to get"
    )

    args = parser.parse_args()

    api = Scryfall()

    try:
        if args.command == "search":
            for i in api.search(" ".join(args.query)):
                print("---")
                print(i)
        elif args.command == "random":
            for i in api.random(args.count):
                print("---")
                print(i)
        else:
            parser.print_help()
            return 1
    except api.TooManyRequests:
        time.sleep(1)
        return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
