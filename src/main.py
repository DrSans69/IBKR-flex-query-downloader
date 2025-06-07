import logging

from data import Credentials
import cli

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


def main():
    parser = cli.setup_parser()

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
