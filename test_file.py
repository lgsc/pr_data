from data_lib import exports
import logging

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    df = exports.get_df_from_csv(
        file_name='data_lib/mapa_de_donaciones_recibidas.csv')
    log.info(df)


if __name__ == '__main__':
    main()
