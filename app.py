# app.py
from flask import Flask, request, render_template, redirect
from config import GOOGLE_DRIVE_LINK, SECRET_KEY
from database import init_db
from key_manager import get_key_for_ip, validate_key

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Khởi tạo DB khi chạy lần đầu
init_db()

@app.route("/")
def index():
    user_ip = request.remote_addr
    key = get_key_for_ip(user_ip)
    return render_template("index.html", ip=user_ip, key=key)

@app.route("/access/<key>")
def access(key):
    user_ip = request.remote_addr
    if validate_key(user_ip, key):
        return render_template("access.html", link=GOOGLE_DRIVE_LINK)
    else:
        return render_template("error.html", message="Key không hợp lệ hoặc đã hết hạn!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
