
def get_sql_query_br_from_db_gistek(date_yyyymmdd: str) -> str:
    """SQL Запрос для получения загруженных из БР данных в БД ГИСТЭК"""

    sql_query = f"""
            WITH spis AS (SELECT * FROM GISTEK.GISTEK_LOAD_BR)
            SELECT
            	b.TRADER_CODE,
            	decode(b.DPG_TYPE,1,'П',2,'Г') GTP_type,
            	a.*
            FROM
            	spis a
            JOIN GISTEK.TRADER b ON
            	b.real_trader_id = a.object_id
            WHERE
            	A.TARGET_DATE = TO_DATE({date_yyyymmdd}, 'yyyymmdd')
            	AND TO_DATE({date_yyyymmdd}, 'yyyymmdd') BETWEEN b.begin_date AND b.end_date
            	AND START_VER IN (SELECT max(START_VER) 
            				  FROM GISTEK.GISTEK_LOAD_BR 
            				  WHERE TARGET_DATE = TO_DATE({date_yyyymmdd}, 'yyyymmdd')) 
            ORDER BY 1"""
    return sql_query
