import os
from flask import Flask, render_template, request, flash
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename, redirect
import numpy as np
import tensorflow as tf



UPLOAD_FOLDER = './static'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_file():
    if request.method == 'POST':
        f = request.files['file']
       # f.save(secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        predictImage(f.filename)
        val, filename = predictImage(f.filename)
        flash(val)
        flash(filename)
        return redirect('/')


def predictImage(filename):
    model = tf.keras.models.load_model("./model/my_cnn_model.h5",compile=False)

    img1 = load_img('./static/'+filename, target_size=(150, 150))

    Y = img_to_array(img1)
    X = np.expand_dims(Y, axis=0)
    val = model.predict(X)

    if val == 1:
        val="Recyclable"
    elif val == 0:
        val="Organic"
    val= str(val)
    values = [val, filename]
    return values[0], values[1]

if __name__ == '__main__':
    app.run(debug=True)