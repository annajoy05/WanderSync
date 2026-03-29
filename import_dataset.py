import csv
import database
from psycopg2.extras import execute_values

def import_csv():
    conn = database.get_db_connection()
    c = conn.cursor()
    
    # Create a default user to own these trips
    c.execute("INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING user_id", 
              ('Dataset User', 'dataset@example.com', 'hashed'))
    res = c.fetchone()
    user_id = res[0] if res else None
    if not user_id:
        c.execute("SELECT user_id FROM users WHERE email='dataset@example.com'")
        res = c.fetchone()
        if res:
            user_id = res[0]
        else:
            # Fallback
            c.execute("SELECT user_id FROM users LIMIT 1")
            res = c.fetchone()
            if not res:
                print("No users in DB. Something is wrong.")
                return
            user_id = res[0]

    trips = {}
    with open('travel_dataset.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = row['trip_id']
            if tid not in trips:
                trips[tid] = {
                    'trip_info': row,
                    'places': []
                }
            trips[tid]['places'].append(row)
            
    print(f"Found {len(trips)} unique trips to import.")
    
    trip_insert_query = """
    INSERT INTO trip_experiences 
    (user_id, origin, destination, trip_date, age, companion_type, has_children, interests, cuisine_preferences, stay_name, stay_price, stay_rating, total_expense)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING trip_id
    """
    
    place_insert_query = """
    INSERT INTO places_visited 
    (trip_id, place_order, place_name, place_rating, entry_fee, distance_from_prev, travel_method, travel_cost, travel_rating, experience_review)
    VALUES %s
    """
    
    places_to_insert = []
    
    count = 0
    for old_tid, data in trips.items():
        t = data['trip_info']
        c.execute(trip_insert_query, (
            user_id, t['origin'], t['destination'], t['trip_date'], int(t['age']), t['companion_type'], 
            t['has_children'] == 'True', t['interests'], t['cuisine_preferences'], t['stay_name'], 
            float(t['stay_price']), float(t['stay_rating']), float(t['total_expense'])
        ))
        new_trip_id = c.fetchone()[0]
        
        for i, p in enumerate(data['places']):
            places_to_insert.append((
                new_trip_id, i+1, p['place_name'], float(p['place_rating']), float(p['entry_fee']),
                float(p['distance_from_prev']), p['travel_method'], float(p['travel_cost']), 
                float(p['travel_rating']), p['experience_review']
            ))
            
        count += 1
        if count % 1000 == 0:
            execute_values(c, place_insert_query, places_to_insert)
            places_to_insert = []
            conn.commit()
            print(f"Inserted {count} trips...")
            
    if places_to_insert:
        execute_values(c, place_insert_query, places_to_insert)
        conn.commit()
        
    print("Dataset imported successfully!")
    c.close()
    conn.close()

if __name__ == '__main__':
    import_csv()
