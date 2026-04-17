from curl_cffi import requests
from flask import Flask, Response
import datetime
import os
import re

app = Flask(__name__)

# 日本時間（UTC+9）に補正するための関数
def to_jst(timestamp):
    dt_utc = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    dt_jst = dt_utc + datetime.timedelta(hours=9)
    return dt_jst.strftime('%Y/%m/%d %H:%M:%S')

# ASCII以外（絵文字や日本語）をすべて数値文字参照に変換する関数
def encode_to_entities(text):
    return "".join([f"&#{ord(c)};" if ord(c) > 128 else c for c in text])

@app.route("/")
def get_clean_subject():
    url = "https://bbs.eddibb.cc/liveedge/subject.txt"
    headers = {"User-Agent": "Monazilla/1.00"}

    try:
        res = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
        if res.status_code != 200:
            return f"取得失敗: {res.status_code}", res.status_code

        # 1. まずShift_JISで安全にデコード
        raw_text = res.content.decode('cp932', errors='replace')
        lines = raw_text.splitlines()
        
        output = []
        for line in lines:
            # 形式: 1776429641.dat<>スレタイ (レス数)
            match = re.match(r'(\d+)\.dat<>(.*)', line)
            if match:
                thread_id = int(match.group(1))
                title_part = match.group(2)
                
                # 2. 時間を日本時間に直す
                time_jst = to_jst(thread_id)
                
                # 3. スレタイ内の絵文字や文字化け残骸を、掲示板が解釈できる数値文字参照に変換
                safe_title = encode_to_entities(title_part)
                
                output.append(f"{time_jst} | {safe_title}")
            else:
                output.append(line)

        final_result = "\n".join(output)
        # 掲示板にそのままコピペしても機能する形式で返す
        return Response(final_result, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        return f"エラー: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
