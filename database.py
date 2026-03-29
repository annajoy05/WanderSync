import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create tables based on architecture (PostgreSQL syntax)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            preferences TEXT,
            points INTEGER DEFAULT 0,
            achievements TEXT DEFAULT '',
            headline TEXT DEFAULT '',
            bio TEXT DEFAULT '',
            location TEXT DEFAULT '',
            profile_pic TEXT DEFAULT '',
            cover_pic TEXT DEFAULT '',
            google_id TEXT UNIQUE,
            phone TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS trip_experiences (
            trip_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            origin TEXT,
            destination TEXT,
            trip_date TEXT,
            age INTEGER,
            companion_type TEXT,
            has_children BOOLEAN DEFAULT FALSE,
            interests TEXT,
            cuisine_preferences TEXT,
            trip_duration INTEGER,
            main_transport TEXT,
            travel_style TEXT,
            stay_name TEXT,
            stay_price REAL,
            stay_rating REAL,
            total_expense REAL,
            guide_name TEXT,
            guide_phone TEXT,
            guide_specialty TEXT,
            emergency_ambulance TEXT DEFAULT '',
            emergency_police TEXT DEFAULT '',
            emergency_health TEXT DEFAULT ''
        );

        -- Add columns if they don't exist (for existing tables)
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='trip_experiences' AND column_name='emergency_ambulance') THEN
                ALTER TABLE trip_experiences ADD COLUMN emergency_ambulance TEXT DEFAULT '';
            END IF;
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='trip_experiences' AND column_name='emergency_police') THEN
                ALTER TABLE trip_experiences ADD COLUMN emergency_police TEXT DEFAULT '';
            END IF;
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='trip_experiences' AND column_name='emergency_health') THEN
                ALTER TABLE trip_experiences ADD COLUMN emergency_health TEXT DEFAULT '';
            END IF;
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='google_id') THEN
                ALTER TABLE users ADD COLUMN google_id TEXT UNIQUE;
            END IF;
        END $$;

        CREATE TABLE IF NOT EXISTS places_visited (
            place_id SERIAL PRIMARY KEY,
            trip_id INTEGER REFERENCES trip_experiences(trip_id),
            place_order INTEGER,
            place_name TEXT,
            place_rating REAL,
            entry_fee REAL,
            distance_from_prev REAL,
            travel_method TEXT,
            travel_cost REAL,
            travel_rating REAL,
            experience_review TEXT
        );

        CREATE TABLE IF NOT EXISTS blogs (
            blog_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            short_description TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS blog_images (
            image_id SERIAL PRIMARY KEY,
            blog_id INTEGER REFERENCES blogs(blog_id) ON DELETE CASCADE,
            image_url TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS blog_likes (
            like_id SERIAL PRIMARY KEY,
            blog_id INTEGER REFERENCES blogs(blog_id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(user_id),
            UNIQUE(blog_id, user_id)
        );

        CREATE TABLE IF NOT EXISTS blog_comments (
            comment_id SERIAL PRIMARY KEY,
            blog_id INTEGER REFERENCES blogs(blog_id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(user_id),
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS notes (
            note_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            color TEXT DEFAULT '#ffeb3b',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.commit()
    c.close()
    
    # Run migrations/fixes for existing tables
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS phone TEXT DEFAULT \'\';')
        conn.commit()
    except:
        conn.rollback()
    c.close()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("PostgreSQL Database initialized successfully.")
