from flask import render_template
from flask import Flask, redirect, url_for, request

from base64 import b64decode
from PIL.Image import open
from io import BytesIO



from PIL import Image
from numpy import load, maximum, exp, sum, apply_along_axis, argmax, array

cords = ast.literal_eval(open("cords2").read())

W0 = load("W0.npy")
W1 = load("W1.npy")
b0 = load("b0.npy")
b1 = load("b1.npy")


relu = lambda x: maximum(x, 0.)

def softmax(x):
    exps = exp(x - max(x))
    return exps / sum(exps)

#layer 2 activation
def matrix_softmax(m):
    return apply_along_axis(softmax, 0, m)

#trouble with 6 and 9
#they are only good if tilted
def predict(img):
   
    x0 = img.reshape(-1,1)
    if sum(x0) == 0:
        return "Nothing"
    x1 = W0 @ x0 + b0
    l1 = relu(x1)
    x2 = (W1 @ l1 + b1)
    l2 = softmax(x2)
    return str(argmax(l2)) 



app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template("3.html") 
    
@app.route('/neural_network/<n>')
def neural_network(n): 
    return render_template("neural_network.html", number=n) 
 
@app.route('/neural_network/predict', methods=["POST"])
def guess():
    url_value = request.form['url']

    #url_value was set by javascript to contain encoded image's bytes
    #since url's value is somerthing like:
    #data:image/png;base64,iVBORw0KGgoAAAANSU...useful bytes
    #                      ^ 
    #we don't need anythin before the marked byte i
    #it happens to be byte number 22
    nice_bytes = url_value[22: ]


    im = open(BytesIO(b64decode(nice_bytes))).convert('LA')
    x = array(im)

    #x is really weird and requires some work
    x = x.T[-1].T
    #now it's a normal 2D array

    string = str(predict(x)) 
    return redirect(string) 


@app.route('/cellular_automata/', methods=["GET"])
def cellular_automata(): 
    return render_template("cellular_automata.html") 
 
@app.route('/path_finding/', methods=["GET"])
def path_finding(): 
    return render_template("path_finding.html") 
 

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)

