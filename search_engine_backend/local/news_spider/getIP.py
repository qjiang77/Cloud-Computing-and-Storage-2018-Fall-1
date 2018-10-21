from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def getIP():
    return request.remote_addr

if __name__ == "__main__":
	app.run("0.0.0.0", port=9000)
