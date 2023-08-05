import argparse
import logger
import yaml

import logging
from regmitter import Regmitter


def main():
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument("-t", "--type", dest="type",
            default="pull", choices=["pull", "push", "remove"],
            help="Type of operation")
        parser.add_argument("images", type=str,
            default="images.yml",
            help="File with images and their tags")
        parser.add_argument("--docker-version", dest="dv",
            default="auto", help="Docker client version")
        parser.add_argument("-l", "--log", dest="log",
            help="Redirect logging to file")
        args = parser.parse_args()

        if args.log is not None:
            log = logging.getLogger(__name__)
            log.addHandler(logger.FileHandler(args.log))
            log.setLevel(logging.DEBUG)
        else:
            log = logging.getLogger(__name__)
            log.addHandler(logger.StreamHandler())
            log.setLevel(logging.DEBUG)

        with open(args.images) as im_file:
            images = yaml.load_all(im_file).next()
        regmitter = Regmitter(args.dv, args.log)

        if args.type == "pull":
            regmitter.pull(images)
        elif args.type == "push":
            regmitter.push(images)
        elif args.type == "remove":
            regmitter.remove(images)

    except KeyboardInterrupt:
        print('\nThe process was interrupted by the user')
        raise SystemExit

if __name__ == "__main__":
    main()
