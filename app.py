from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Cloud Interfacing Completed Successfully at port=5000!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
