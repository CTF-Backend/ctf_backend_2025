from flask import Flask, render_template

app = Flask(__name__)

@app.route('/my-app')
def my_app():
    return render_template("my_app.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
