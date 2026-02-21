from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
os.environ["KERAS_BACKEND"] = "torch"
from PIL import Image
from flask_executor import Executor
import torch
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
    label_to_name = {
    0: 'Actinic keratoses',
    1: 'Basal cell carcinoma',
    2: 'Benign keratosis-like lesions',
    3: 'Dermatofibroma',
    4: 'Melanoma',
    5: 'Melanocytic nevi',
    6: 'Vascular lesions'
    }       
    model = torch.load('static/prediction_model/model.pth', weights_only=False)
    with Image.open(img) as im:
        arr = np.asarray(im.resize((224,224)))
    pred = model.predict(arr[np.newaxis,:,:,:])
    result_dict = {k:v.item()*100 for k,v in zip(list(label_to_name.values()), list(pred.ravel()))}
    result_dict = dict(sorted(result_dict.items(), key=lambda x:x[1], reverse=True))
    result = {k:v for k,v in list(result_dict.items())[:3]}
    pred_path = os.path.splitext(img.replace("uploads", "predictions"))[0] + '.txt'
    with open(pred_path, "w") as fp:
        for k,v in result.items():
            fp.write(f"{k}: {v:.2f}%")
            fp.write("\n")
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
