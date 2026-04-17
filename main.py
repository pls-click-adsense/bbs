from curl_cffi import requests
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def get_subject():
    # ターゲットURL
    url = "https://bbs.eddibb.cc/liveedge/subject.txt"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    }

    try:
        # Cloudflare突破の肝：impersonateでブラウザの通信を模倣
        res = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
        
        if res.status_code == 200:
            # えりぢはUTF-8かもしれないけど、文字化けするなら 'cp932' に変えてみて
            return res.content.decode('utf-8', errors='replace')
        else:
            return f"Cloudflareにブロックされました (Status: {res.status_code})", res.status_code
            
    except Exception as e:
        return f"エラー発生: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
