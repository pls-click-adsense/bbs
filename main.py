from curl_cffi import requests
from flask import Flask, Response
import os

app = Flask(__name__)

@app.route("/")
def get_and_convert_subject():
    # ターゲットURL
    url = "https://bbs.eddibb.cc/liveedge/subject.txt"
    headers = {"User-Agent": "Monazilla/1.00"}

    try:
        # 1. subject.txtをバイナリで取得
        res = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
        
        if res.status_code != 200:
            return f"取得失敗: {res.status_code}", res.status_code

        # 2. Shift_JIS(cp932)でデコードして日本語にする
        # これで文字化け(yezとか)が消える
        raw_text = res.content.decode('cp932', errors='replace')

        # 3. 掲示板が受け取れる「数値文字参照」形式に変換した版も作りたい場合や、
        # そのままブラウザで見れるように整形して返す
        lines = raw_text.splitlines()
        output = []
        for line in lines:
            # スレタイ部分を安全な形式にしてリスト化
            output.append(line)

        # 改行を維持したまま、きれいなテキストで表示
        final_result = "\n".join(output)
        return Response(final_result, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        return f"エラー: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
