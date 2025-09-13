from flask import Flask
app = Flask(__name__)

@app.get("/health")
def health():
    return "ok", 200

@app.get("/")
def hello():
    return "Hello TallerMGF!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
