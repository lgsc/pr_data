from data_lib import exports
import logging

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    df = exports.get_df_from_csv(file='data_lib/record_de_votacion_de_senado.csv')
    log.info(list(df))


if __name__ == '__main__':
    main()
