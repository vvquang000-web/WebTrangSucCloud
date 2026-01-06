from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'luxury-jewelry-secret-key'  # Đổi secret key

# DANH SÁCH SẢN PHẨM (Đã thêm trường 'category')
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

# TRANG CHỦ (TÌM KIẾM + LỌC + SẮP XẾP)
@app.route('/')
def index():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    sort_by = request.args.get('sort', '')
    
    filtered_products = products

    # 1. Tìm kiếm
    if query:
        filtered_products = [p for p in filtered_products if query.lower() in p['name'].lower()]
    
    # 2. Lọc danh mục
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]

    # 3. Sắp xếp
    if sort_by == 'price_asc':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)

    cart_count = len(session.get('cart', []))
    return render_template('index.html', products=filtered_products, cart_count=cart_count, current_cat=category, current_sort=sort_by)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    cart_count = len(session.get('cart', []))
    if not product:
        return "Sản phẩm không tồn tại", 404
    
    # Gợi ý sản phẩm liên quan (cùng category)
    related = [p for p in products if p['category'] == product['category'] and p['id'] != product['id']]
    
    return render_template('detail.html', product=product, cart_count=cart_count, related_products=related[:4])

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
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

# XỬ LÝ THANH TOÁN (DEMO)
@app.route('/checkout', methods=['POST'])
def checkout():
    session.pop('cart', None) # Xóa giỏ hàng sau khi đặt
    return render_template('cart.html', cart_items=[], total_price=0, success=True)

if __name__ == '__main__':
    app.run(debug=True)