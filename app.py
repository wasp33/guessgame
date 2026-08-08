"""Flask 網頁版猜數字遊戲。

只用 Flask 內建的 session 保存遊戲狀態，不使用資料庫。
"""

import os
import random

from flask import Flask, render_template, request, session

app = Flask(__name__)

# 開發環境使用固定的簡單 secret key。
# 正式環境請改用環境變數（例如 os.environ["SECRET_KEY"]），
# 不要把正式環境的 secret key 直接寫死在程式碼中。
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-please-change")

MIN_NUMBER = 1
MAX_NUMBER = 100
INVALID_INPUT_MESSAGE = f"請輸入 {MIN_NUMBER} 到 {MAX_NUMBER} 之間的整數"


def start_new_game():
    """產生新答案並將猜測次數歸零，存入 session。"""
    session["answer"] = random.randint(MIN_NUMBER, MAX_NUMBER)
    session["guess_count"] = 0
    session["is_won"] = False


def parse_guess(raw_value):
    """驗證玩家輸入的猜測值。

    回傳 (數值, 錯誤訊息) tuple：驗證成功時錯誤訊息為 None，
    驗證失敗時數值為 None。
    """
    raw_value = (raw_value or "").strip()

    if not raw_value:
        return None, INVALID_INPUT_MESSAGE

    # 只接受整數字串（含負號），避免 "3.5" 這種小數被 int() 誤判成功。
    if not (raw_value.lstrip("-").isdigit()):
        return None, INVALID_INPUT_MESSAGE

    guess = int(raw_value)

    if guess < MIN_NUMBER or guess > MAX_NUMBER:
        return None, INVALID_INPUT_MESSAGE

    return guess, None


@app.route("/")
def index():
    # 第一次造訪，或是 session 過期/被清除時，重新開一局。
    if "answer" not in session:
        start_new_game()

    return render_template(
        "index.html",
        message=None,
        message_type=None,
        guess_count=session.get("guess_count", 0),
        is_won=session.get("is_won", False),
    )


@app.route("/guess", methods=["POST"])
def guess():
    # session 沒有答案（例如過期），先開新局再請玩家重新操作。
    if "answer" not in session:
        start_new_game()
        return render_template(
            "index.html",
            message="遊戲已重新開始，請再猜一次",
            message_type="error",
            guess_count=session["guess_count"],
            is_won=False,
        )

    guess_value, error_message = parse_guess(request.form.get("guess"))

    if error_message:
        return render_template(
            "index.html",
            message=error_message,
            message_type="error",
            guess_count=session["guess_count"],
            is_won=session["is_won"],
        )

    # 有效輸入才累計次數。
    session["guess_count"] += 1
    answer = session["answer"]

    if guess_value < answer:
        message, message_type = "太小", "too_low"
    elif guess_value > answer:
        message, message_type = "太大", "too_high"
    else:
        session["is_won"] = True
        message = f"恭喜猜中了！你總共猜了 {session['guess_count']} 次"
        message_type = "success"

    return render_template(
        "index.html",
        message=message,
        message_type=message_type,
        guess_count=session["guess_count"],
        is_won=session["is_won"],
    )


@app.route("/reset", methods=["POST"])
def reset():
    start_new_game()
    return render_template(
        "index.html",
        message=None,
        message_type=None,
        guess_count=session["guess_count"],
        is_won=False,
    )


if __name__ == "__main__":
    app.run(debug=True)
