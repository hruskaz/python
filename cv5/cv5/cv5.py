
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def processRequest():
   if request.method == 'GET':    
        return 'this is static content'
       
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path

if __name__ == '__main__':
     app.run(port=8000)