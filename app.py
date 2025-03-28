from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'),host="0.0.0.0")