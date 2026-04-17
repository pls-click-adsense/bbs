from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/")
def encode_everything():
    # URLのパラメータ (?text=...) から文字を受け取る。空なら説明を出す。
    input_text = request.args.get('text', "")
    
    if not input_text:
        return "URLの末尾に ?text=変換したい文字 を入れてね。"

    # 全文字スキャンして、ASCII（英数字など）以外は全部数値文字参照に変換
    # 😶 でも 🥺 でも 漢字でも、Shift_JIS外の文字はこれで掲示板に通るようになる
    encoded_text = "".join([f"&#{ord(c)};" if ord(c) > 128 else c for c in input_text])
    
    # 掲示板にコピペしやすいように、プレーンテキストで結果だけを返す
    return Response(encoded_text, mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
