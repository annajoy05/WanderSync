import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        
        print("Checking for profile-related columns in users table...")
        c.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='headline';")
        if not c.fetchone():
            print("Adding headline, bio, location, profile_pic, and cover_pic columns to users table...")
            c.execute("ALTER TABLE users ADD COLUMN headline TEXT DEFAULT '';")
            c.execute("ALTER TABLE users ADD COLUMN bio TEXT DEFAULT '';")
            c.execute("ALTER TABLE users ADD COLUMN location TEXT DEFAULT '';")
            c.execute("ALTER TABLE users ADD COLUMN profile_pic TEXT DEFAULT '';")
            c.execute("ALTER TABLE users ADD COLUMN cover_pic TEXT DEFAULT '';")
            conn.commit()
            print("Migration successful.")
        else:
            print("Profile columns already exist.")
            
        c.close()
        conn.close()
    except Exception as e:
        print(f"Migration error: {str(e)}")

if __name__ == '__main__':
    migrate()
