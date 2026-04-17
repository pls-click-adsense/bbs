from curl_cffi import requests
from flask import Flask, Response
import datetime
import os
import re

app = Flask(__name__)

@app.route("/")
def get_subject_with_time():
    url = "https://bbs.eddibb.cc/liveedge/subject.txt"
    headers = {"User-Agent": "Monazilla/1.00"}

    try:
        res = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
        if res.status_code != 200:
            return f"取得失敗: {res.status_code}", res.status_code

        # Shift_JISでデコード（文字化け対策）
        raw_text = res.content.decode('cp932', errors='replace')
        lines = raw_text.splitlines()
        
        output = []
        for line in lines:
            # lineの形式: 1776429641.dat<>スレタイ (レス数)
            match = re.match(r'(\d+)\.dat<>(.*)', line)
            if match:
                thread_id = int(match.group(1)) # スレID（UNIXタイムスタンプ）
                title_part = match.group(2)    # スレタイとレス数
                
                # IDを日時に変換
                dt = datetime.datetime.fromtimestamp(thread_id)
                time_str = dt.strftime('%Y/%m/%d %H:%M:%S')
                
                # 「日時 | スレタイ (レス数)」の形式に整形
                output.append(f"{time_str} | {title_part}")
            else:
                output.append(line)

        final_result = "\n".join(output)
        return Response(final_result, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        return f"エラー: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
