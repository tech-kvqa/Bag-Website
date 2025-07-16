from flask import Flask, jsonify, request, send_file
from models import *
from api.product_api import product_api
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_cors import CORS
from datetime import datetime
import os
from flask_socketio import SocketIO, emit
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from flask import make_response
from io import BytesIO

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'anuragiitmadras'

db.init_app(app)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

app.register_blueprint(product_api)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return ("Ecommerce website started")

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
    db.session.commit()  # Commit to get order ID

    low_stock_alerts = []

    # Move cart items to order items and reduce stock
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            if product.stock < cart_item.quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400

            product.stock -= cart_item.quantity

            # Check for low stock
            if product.stock < 5:
                low_stock_alerts.append(product)

            # Add to OrderItems
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=cart_item.quantity
            )
            db.session.add(order_item)

    # Save and emit low stock notifications
    for product in low_stock_alerts:
        message = f"⚠️ Stock for '{product.name}' is low (only {product.stock} left)."
        notification = Notification(message=message, is_read=False)
        db.session.add(notification)
        socketio.emit('low_stock_alert', {
            'product_name': product.name,
            'stock': product.stock
        }, namespace='/admin')


    # Clear cart
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

# @app.route('/wishlist/<int:item_id>', methods=['DELETE'])
# def remove_from_wishlist(item_id):
#     item = Wishlist.query.get(item_id)
#     if item:
#         db.session.delete(item)
#         db.session.commit()
#         return jsonify({'message': 'Removed from wishlist'})
#     return jsonify({'message': 'Item not found'}), 404

@app.route('/wishlist/delete', methods=['DELETE'])
def delete_from_wishlist():
    user_id = request.args.get('user_id')
    product_id = request.args.get('product_id')
    if not user_id or not product_id:
        return jsonify({'error': 'User ID and Product ID required'}), 400

    item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Removed from wishlist'})


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

@app.route('/cart', methods=['GET'])
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

@app.route('/cart/<int:item_id>', methods=['DELETE'])
def remove_cart_item(item_id):
    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'})


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

# @app.route('/order-history/<int:user_id>', methods=['GET'])
# def order_history(user_id):
#     orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()
#     if not orders:
#         return jsonify({'message': 'No past orders found.'}), 200

#     order_list = []
#     for order in orders:
#         items = OrderItem.query.filter_by(order_id=order.id).all()
#         item_list = [
#             {
#                 'product_name': item.product_name,
#                 'price': item.price,
#                 'quantity': item.quantity
#             } for item in items
#         ]

#         order_list.append({
#             'order_id': order.id,
#             'customer_name': order.customer_name,
#             'total_amount': order.total_amount,
#             'status': order.status,
#             'created_on': order.id,  # if you have created_at column, use it
#             'items': item_list
#         })

#     return jsonify(order_list), 200


@app.route('/order-history/<int:user_id>', methods=['GET'])
def order_history(user_id):
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    history = []

    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        history.append({
            'order_id': order.id,
            'customer_name': order.customer_name,
            'total_amount': order.total_amount,
            'status': order.status,
            'tracking_status': order.tracking_status or 'Processed',
            'tracking_id': order.tracking_id or '',
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'items': [ 
                {
                    'product_name': item.product_name,
                    'quantity': item.quantity,
                    'price': item.price
                } for item in items
            ]
        })
    return jsonify(history), 200


########################################### Admin Routes #############################################

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    user = User.query.filter_by(email=data['email'], is_admin=True).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid admin credentials'}), 401

    return jsonify({
        'message': 'Admin login successful',
        'admin': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    })

# Get all products (for admin)
@app.route('/admin/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@app.route('/admin/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict()), 200


# Add a new product
@app.route('/admin/add-product', methods=['POST'])
def add_product():
    print("Incoming form data:", request.form)
    print("Incoming files:", request.files)

    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    stock = request.form.get('stock')
    category = request.form.get('category')
    file = request.files.get('image')

    if not all([name, description, price, stock, category]) or not file or file.filename == '':
        print("Missing required fields.")
        return jsonify({'error': 'Missing required fields'}), 400

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid image format'}), 400

    # Save image to static/images/
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.root_path, 'static/images', filename)
    file.save(file_path)

    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category=category,
        image_url=f'/static/images/{filename}'
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'})


# Update a product
@app.route('/admin/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product.name = request.form.get('name')
    product.description = request.form.get('description')
    product.price = request.form.get('price')
    product.stock = request.form.get('stock')
    product.category = request.form.get('category')

    # Handle optional image replacement
    image_file = request.files.get('image')
    if image_file:
        image_path = f'/static/images/{image_file.filename}'
        image_file.save(image_path)
        product.image_url = image_path

    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200


# Delete a product
@app.route('/admin/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.order_by(Order.id.desc()).all()
    result = []
    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        item_list = [{
            'product_name': item.product_name,
            'price': item.price,
            'quantity': item.quantity
        } for item in items]

        result.append({
            'id': order.id,
            'customer_name': order.customer_name,
            'total_amount': order.total_amount,
            'status': order.status,
            'tracking_status': order.tracking_status or 'Processed',
            'tracking_id': order.tracking_id or '',
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'items': item_list
        })

    return jsonify(result), 200

# @app.route('/admin/orders/<int:order_id>', methods=['PUT'])
# def update_order_status(order_id):
#     order = Order.query.get_or_404(order_id)
#     data = request.json
#     order.status = data.get('status', order.status)
#     db.session.commit()
#     return jsonify({'message': 'Order status updated successfully'}), 200

# @app.route('/admin/users', methods=['GET'])
# def get_users():
#     users = User.query.filter_by(is_admin=False).all()
#     user_list = [{
#         "id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "phone": user.phone,
#         "address": user.address
#     } for user in users]
#     return jsonify(user_list), 200


# @app.route('/admin/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get_or_404(user_id)

#     if user.is_admin:
#         return jsonify({'error': 'Cannot delete admin user'}), 400

#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/admin/users', methods=['GET'])
def get_all_users():
    users = User.query.filter_by(is_admin=False).all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'phone': u.phone,
        'address': u.address
    } for u in users]), 200

@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        return jsonify({'error': 'Cannot delete admin'}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    total_users = User.query.filter_by(is_admin=False).count()
    total_orders = Order.query.count()
    total_products = Product.query.count()
    return jsonify({
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products
    }), 200

@app.route('/admin/low-stock-products', methods=['GET'])
def get_low_stock_products():
    threshold = 5  # Change if needed
    products = Product.query.filter(Product.stock < threshold).all()
    return jsonify([p.to_dict() for p in products]), 200

@app.route('/admin/notifications', methods=['GET'])
def get_admin_notifications():
    notifications = Notification.query.filter_by(is_read=False).order_by(Notification.created_at.desc()).all()
    return jsonify([
        {
            'id': n.id,
            'message': n.message,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
            'read': n.is_read
        } for n in notifications
    ]), 200

@app.route('/admin/notifications/read', methods=['POST'])
def mark_notifications_as_read():
    Notification.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'message': 'All notifications marked as read'}), 200

@app.route('/admin/order/<int:order_id>/invoice', methods=['GET'])
def generate_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    items = OrderItem.query.filter_by(order_id=order.id).all()

    # Prepare PDF in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"🧾 Invoice for Order #{order.id}")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Customer: {order.customer_name}")
    y -= 20
    c.drawString(50, y, f"Email: {order.email or 'N/A'}")
    y -= 20
    c.drawString(50, y, f"Phone: {order.phone}")
    y -= 20
    c.drawString(50, y, f"Address: {order.address}")
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Items")
    y -= 20

    c.setFont("Helvetica", 12)
    for item in items:
        line = f"{item.product_name} (x{item.quantity}) - INR {item.price * item.quantity:.2f}"
        c.drawString(50, y, line)
        y -= 18
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total: INR {order.total_amount:.2f}")
    y -= 20
    c.drawString(50, y, f"Status: {order.status}")
    y -= 20

    c.showPage()
    c.save()
    buffer.seek(0)

    # Check if preview requested
    preview = request.args.get('preview')
    if preview == 'true':
        return send_file(buffer, as_attachment=False, mimetype='application/pdf')
    else:
        return send_file(buffer,
                         as_attachment=True,
                         download_name=f'invoice_order_{order_id}.pdf',
                         mimetype='application/pdf')
    
@app.route('/admin/orders/<int:order_id>/tracking', methods=['PUT'])
def update_tracking(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    order.tracking_status = data.get('tracking_status', order.tracking_status)
    order.tracking_id = data.get('tracking_id', order.tracking_id)
    db.session.commit()
    return jsonify({'message': 'Tracking updated successfully'})


@app.route('/admin/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)

    order.status = data.get('status', order.status)
    order.tracking_status = data.get('tracking_status', order.tracking_status)
    order.tracking_id = data.get('tracking_id', order.tracking_id)

    db.session.commit()
    return jsonify({'message': 'Order updated successfully.'}), 200

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

with app.app_context():
    db.create_all()

socketio_app = socketio  # Gunicorn entry point
# gunicorn -k eventlet -w 1 wsgi:socketio
