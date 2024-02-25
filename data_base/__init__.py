
# TODO экспорт название курсоров БД
from .database import (cursor_db, basket_db, date_add_db, all_analysis_db, add_db,
                       order_done_db, date_person_db, archive_db, profit_db, profit_income_db,
                       job_db, complex_analyses_db, midwifery_db, pattern_db, sur_analysis_db)

# TODO экспорт самих курсоров для закрытия и коммита БД
from .database import (conn, conn_basket, midwifery_conn, conn_analysis, connect_added,
                       connect_order_done, connect_person_date, connect_archive, connect_profit,
                       connect_profit_income, connect_job, conn_complex_analyses,
                       connect_midwifery, connect_pattern, connect_sur_analysis)
