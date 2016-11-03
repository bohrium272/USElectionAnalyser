from flask import Flask, render_template
from os import environ
import analysis

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)