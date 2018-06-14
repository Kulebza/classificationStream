import cv2
from flask_mail import Mail
from flask_script import Manager

from keras.models import model_from_json

from app import app
from flask_bootstrap import Bootstrap
import tensorflow as tf

mail = Mail(app)

ADMINS = ['your-gmail-username@gmail.com']

#bootstrap = Bootstrap(app)
manager = Manager(app)


def load():
    json_file = open("app\\app\\static\\railway_model.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    # Создаем модель на основе загруженных данных
    model = model_from_json(loaded_model_json)
    # Загружаем веса в модель
    model.load_weights("app]\\app\\static\\railway_model.h5")
    model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])
    return model

global model
model = load()

global adress
adress = "elizaweta.by4kova@yandex.ru"

global camera_url
camera_url = "https://streaming.ivideon.com/hls/live.m3u8?server=200-4721c6ffcb78953b724c195f01db1168&camera=327680&sessionId=demo&q=2&acodec=none&wait_segments=1&segment_duration=1&_=0.9379075938869521"

global vidcap
vidcap = cv2.VideoCapture(camera_url)

global graph
graph = tf.get_default_graph()

# Run the manager
if __name__ == '__main__':
    with graph.as_default():
        load()
    manager.run(treaded = True)