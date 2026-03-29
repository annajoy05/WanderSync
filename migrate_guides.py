import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        
        print("Checking for guide columns in trip_experiences...")
        c.execute("SELECT column_name FROM information_schema.columns WHERE table_name='trip_experiences' AND column_name='guide_name';")
        if not c.fetchone():
            print("Adding guide_name, guide_phone, guide_specialty columns to trip_experiences...")
            c.execute("ALTER TABLE trip_experiences ADD COLUMN guide_name TEXT;")
            c.execute("ALTER TABLE trip_experiences ADD COLUMN guide_phone TEXT;")
            c.execute("ALTER TABLE trip_experiences ADD COLUMN guide_specialty TEXT;")
            conn.commit()
            print("Migration successful.")
        else:
            print("Guide columns already exist.")
            
        c.close()
        conn.close()
    except Exception as e:
        print(f"Migration error: {str(e)}")

if __name__ == '__main__':
    migrate()
