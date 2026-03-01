from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from PIL import Image
from flask_executor import Executor
import keras
import numpy as np

app = Flask(__name__)

executor = Executor(app)

app.config['UPLOAD'] ='static/uploads'
img_path = 'static/uploads'
os.makedirs("static/prediction_model", exist_ok=True)
os.makedirs(img_path, exist_ok=True)
os.makedirs(img_path.replace("uploads", "predictions"), exist_ok=True)

@app.route("/", methods=['GET','POST'])
def upload_image():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        img = os.path.join(img_path, filename)
        file.save(img)
        executor.submit(prediction, img)
        return redirect(url_for('display_prediction', img=img))
    

@app.route('/prediction', methods=['GET', 'POST'])
def prediction(img):
    model = keras.saving.load_model(
        'static/prediction_model/model.keras')
    with Image.open(img) as im:
        arr = np.asarray(im.resize((224,224)))
    pred = model.predict(arr[np.newaxis,:,:,:])
    result = round(pred.item()*100, 1)
    pred_path = os.path.splitext(img.replace("uploads", "predictions"))[0] + '.txt'
    with open(pred_path, "w") as fp:
        fp.write(f"Cancerous lesion: {result:.1f}% probability.")
    return redirect(url_for('display_prediction', img=img))
    
@app.route('/display_prediction', methods=['GET', 'POST'])
def display_prediction():
    img = request.args.get('img')
    pred_path = os.path.splitext(img.replace("uploads", "predictions"))[0] + '.txt'
    if os.path.exists(pred_path):
        with open(pred_path, "r") as fp:
            result = fp.readlines()
    else:
        result = 'Prediction in progress...'
    return render_template('/result.html', img=img, result=result)


if __name__ == '__main__':

    app.run(host = '0.0.0.0', port=5000)