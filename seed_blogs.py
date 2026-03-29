import database
import datetime
import random

def seed_blogs():
    conn = database.get_db_connection()
    c = conn.cursor()

    # Clear old blogs first safely to prevent dupes
    c.execute("DELETE FROM blogs")

    authors = [
        ('Arjun Varma', 'arjun@example.com'),
        ('Anjali Krishna', 'anjali@example.com'),
        ('Ajun Prashanth', 'ajun@example.com'),
        ('Kailash Kumar', 'kailash@example.com'),
        ('Abhishek Prabhakaran', 'abhishek@example.com')
    ]
    
    author_ids = []
    
    for name, email in authors:
        c.execute("SELECT user_id FROM users WHERE email=%s", (email,))
        user = c.fetchone()
        if not user:
            c.execute("""
                INSERT INTO users (full_name, email, password_hash) 
                VALUES (%s, %s, 'dummyhash') 
                RETURNING user_id
            """, (name, email))
            user_id = c.fetchone()[0]
        else:
            user_id = user[0]
        author_ids.append(user_id)
    
    conn.commit()

    all_users = author_ids

    blogs = [
        {
            "title": "Backwaters & Beyond: A Perfect Kerala Itinerary",
            "short_description": "Explore Kerala’s beauty with a simple day-by-day travel plan covering backwaters, beaches, and culture.",
            "content": "If you are dreaming of lush greenery, peaceful houseboat rides, and golden beaches, Kerala is exactly where you need to go. But piecing together a trip across different cities can quickly get confusing. Rather than endlessly scrolling through search results, a solid day-by-day plan makes everything effortless.\n\nFinding the Balance\nThe secret to a perfect Kerala trip is balance. You don't want to rush. Use your itinerary builder to space out your days. Dedicate your first two days to the heritage of Fort Kochi, absorbing the art and the iconic Chinese fishing nets. Then, let the app calculate the best route down to the backwaters of Alleppey.\n\nSmart Budgeting for Students\nWe know how fast travel expenses add up, especially when you're a student. The great thing about using an itinerary generator is the built-in budget tracking. You can tell the app you are on a 'moderate' or 'relaxed' budget, and it will prioritize affordable homestays, cheap local ferries, and free cultural sights over expensive tourist traps.\n\nLet AI Handle the Logistics\nNot sure how to get from the hills of Munnar down to the beaches of Varkala? The spatial optimization feature analyzes travel times and distances for you. It automatically suggests whether a bus or a shared taxi is the smartest financial choice for your route.\n\nKerala is breathtaking, and planning your trip shouldn't take away from the magic. Enter your constraints into the dashboard, grab your generated plan, and get ready to experience the backwaters like never before.",
            "category": "General",
            "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&h=600",
            "comments": ["This was so helpful for my trip next week!", "Loved the budget tracking tip."]
        },
        {
            "title": "48 Hours in Kochi: What to See & Do",
            "short_description": "Short on time? Here’s a compact itinerary to experience the best of Kochi in just 2 days.",
            "content": "Kochi is the perfect mix of old-world charm and modern energy. If you only have a weekend to spare, you might be worried about missing out. Luckily, 48 hours is plenty of time to capture the essence of the city if you optimize your route.\n\nDay 1: Heritage and Sunsets\nStart your morning in Fort Kochi. Wander the cobblestone streets, grab a coffee at a trendy art cafe, and explore the Jewish Synagogue. Instead of guessing where to go next, rely on community recommendations. Your dashboard can instantly pull up the highest-rated local lunch spots so you don't fall for overpriced tourist restaurants. End the day watching the sunset by the Chinese fishing nets.\n\nDay 2: Culture and Shopping\nOn your second day, dive into the bustling markets of Mattancherry. It is easy to lose track of time while shopping for spices and antiques. This is where a day-wise plan saves you. By having a structured timeline, you can clearly see when you need to wrap up shopping to make it to a Kathakali dance performance in the evening.\n\nKeep Your Weekend Stress-Free\nA weekend trip means every hour counts. By generating your trip within the dashboard, you get a clean, visual timeline. You won't waste an hour figuring out bus routes because the built-in planner maps out the distances between your stops automatically. Just open your personalized Kochi itinerary and start exploring.",
            "category": "Culture",
            "image": "https://images.unsplash.com/photo-1593693397690-362cb9666723?auto=format&fit=crop&w=800&h=600",
            "comments": ["48 hours wasn't enough, but it was amazing!", "Fort Kochi is simply beautiful."]
        },
        {
            "title": "Alleppey in a Day: Houseboats & Hidden Gems",
            "short_description": "Plan a relaxing day in Alleppey with houseboat rides and local experiences.",
            "content": "Alleppey is famous worldwide for its mesmerizing backwaters. However, many travelers make the mistake of showing up without a plan, only to get overwhelmed by the sheer number of houseboat operators. When you only have one day, knowing exactly what to do makes all the difference.\n\nSecuring the Right Ride\nYou don't always need to book a luxury overnight houseboat to enjoy Alleppey. For a student budget, the state-run water taxis or a simple wooden canoe ride through the narrow canals offer an equally stunning experience. When you set your preferences in the itinerary builder, it filters out the high-ticket items and suggests the most budget-friendly ways to hit the water.\n\nExploring Beyond the Boats\nAlleppey is more than just water. There are beautiful, quiet stretches of Marari beach just a short drive away. But how do you fit both the backwaters and the beach into a single afternoon?\n\nRoute Optimization\nYour smart planner does the heavy lifting. If you add 'Beach' and 'Houseboat' to your interests, the AI automatically calculates the optimal route to minimize your travel time. It will give you a step-by-step breakdown: hitting the canals in the morning and arriving at the beach right in time for the evening breeze. No stress, no backtracking, just pure relaxation.",
            "category": "Adventure",
            "image": "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?auto=format&fit=crop&w=800&h=600",
            "comments": ["Canoe rides are definitely the way to go!"]
        },
        {
            "title": "Munnar Escape: A 3-Day Hill Station Plan",
            "short_description": "Cool weather, tea gardens, and scenic views — your perfect Munnar getaway starts here.",
            "content": "When college life gets too loud, the silent, misty hills of Munnar are the ultimate cure. A 3-day getaway is the perfect amount of time to soak in the crisp mountain air, trek through endless tea plantations, and reset your mind.\n\nDay-by-Day Mountain Magic\nMunnar’s attractions are spread far apart, which is why a disorganized trip usually results in spending half the day inside a taxi.\n- Day 1: Arrive and explore the local tea museums.\n- Day 2: Head out for a morning trek to Echo Point and Top Station.\n- Day 3: Visit the beautiful Mattupetty Dam before heading home.\n\nNavigating the Hills\nBecause the scenic spots are scattered, using the day-wise planning feature is a lifesaver. It automatically groups attractions that are close to each other into the same day. This means you spend more time taking photos and less time sitting in traffic on winding mountain roads.\n\nEat Like a Local\nFinding good, affordable food in a tourist hotspot is tough. The itinerary builder leverages community data to recommend hidden gems that serve authentic Kerala meals without breaking the bank. You can set the budget tracker to strict, ensuring your 3-day mountain escape leaves you refreshed without emptying your wallet.",
            "category": "General",
            "image": "https://images.unsplash.com/photo-1583344607753-2adcb3b58ec5?auto=format&fit=crop&w=800&h=600",
            "comments": ["The tea gardens were breathtaking.", "Perfect 3-day split, thanks!"]
        },
        {
            "title": "Budget Travel in Kerala for Students",
            "short_description": "Travel across Kerala without spending too much using smart planning tips.",
            "content": "Traveling across a vibrant state like Kerala sounds expensive, but it genuinely doesn't have to be. As students, mastering the art of budget travel opens up the world. All it takes is a mix of flexibility and some incredibly smart planning tools.\n\nDitching the Excel Sheets\nYou used to need a messy spreadsheet to keep your travel costs low. Now, the itinerary builder handles it for you. By entering your maximum spending limit, the engine scans through crowd-sourced data to build a trip that fits your wallet perfectly. It actively excludes 5-star resorts and instead points you toward safe, highly-rated hostels and homestays.\n\nTransportation Hacks\nTransportation is usually the quiet budget-killer. Should you take a bus or a train from Kochi to Trivandrum? The app’s intercity travel recommendations do the math instantly. It shows you the average cost and rating of each transport method, ensuring you never overpay for a simple commute.\n\nTrust the Community\nThe best budget spots aren't found in expensive guidebooks; they are found through other travelers. By logging your past trips and reading community reviews inside the dashboard, you gain access to the cheapest street food, free public beaches, and discounted student entry fees at museums. Traveling cheap doesn’t mean traveling poorly—it just means traveling smart!",
            "category": "Food",
            "image": "https://images.unsplash.com/photo-1605553014760-b6f120aa70ae?auto=format&fit=crop&w=800&h=600",
            "comments": ["Finally, practical advice for students!", "This app saved us so much money on transport."]
        }
    ]

    for i, b in enumerate(blogs):
        user_id = author_ids[i]
        
        # Insert Blog
        # Random days in the past month for realistic dates
        random_days = random.randint(1, 30)
        created_at = datetime.datetime.now() - datetime.timedelta(days=random_days)
        
        c.execute('''
            INSERT INTO blogs (user_id, title, content, short_description, category, created_at)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING blog_id
        ''', (user_id, b['title'], b['content'], b['short_description'], b['category'], created_at))
        blog_id = c.fetchone()[0]

        # Insert Image
        c.execute("INSERT INTO blog_images (blog_id, image_url) VALUES (%s, %s)", (blog_id, b['image']))

        # Insert Comments
        for comment_text in b['comments']:
            comment_user = random.choice(all_users)
            c.execute("INSERT INTO blog_comments (blog_id, user_id, comment_text, created_at) VALUES (%s, %s, %s, %s)", 
                      (blog_id, comment_user, comment_text, created_at + datetime.timedelta(hours=random.randint(1, 24))))
        
        # Insert Likes
        likers = random.sample(all_users, k=random.randint(1, len(all_users)))
        for liker in likers:
            c.execute("INSERT INTO blog_likes (blog_id, user_id) VALUES (%s, %s)", (blog_id, liker))

    conn.commit()
    conn.close()
    print("Successfully seeded 5 blogs into the database!")

if __name__ == '__main__':
    seed_blogs()
