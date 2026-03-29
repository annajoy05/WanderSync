import database
import json

def seed():
    conn = database.get_db_connection()
    c = conn.cursor()
    user_id = 11

    # 1. Munnar Heritage - Accessibility Focus
    c.execute('''
        INSERT INTO trip_experiences 
        (user_id, origin, destination, trip_date, age, companion_type, has_children, interests, cuisine_preferences, trip_duration, main_transport, travel_style, stay_name, stay_price, stay_rating, total_expense, accessibility_notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING trip_id
    ''', (
        user_id, 'Cochin', 'Munnar', '2024-03-15', 28, 'Partner', False,
        'Nature, Photography', 'South Indian', 3, 'Car', 'Relaxed',
        'Tea County Resort', 4500.0, 4.5, 15000.0,
        "Excellent wheelchair access to viewpoints. The Tea Museum has ramps and wide corridors. Eravikulam National Park has an accessible bus for the safari."
    ))
    trip1_id = c.fetchone()[0]
    
    places1 = [
        (trip1_id, 0, 'Tea Museum', 4.8, 100, 5, 'Car', 200, 5, 'Must visit! Ramps are well maintained.'),
        (trip1_id, 1, 'Mattupetty Dam', 4.5, 20, 12, 'Car', 300, 4, 'Breathtaking views. Paved walkways are great for accessibility.')
    ]
    for p in places1:
        c.execute('INSERT INTO places_visited (trip_id, place_order, place_name, place_rating, entry_fee, distance_from_prev, travel_method, travel_cost, travel_rating, experience_review) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', p)

    # 2. Cochin Cultural - Guide Focus
    c.execute('''
        INSERT INTO trip_experiences 
        (user_id, origin, destination, trip_date, age, companion_type, has_children, interests, cuisine_preferences, trip_duration, main_transport, travel_style, stay_name, stay_price, stay_rating, total_expense, guide_name, guide_phone, guide_specialty, accessibility_notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING trip_id
    ''', (
        user_id, 'Bangalore', 'Fort Kochi', '2024-02-10', 30, 'Solo', False,
        'History, Art', 'Seafood', 2, 'Walking', 'Cultural',
        'Brunton Boatyard', 8000.0, 4.9, 20000.0,
        "Siddharth S.", "+91 94470 54321", "Colonial History",
        "Fort Kochi is mostly walkable but streets are uneven. Suggest using a rickshaw for longer heritage stretches. Good signage for landmarks."
    ))
    trip2_id = c.fetchone()[0]
    
    places2 = [
        (trip2_id, 0, 'Chinese Fishing Nets', 4.7, 0, 0, 'Walk', 0, 5, 'Iconic. Guide Siddharth explained the mechanism perfectly.'),
        (trip2_id, 1, 'Jewish Synagogue', 4.9, 10, 2, 'Rickshaw', 50, 4, 'Very historic. Note: photography not allowed inside.')
    ]
    for p in places2:
        c.execute('INSERT INTO places_visited (trip_id, place_order, place_name, place_rating, entry_fee, distance_from_prev, travel_method, travel_cost, travel_rating, experience_review) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', p)

    # 3. Alleppey Backwaters
    c.execute('''
        INSERT INTO trip_experiences 
        (user_id, origin, destination, trip_date, age, companion_type, has_children, interests, cuisine_preferences, trip_duration, main_transport, travel_style, stay_name, stay_price, stay_rating, total_expense, accessibility_notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING trip_id
    ''', (
        user_id, 'Kottayam', 'Alleppey', '2024-01-20', 32, 'Family', True,
        'Relaxing', 'Traditional Kerala', 1, 'Boat', 'Luxurious',
        'Rainbow Houseboats', 12000.0, 4.7, 15000.0,
        "Most houseboats require a step-up for boarding. Request a ramp-equipped boat in advance. Path to the jetty is narrow but flat."
    ))
    trip3_id = c.fetchone()[0]
    
    places3 = [
        (trip3_id, 0, 'Vembanad Lake', 5.0, 0, 0, 'Houseboat', 0, 5, 'The height of peace. Very kid friendly.')
    ]
    for p in places3:
        c.execute('INSERT INTO places_visited (trip_id, place_order, place_name, place_rating, entry_fee, distance_from_prev, travel_method, travel_cost, travel_rating, experience_review) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', p)

    conn.commit()
    conn.close()
    print("Dummy trip data seeded successfully for Anamika (User ID: 11)")

if __name__ == '__main__':
    seed()
