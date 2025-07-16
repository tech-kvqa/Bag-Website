from app import app, db
from models import Product, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    # Clear existing products (if needed)
    Product.query.delete()

    # Sample products
    products = [
        # Backpacks
        Product(
            name='Urban Trek Backpack',
            category='Backpacks',
            price=1499.0,
            image_url='/static/images/backpack1.png',
            description='Durable and stylish backpack for daily commute.',
            stock=20
        ),
        Product(
            name='Adventure Pro Backpack',
            category='Backpacks',
            price=1999.0,
            image_url='/static/images/backpack2.jpg',
            description='Water-resistant with laptop compartment.',
            stock=15
        ),
        Product(
            name='Compact City Backpack',
            category='Backpacks',
            price=1299.0,
            image_url='/static/images/backpack3.png',
            description='Lightweight, perfect for quick trips.',
            stock=25
        ),

        # School Bags
        Product(
            name='Junior School Bag',
            category='School Bags',
            price=899.0,
            image_url='/static/images/schoolbag1.png',
            description='Spacious bag with cartoon print.',
            stock=30
        ),
        Product(
            name='Teen Trend School Bag',
            category='School Bags',
            price=1099.0,
            image_url='/static/images/schoolbag2.png',
            description='Trendy design for high school students.',
            stock=20
        ),
        Product(
            name='ErgoFit School Backpack',
            category='School Bags',
            price=999.0,
            image_url='/static/images/schoolbag3.png',
            description='Ergonomic straps for comfort.',
            stock=18
        ),

        # Luggage
        Product(
            name='Voyager Travel Luggage',
            category='Luggage',
            price=3499.0,
            image_url='/static/images/luggage1.png',
            description='Hardshell suitcase with spinner wheels.',
            stock=10
        ),
        Product(
            name='Explorer Carry-On',
            category='Luggage',
            price=2799.0,
            image_url='/static/images/luggage2.png',
            description='Cabin size luggage, airline-approved.',
            stock=12
        ),
        Product(
            name='Classic Check-in Luggage',
            category='Luggage',
            price=3199.0,
            image_url='/static/images/luggage3.png',
            description='Large-sized suitcase with TSA lock.',
            stock=8
        ),
    ]

    db.session.bulk_save_objects(products)

    existing_admin = User.query.filter_by(email='admin@shop.com').first()
    if not existing_admin:
        admin_user = User(
            name='Admin',
            email='akanuragkumar4@gmail.com',
            password=generate_password_hash('qwerty'),
            phone='9999999999',
            address='Admin HQ',
            is_admin=True
        )
        db.session.add(admin_user)
        print("✅ Admin user created successfully.")
    else:
        print("ℹ️ Admin user already exists.")

    db.session.commit()

    print("✅ Product table seeded with demo data.")


