import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        
        print("Checking for points and achievements columns in users table...")
        c.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='points';")
        if not c.fetchone():
            print("Adding points and achievements columns to users table...")
            c.execute("ALTER TABLE users ADD COLUMN points INTEGER DEFAULT 0;")
            c.execute("ALTER TABLE users ADD COLUMN achievements TEXT DEFAULT '';")
            conn.commit()
            print("Migration successful.")
        else:
            print("Gamification columns already exist.")
            
        c.close()
        conn.close()
    except Exception as e:
        print(f"Migration error: {str(e)}")

if __name__ == '__main__':
    migrate()
