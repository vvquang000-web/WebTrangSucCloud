from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'vu-van-quang-secret-key'  # Bắt buộc có để dùng Giỏ hàng (Session)

# DANH SÁCH SẢN PHẨM (Giá đã đổi thành số nguyên để tính toán)
products = [
    {"id": 1, "name": "Nhẫn Kim Cương Solitaire", "price": 125000000, "image": "nhan-kim-cuong.jpg", "desc": "Kim cương tự nhiên 5 ly, nước D, độ sạch VVS1."},
    {"id": 2, "name": "Dây Chuyền Vàng 24K", "price": 18500000, "image": "day-chuyen-vang.jpg", "desc": "Vàng 9999, chế tác thủ công tinh xảo."},
    {"id": 3, "name": "Bông Tai Ngọc Trai Biển", "price": 8200000, "image": "bong-tai-ngoc-trai.jpg", "desc": "Ngọc trai Akoya Nhật Bản, ánh hồng tự nhiên."},
    {"id": 4, "name": "Lắc Tay Bạc Charm", "price": 2500000, "image": "lac-tay-bac.jpg", "desc": "Bạc Ý 925 cao cấp, mix charm phong thủy."},
    {"id": 5, "name": "Nhẫn Cưới Bạch Kim", "price": 35000000, "image": "nhan-cuoi.jpg", "desc": "Bạch kim Platin 950, đính kim cương tấm."},
    {"id": 6, "name": "Kiềng Vàng Phú Quý", "price": 45000000, "image": "kieng-vang.jpg", "desc": "Thiết kế rồng phượng, phù hợp làm của hồi môn."},
    {"id": 7, "name": "Vòng Tay Đá Phong Thủy", "price": 1200000, "image": "vong-tay-da.jpg", "desc": "Đá thạch anh tóc vàng tự nhiên 100%."},
    {"id": 8, "name": "Bộ Trang Sức Ruby Đỏ", "price": 89000000, "image": "bo-trang-suc-ruby.jpg", "desc": "Ruby huyết bồ câu, thiết kế sang trọng đẳng cấp."}
]

# Hàm hỗ trợ định dạng tiền tệ (Ví dụ: 100000 -> 100,000 đ)
@app.template_filter()
def format_currency(value):
    return "{:,.0f} đ".format(value).replace(",", ".")

# 1. TRANG CHỦ & TÌM KIẾM
@app.route('/')
def index():
    query = request.args.get('q')
    cart_count = len(session.get('cart', [])) # Đếm số món trong giỏ
    
    if query:
        filtered_products = [p for p in products if query.lower() in p['name'].lower()]
    else:
        filtered_products = products
        
    return render_template('index.html', products=filtered_products, cart_count=cart_count)

# 2. TRANG CHI TIẾT SẢN PHẨM
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    cart_count = len(session.get('cart', []))
    if not product:
        return "Sản phẩm không tồn tại", 404
    return render_template('detail.html', product=product, cart_count=cart_count)

# 3. THÊM VÀO GIỎ HÀNG
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    # Tìm thông tin sản phẩm
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        session['cart'].append(product)
        session.modified = True
    
    return redirect(url_for('cart'))

# 4. XEM GIỎ HÀNG & TÍNH TỔNG
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# 5. XÓA KHỎI GIỎ HÀNG
@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    cart_items = session.get('cart', [])
    if 0 <= index < len(cart_items):
        cart_items.pop(index)
        session['cart'] = cart_items
        session.modified = True
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)