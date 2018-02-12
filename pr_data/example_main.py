from base import exports
import logging

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    df = exports.edu_county_appends()
    log.info(df)


if __name__ == '__main__':
    main()
