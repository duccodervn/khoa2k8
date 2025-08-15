# key_manager.py
import time
import uuid
from database import get_connection
from config import KEY_EXPIRE_SECONDS

def get_key_for_ip(ip):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT key, expire_at FROM keys WHERE ip=?", (ip,))
    row = c.fetchone()

    now = int(time.time())

    if row:
        key, expire_at = row
        if expire_at > now:  # Còn hạn
            conn.close()
            return key
        else:
            # Hết hạn -> tạo key mới
            new_key = str(uuid.uuid4())
            expire_at = now + KEY_EXPIRE_SECONDS
            c.execute("UPDATE keys SET key=?, expire_at=? WHERE ip=?", (new_key, expire_at, ip))
            conn.commit()
            conn.close()
            return new_key
    else:
        # Chưa có key -> tạo mới
        new_key = str(uuid.uuid4())
        expire_at = now + KEY_EXPIRE_SECONDS
        c.execute("INSERT INTO keys (ip, key, expire_at) VALUES (?, ?, ?)", (ip, new_key, expire_at))
        conn.commit()
        conn.close()
        return new_key

def validate_key(ip, key):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT key, expire_at FROM keys WHERE ip=?", (ip,))
    row = c.fetchone()
    conn.close()

    if not row:
        return False

    stored_key, expire_at = row
    now = int(time.time())
    return stored_key == key and expire_at > now
