import urllib.parse # Thư viện xử lý chuỗi kết nối
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'luxury-jewelry-secret-key'

# --- CẤU HÌNH KẾT NỐI AZURE SQL DATABASE ---
server = 'vvquang.database.windows.net'  
database = 'luxury-db'                            
username = 'vuvanquang'                          
password = 'quangvu894#'                       

# Tạo chuỗi kết nối an toàn
driver = '{ODBC Driver 18 for SQL Server}'
connection_string = f'Driver={driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
params = urllib.parse.quote_plus(connection_string)

# Gán vào Flask
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc:///?odbc_connect={params}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# -------------------------------------------

# CẤU HÌNH LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# MODEL USER (Bảng người dùng trong DB)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# TẠO DATABASE (Tự động tạo bảng trên Azure nếu chưa có)
with app.app_context():
    try:
        db.create_all()
        print("Đã kết nối và tạo bảng trên Azure SQL thành công!")
    except Exception as e:
        print("Lỗi kết nối Database:", e)

# --- DỮ LIỆU SẢN PHẨM ---
products = [
    {"id": 1, "name": "Nhẫn Kim Cương Solitaire", "price": 125000000, "image": "nhan-kim-cuong.jpg", "category": "ring", "desc": "Kim cương tự nhiên 5 ly, nước D, độ sạch VVS1."},
    {"id": 2, "name": "Dây Chuyền Vàng 24K", "price": 18500000, "image": "day-chuyen-vang.jpg", "category": "necklace", "desc": "Vàng 9999, chế tác thủ công tinh xảo."},
    {"id": 3, "name": "Bông Tai Ngọc Trai Biển", "price": 8200000, "image": "bong-tai-ngoc-trai.jpg", "category": "earring", "desc": "Ngọc trai Akoya Nhật Bản, ánh hồng tự nhiên."},
    {"id": 4, "name": "Lắc Tay Bạc Charm", "price": 2500000, "image": "lac-tay-bac.jpg", "category": "bracelet", "desc": "Bạc Ý 925 cao cấp, mix charm phong thủy."},
    {"id": 5, "name": "Nhẫn Cưới Bạch Kim", "price": 35000000, "image": "nhan-cuoi.png", "category": "ring", "desc": "Bạch kim Platin 950, đính kim cương tấm."},
    {"id": 6, "name": "Kiềng Vàng Phú Quý", "price": 45000000, "image": "kieng-vang.jpg", "category": "necklace", "desc": "Thiết kế rồng phượng, phù hợp làm của hồi môn."},
    {"id": 7, "name": "Vòng Tay Đá Phong Thủy", "price": 1200000, "image": "vong-tay-da.jpg", "category": "bracelet", "desc": "Đá thạch anh tóc vàng tự nhiên 100%."},
    {"id": 8, "name": "Bộ Trang Sức Ruby Đỏ", "price": 89000000, "image": "bo-trang-suc-ruby.jpg", "category": "set", "desc": "Ruby huyết bồ câu, thiết kế sang trọng đẳng cấp."}
]

@app.template_filter()
def format_currency(value):
    return "{:,.0f} đ".format(value).replace(",", ".")

# --- ROUTES AUTHENTICATION (ĐĂNG KÝ/ĐĂNG NHẬP) ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Kiểm tra tồn tại
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email đã tồn tại!', 'danger')
            return redirect(url_for('register'))
        
        # Mã hóa mật khẩu và lưu
        new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Sai email hoặc mật khẩu.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Demo logic: Thực tế cần SMTP Server để gửi email
        email = request.form['email']
        flash(f'Yêu cầu đã nhận! Một email đặt lại mật khẩu đã được gửi tới {email}', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

# --- ROUTES CHÍNH ---

@app.route('/')
def index():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    sort_by = request.args.get('sort', '')
    
    filtered_products = products
    if query: filtered_products = [p for p in filtered_products if query.lower() in p['name'].lower()]
    if category: filtered_products = [p for p in filtered_products if p['category'] == category]
    if sort_by == 'price_asc': filtered_products = sorted(filtered_products, key=lambda x: x['price'])
    elif sort_by == 'price_desc': filtered_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)

    cart_count = len(session.get('cart', []))
    return render_template('index.html', products=filtered_products, cart_count=cart_count, current_cat=category, current_sort=sort_by)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    cart_count = len(session.get('cart', []))
    if not product: return "Lỗi", 404
    related = [p for p in products if p['category'] == product['category'] and p['id'] != product['id']]
    return render_template('detail.html', product=product, cart_count=cart_count, related_products=related[:4])

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session: session['cart'] = []
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        session['cart'].append(product)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    cart_items = session.get('cart', [])
    if 0 <= index < len(cart_items):
        cart_items.pop(index)
        session['cart'] = cart_items
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@login_required # Yêu cầu đăng nhập mới được thanh toán
def checkout():
    session.pop('cart', None)
    return render_template('cart.html', cart_items=[], total_price=0, success=True)

if __name__ == '__main__':
    app.run(debug=True)