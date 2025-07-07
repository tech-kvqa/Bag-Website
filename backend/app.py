from flask import Flask, jsonify, request
from models import *
from api.product_api import product_api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'anuragiitmadras'

db.init_app(app)
CORS(app)

app.register_blueprint(product_api)

@app.route('/')
def home():
    return ("Ecommerce website started")

@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    try:
        order = Order(
            customer_name=data['customer_name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            payment_method=data['payment_method'],
            total_amount=data['total_amount']
        )
        db.session.add(order)
        db.session.commit()

        for item in data['cart']:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product']['id'],
                product_name=item['product']['name'],
                price=item['product']['price'],
                quantity=item['quantity']
            )
            db.session.add(order_item)
        
        db.session.commit()

        return jsonify({'message': 'Order placed successfully', 'order_id': order.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 409
    
    hashed_password = generate_password_hash(data['password'])

    user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        phone=data.get('phone', ''),
        address=data.get('address', '')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    return jsonify({'message': 'Login successful', 'user': {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'address': user.address
    }})

@app.route('/orders', methods=['GET'])
def get_orders():
    user_id = request.args.get('user_id')
    orders_query = Order.query
    if user_id:
        orders_query = orders_query.filter_by(user_id=user_id)
    orders = orders_query.all()

    result = []
    for o in orders:
        items = OrderItem.query.filter_by(order_id=o.id).all()
        item_list = [
            {
                'product_name': item.product_name,
                'price': item.price,
                'quantity': item.quantity
            } for item in items
        ]
        result.append({
            'order_id': o.id,
            'total_amount': o.total_amount,
            'payment_method': o.payment_method,
            'status': o.status,
            'items': item_list
        })

    return jsonify(result)

@app.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.json
    wishlist_item = Wishlist.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).first()
    if wishlist_item:
        return jsonify({'message': 'Already in wishlist'})

    item = Wishlist(user_id=data['user_id'], product_id=data['product_id'])
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Added to wishlist'})

@app.route('/wishlist', methods=['GET'])
def get_wishlist():
    user_id = request.args.get('user_id')
    items = Wishlist.query.filter_by(user_id=user_id).all()

    result = []
    for w in items:
        product = Product.query.get(w.product_id)
        if product:
            result.append(product.to_dict())

    return jsonify(result)

@app.route('/wishlist/<int:item_id>', methods=['DELETE'])
def remove_from_wishlist(item_id):
    item = Wishlist.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Removed from wishlist'})
    return jsonify({'message': 'Item not found'}), 404

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    existing_item = CartItem.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).first()
    if existing_item:
        existing_item.quantity += data.get('quantity', 1)
    else:
        item = CartItem(user_id=data['user_id'], product_id=data['product_id'], quantity=data.get('quantity', 1))
        db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item added to cart'})

@app.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    result = []
    for c in cart_items:
        product = Product.query.get(c.product_id)
        if product:
            result.append({
                'id': c.id,
                'product': product.to_dict(),
                'quantity': c.quantity
            })
    return jsonify(result)

@app.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    user_id = request.args.get('user_id')
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared'})



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)