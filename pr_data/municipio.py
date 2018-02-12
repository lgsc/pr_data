from pr_data.base import exports as exp
import logging
from pandasql import sqldf

log = logging.getLogger(__name__)


def school_appends():
    raw_data = exp.get_df_from_csv(file_name='data/escuelas_publicas_2017.csv')
    # Label records for Punta Santiago to Humacao municipio
    raw_data.loc[raw_data.DIRECCION_MUNICIPIO == 'PUNTA SANTIAGO, HUMACAO',
                 'DIRECCION_MUNICIPIO'] = 'HUMACAO'

    query = \
        '''SELECT DIRECCION_MUNICIPIO as municipio
            ,count(*) as total_schools
            ,SUM(MATRICULA_TOTAL) as total_matriculation
            ,ROUND(avg(BAJO_NIVEL_POBREZA), 2) as avg_perc_students_in_poverty
            from raw_data where DIRECCION_MUNICIPIO not in ("")
            group by 1 order by 2 desc'''

    return sqldf(query)


def main():
    logging.basicConfig(level=logging.INFO)
    df = school_appends()
    log.info(df)


if __name__ == '__main__':
    main()
