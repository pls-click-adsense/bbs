from curl_cffi import requests
from flask import Flask, Response
import os

app = Flask(__name__)

@app.route("/")
def get_subject():
    # ターゲットのURL
    url = "https://bbs.eddibb.cc/liveedge/subject.txt"
    
    # 掲示板にアクセスするための最小限の設定
    headers = {
        "User-Agent": "Monazilla/1.00",
    }

    try:
        # curl_cffiを使ってCloudflareのチェックをスルーする
        # impersonate="chrome120" がブラウザのふりをする魔法の言葉
        res = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
        
        if res.status_code == 200:
            # 【重要】掲示板はShift_JIS(cp932)なので、デコードして日本語にする
            decoded_data = res.content.decode('cp932', errors='replace')
            
            # ブラウザで見た時に改行がそのまま出るように text/plain で返す
            return Response(decoded_data, mimetype='text/plain')
        else:
            return f"掲示板側でエラーが発生しました (Status: {res.status_code})", res.status_code
            
    except Exception as e:
        return f"プログラムエラー: {str(e)}", 500

if __name__ == "__main__":
    # Renderのポート番号に合わせて起動
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
