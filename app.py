from flask import Flask, render_template

app = Flask(__name__)
products = [
    {
        "id": 1,
        "name": "Nhẫn Kim Cương Solitaire",
        "price": "125.000.000 đ",
        "image": "nhan-kim-cuong.jpg"
    },
    {
        "id": 2,
        "name": "Dây Chuyền Vàng 24K",
        "price": "18.500.000 đ",
        "image": "day-chuyen-vang.jpg"
    },
    {
        "id": 3,
        "name": "Bông Tai Ngọc Trai Biển",
        "price": "8.200.000 đ",
        "image": "bong-tai-ngoc-trai.jpg"
    },
    {
        "id": 4,
        "name": "Lắc Tay Bạc Charm",
        "price": "2.500.000 đ",
        "image": "lac-tay-bac.jpg"
    },
    {
        "id": 5,
        "name": "Nhẫn Cưới Bạch Kim",
        "price": "35.000.000 đ",
        "image": "nhan-cuoi.jpg"
    },
    {
        "id": 6,
        "name": "Kiềng Vàng Phú Quý",
        "price": "45.000.000 đ",
        "image": "kieng-vang.jpg"
    },
    {
        "id": 7,
        "name": "Vòng Tay Đá Phong Thủy",
        "price": "1.200.000 đ",
        "image": "vong-tay-da.jpg"
    },
    {
        "id": 8,
        "name": "Bộ Trang Sức Ruby Đỏ",
        "price": "89.000.000 đ",
        "image": "bo-trang-suc-ruby.jpg"
    }
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)