from flask import Flask, jsonify, request
from models import *
from api.product_api import product_api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime

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

# @app.route('/place-order', methods=['POST'])
# def place_order():
#     data = request.json
#     try:
#         order = Order(
#             customer_name=data['customer_name'],
#             email=data['email'],
#             phone=data['phone'],
#             address=data['address'],
#             payment_method=data['payment_method'],
#             total_amount=data['total_amount']
#         )
#         db.session.add(order)
#         db.session.commit()

#         for item in data['cart']:
#             order_item = OrderItem(
#                 order_id=order.id,
#                 product_id=item['product']['id'],
#                 product_name=item['product']['name'],
#                 price=item['product']['price'],
#                 quantity=item['quantity']
#             )
#             db.session.add(order_item)
        
#         db.session.commit()

#         return jsonify({'message': 'Order placed successfully', 'order_id': order.id})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.get_json()

    required_fields = ['customer_name', 'phone', 'address', 'payment_method', 'total_amount', 'user_id']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Missing required order details.'}), 400

    user_id = data['user_id']

    # Fetch user's cart items
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty.'}), 400

    # Create Order
    new_order = Order(
        customer_name=data['customer_name'],
        email=data.get('email', ''),
        phone=data['phone'],
        address=data['address'],
        payment_method=data['payment_method'],
        total_amount=data['total_amount'],
        status='Pending',
        user_id=user_id
    )
    db.session.add(new_order)
    db.session.commit()  # Commit now to generate order.id

    # Move cart items to order items
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=cart_item.quantity
            )
            db.session.add(order_item)

    # Clear user's cart
    CartItem.query.filter_by(user_id=user_id).delete()

    db.session.commit()

    return jsonify({'message': 'Order placed successfully.', 'order_id': new_order.id}), 201

    
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

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not user_id or not product_id:
        return jsonify({'error': 'User ID and Product ID required'}), 400

    existing_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()
    return jsonify({'message': 'Item added to cart successfully'})

# @app.route('/cart', methods=['GET'])
# def get_cart():
#     user_id = request.args.get('user_id')
#     if not user_id:
#         return jsonify({'error': 'User ID required'}), 400

#     cart_items = CartItem.query.filter_by(user_id=user_id).all()
#     result = []
#     for item in cart_items:
#         product = Product.query.get(item.product_id)
#         if product:
#             result.append({
#                 'id': item.id,
#                 'product': product.to_dict(),
#                 'quantity': item.quantity
#             })

#     return jsonify(result)

@app.route('/cart')
def get_cart():
    user_id = request.args.get('user_id')
    items = CartItem.query.filter_by(user_id=user_id).all()
    cart = []
    for item in items:
        product_data = item.product.to_dict()  # Now this works
        product_data['image_url'] = f"{request.host_url.rstrip('/')}/{product_data['image_url']}"
        cart.append({
            'id': item.id,
            'quantity': item.quantity,
            'product': product_data
        })
    return jsonify(cart)


@app.route('/products/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_data = product.to_dict()
    product_data['image_url'] = f"{request.host_url.rstrip('/')}/{product_data['image_url']}"
    return jsonify(product_data)

@app.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400

    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared successfully'})



@app.route('/user-orders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()

    result = []
    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        result.append({
            'order_id': order.id,
            'order_date': order.id,
            'status': order.status,
            'total_amount': order.total_amount,
            'items': [{
                'product_name': i.product_name,
                'quantity': i.quantity,
                'price': i.price
            } for i in items]
        })

    return jsonify(result)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'address': user.address
    })

@app.route('/order-history/<int:user_id>', methods=['GET'])
def order_history(user_id):
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()
    if not orders:
        return jsonify({'message': 'No past orders found.'}), 200

    order_list = []
    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        item_list = [
            {
                'product_name': item.product_name,
                'price': item.price,
                'quantity': item.quantity
            } for item in items
        ]

        order_list.append({
            'order_id': order.id,
            'customer_name': order.customer_name,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_on': order.id,  # if you have created_at column, use it
            'items': item_list
        })

    return jsonify(order_list), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)