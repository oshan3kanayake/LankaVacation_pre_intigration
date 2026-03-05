from app import create_app
from extensions import db
from models import Package, Hotel

app = create_app()

packages_data = [
    {
        "title": "Sigiriya & Ancient Cities",
        "location": "Sigiriya • Polonnaruwa",
        "days": "3 Days",
        "price": "USD 180",
        "image": "images/sigiriya.jpg",
        "description": "Explore the majestic Sigiriya Rock Fortress and the ancient ruins of Polonnaruwa, stepping back in time to discover Sri Lanka's rich history."
    },
    {
        "title": "Tea-Country Retreat",
        "location": "Nuwara Eliya • Ella",
        "days": "2 Nights",
        "price": "USD 140",
        "image": "images/nuwara_ella.jpg",
        "description": "Escape to the cool, misty hills of Sri Lanka's tea country. Enjoy breathtaking views of rolling tea plantations and refreshing waterfalls."
    },
    {
        "title": "Southern Coast Escape",
        "location": "Galle • Mirissa",
        "days": "4 Days",
        "price": "USD 220",
        "image": "images/Miriissa-Beach-Sri-Lanka.jpg",
        "description": "Relax on golden sands, explore the historic Galle Fort, and embark on thrilling whale-watching adventures in the Indian Ocean."
    },
    {
        "title": "Yala Wildlife Safari",
        "location": "Yala • Tissamaharama",
        "days": "3 Days",
        "price": "USD 280",
        "image": "images/yala.jpg",
        "description": "Experience the thrill of the wild on a jeep safari through Yala National Park, home to leopards, elephants, and diverse birdlife."
    },
    {
        "title": "Kandy Cultural Tour",
        "location": "Kandy • Peradeniya",
        "days": "2 Days",
        "price": "USD 150",
        "image": "images/kandy.jpg", 
        "description": "Immerse yourself in Kandyan culture with a visit to the sacred Temple of the Tooth and the beautiful Royal Botanical Gardens."
    },
    {
        "title": "Ella Hiking Adventure",
        "location": "Ella • Bandarawela",
        "days": "2 Nights",
        "price": "USD 160",
        "image": "images/ella_thumb.jpg",
        "description": "Hike to Little Adam's Peak, marvel at the Nine Arches Bridge, and enjoy the stunning mountain scenery of the hill country."
    }
]

hotels_data = [
    {
        "name": "Heritance Kandalama",
        "location": "Dambulla",
        "price_per_night": 250.00,
        "image": "images/hotel-1.jpg",
        "description": "An architectural marvel by Geoffrey Bawa, blending seamlessly into the surrounding jungle with views of the Kandalama lake and Sigiriya rock."
    },
    {
        "name": "The Grand Hotel",
        "location": "Nuwara Eliya",
        "price_per_night": 180.00,
        "image": "images/nuwara_ella.jpg",
        "description": "Experience colonial charm and elegant luxury in the heart of Sri Lanka's 'Little England', complete with beautifully manicured gardens."
    },
    {
        "name": "Cinnamon Wild",
        "location": "Yala",
        "price_per_night": 210.00,
        "image": "images/yala.jpg",
        "description": "A unique wildlife lodge situated on the borders of Yala National Park, offering rustic luxury and frequent wildlife encounters right at your doorstep."
    },
    {
        "name": "Amangalla",
        "location": "Galle",
        "price_per_night": 450.00,
        "image": "images/galle.jpg",
        "description": "Located within the historic walls of the 17th-century Galle Fort, this heritage hotel offers timeless elegance and impeccable service."
    },
    {
        "name": "98 Acres Resort & Spa",
        "location": "Ella",
        "price_per_night": 300.00,
        "image": "images/ella_thumb.jpg",
        "description": "A stunning eco-friendly boutique hotel set on a scenic tea estate, providing breathtaking panoramic views of the Ella Gap."
    },
    {
        "name": "Water Garden Sigiriya",
        "location": "Sigiriya",
        "price_per_night": 320.00,
        "image": "images/sigiriya.jpg",
        "description": "Luxurious villas set amidst serene water gardens, offering spectacular direct views of the ancient Sigiriya Rock Fortress."
    },
    {
        "name": "Weligama Bay Marriott",
        "location": "Weligama",
        "price_per_night": 190.00,
        "image": "images/Miriissa-Beach-Sri-Lanka.jpg",
        "description": "A luxurious beachfront resort on the southern coast, perfect for surfing enthusiasts and those seeking a relaxing seaside getaway."
    },
    {
        "name": "Taj Samudra",
        "location": "Colombo",
        "price_per_night": 160.00,
        "image": "images/hotel-1.jpg",
        "description": "A premier city hotel offering refined luxury, extensive dining options, and stunning views of the Indian Ocean and the Galle Face Green."
    },
    {
        "name": "Aliya Resort and Spa",
        "location": "Habarana",
        "price_per_night": 140.00,
        "image": "images/sigiriya_thumb.jpg",
        "description": "A themed resort inspired by the majestic Sri Lankan elephant, perfectly located for exploring the ruins of the Cultural Triangle."
    }
]

with app.app_context():
    # Insert Packages
    current_packages = Package.query.count()
    if current_packages == 0:
        for p_data in packages_data:
            package = Package(**p_data)
            db.session.add(package)
        print(f"Added {len(packages_data)} packages.")
    else:
        print(f"Packages already exist ({current_packages} found). Skipping package seed.")

    # Insert Hotels
    current_hotels = Hotel.query.count()
    if current_hotels == 0:
        for h_data in hotels_data:
            hotel = Hotel(**h_data)
            db.session.add(hotel)
        print(f"Added {len(hotels_data)} hotels.")
    else:
        print(f"Hotels already exist ({current_hotels} found). Skipping hotel seed.")

    db.session.commit()
    print("Database seeding completed.")
