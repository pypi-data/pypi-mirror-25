import psycopg2

from plugs_status.settings import app_settings as settings

def check_connection():
    if settings['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        conn = psycopg2.connect(
            dbname=settings['NAME'],
            user=settings['USER'],
            password=settings['PASSWORD'],
            host=settings['HOST'],
            port=settings['PORT'],
            connect_timeout=3
        )
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        cur.fetchone()
        cur.close()
        conn.close()
