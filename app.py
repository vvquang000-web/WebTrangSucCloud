from flask import Flask, render_template

app = Flask(__name__)

# Danh sách sản phẩm (Data giả lập)
# Link ảnh lấy từ internet để web nhẹ và hiển thị luôn
products = [
    {"id": 1, "name": "Nhẫn Kim Cương Solitaire", "price": "125.000.000 ₫", "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=400&q=80", "category": "Nhẫn"},
    {"id": 2, "name": "Dây Chuyền Vàng 24K", "price": "18.500.000 ₫", "image": "https://images.unsplash.com/photo-1599643478518-17488fbbcd75?auto=format&fit=crop&w=400&q=80", "category": "Dây Chuyền"},
    {"id": 3, "name": "Bông Tai Ngọc Trai Biển", "price": "8.200.000 ₫", "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=400&q=80", "category": "Bông Tai"},
    {"id": 4, "name": "Lắc Tay Bạc Charm", "price": "2.500.000 ₫", "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&w=400&q=80", "category": "Lắc Tay"},
    {"id": 5, "name": "Nhẫn Cưới Platinum", "price": "45.000.000 ₫", "image": "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=400&q=80", "category": "Nhẫn"},
    {"id": 6, "name": "Đồng Hồ Đính Đá", "price": "85.900.000 ₫", "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=400&q=80", "category": "Đồng Hồ"},
    {"id": 7, "name": "Vòng Cổ Ruby Đỏ", "price": "62.000.000 ₫", "image": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=400&q=80", "category": "Dây Chuyền"},
    {"id": 8, "name": "Bộ Trang Sức Sapphire", "price": "110.000.000 ₫", "image": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?auto=format&fit=crop&w=400&q=80", "category": "Bộ Sưu Tập"},
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run()