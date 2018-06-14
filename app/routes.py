import cv2
import datetime as dt
import numpy as np

from flask import render_template
from flask import request as req
from flask.json import jsonify
from flask_mail import Message
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image

from app import app
import app.manage as mn

@app.route('/')
def index():
    return render_template('start.html')

@app.route('/start')
def start():
    success, img = mn.vidcap.read()
    if (success):
        result = predict(img)
    else:
        mn.vidcap = cv2.VideoCapture(mn.camera_url)
        success, img = mn.vidcap.read()
        if (success):
            result = predict(img)
        else:
            result = "Подождите"
    return jsonify(result = result)

@app.route('/stop')
def stop():
    cv2.destroyAllWindows()
    mn.vidcap.release()
    return jsonify(result=True)

@app.route('/cam', methods=['GET'])
def cam():
    return render_template('cam.html')

def predict(img):
    try:
        global crop_img
        crop_img = img[130:650, 630:1340]
        img = cv2.resize(crop_img, (224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        with mn.graph.as_default():
            preds = mn.model.predict(x)
        n, j = np.unravel_index(preds.argmax(), preds.shape)
        d = {0: 'На переезде свободно', 1: 'На переезде поток машин', 2: 'На переезде следует поезд'}
        r = {"label": d.get(j), "probability": float(preds[n, j])*100,
             "time": dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        results = "{} {}: вероятность {:.2f}% ".format(r.get("time"), r.get("label"), r.get("probability"))
    except:
        results="Ошибка распознавания"
    return results

@app.route('/changeadress')
def change():
    return render_template('b.html')


@app.route('/send')
def send():
    res = start()
    cv2.imwrite('app//predict.jpg', crop_img)
    msg = Message("Оповещение",
                  sender="railways.monitoring@gmail.com",
                  recipients=[mn.adress])
    msg.body = "г.Подольск (улица Ленинцев) " + res.json.get('result')
    with app.open_resource("predict.jpg") as fp:
        msg.attach('predict.jpg', "image/jpg", fp.read())
    mn.mail.send(msg)
    return jsonify(result = "Письмо отправлено")

@app.route('/mail')
def mailing():
    a = req.args.get('a', 0, type=str)
    mn.adress = a
    return jsonify(result = "Адрес изменен ")
