import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def migrate():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    
    print("Starting accessibility migration...")
    
    # 1. Add disability_info to users
    c.execute('''
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='disability_info') THEN
                ALTER TABLE users ADD COLUMN disability_info TEXT DEFAULT '';
            END IF;
        END $$;
    ''')
    
    # 2. Add accessibility_notes to trip_experiences
    c.execute('''
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='trip_experiences' AND column_name='accessibility_notes') THEN
                ALTER TABLE trip_experiences ADD COLUMN accessibility_notes TEXT DEFAULT '';
            END IF;
        END $$;
    ''')
    
    conn.commit()
    c.close()
    conn.close()
    print("Accessibility migration completed successfully.")

if __name__ == '__main__':
    migrate()
