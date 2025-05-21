import psycopg2
from psycopg2 import sql

# اطلاعات اتصال به دیتابیس را اینجا وارد کن
DB_NAME = 'pania_erp'
DB_USER = 'postgres'
DB_PASSWORD = '77308914elia'
DB_HOST = 'localhost'
DB_PORT = '5432'

def add_missing_columns():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    try:
        # اضافه کردن ستون‌ها اگر وجود ندارند
        columns = [
            ("manager_id", "integer NULL"),
            ("budget", "decimal(10,2) NULL"),
            ("created_at", "timestamp with time zone NULL"),
            ("updated_at", "timestamp with time zone NULL"),
            ("status", "varchar(20) NULL")
        ]
        for col, coltype in columns:
            cur.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='taskflow_project' AND column_name='{col}') THEN
                    ALTER TABLE taskflow_project ADD COLUMN {col} {coltype};
                END IF;
            END$$;
            """)
        # اضافه کردن ForeignKey اگر وجود ندارد
        cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.table_constraints WHERE table_name='taskflow_project' AND constraint_name='taskflow_project_manager_id_fkey'
            ) THEN
                ALTER TABLE taskflow_project ADD CONSTRAINT taskflow_project_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES accounts_user(id) DEFERRABLE INITIALLY DEFERRED;
            END IF;
        END$$;
        """)
        conn.commit()
        print('All missing columns and foreign key added (if not exists).')
    except Exception as e:
        print('Error:', e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    add_missing_columns() 