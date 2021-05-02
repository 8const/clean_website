from flask import render_template
import pickle
import base64
import numpy as np
import cv2
from flask import Flask, redirect, url_for, request




from PIL import Image
import base64
import io
import numpy as np

 
import os
import ast

#cords = ast.literal_eval(open("cords2").read())

W0 = np.load("W0.npy")
W1 = np.load("W1.npy")
b0 = np.load("b0.npy")
b1 = np.load("b1.npy")



relu = lambda x: np.maximum(x, 0.)

def softmax(x):
    exps = np.exp(x - np.max(x))
    return exps / np.sum(exps)

#layer 2 activation
def matrix_softmax(m):
    return np.apply_along_axis(softmax, 0, m)

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
    return str(np.argmax(l2)) 



import base64
from PIL import Image
from io import BytesIO

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


    im = Image.open(BytesIO(base64.b64decode(nice_bytes))).convert('LA')
    x = np.array(im)

    #x is really weird and requires some work
    x = x.T[-1].T
    #now it's a normal 2D array

    x = cv2.resize(x, (28,28))
    string = str(predict(x)) 
    

    return redirect(string) 


@app.route('/cellular_automata/', methods=["GET"])
def cellular_automata(): 
    return render_template("cellular_automata.html") 
 
@app.route('/path_finding/', methods=["GET"])
def path_finding(): 
    return render_template("path_finding.html") 
 

if __name__ == '__main__':
    app.run(debug=True)

