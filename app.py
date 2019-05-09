from flask import Flask, redirect, url_for
from common.database import Database
#from utils.scheduler_utils import SchedulerUtils
import threading

app = Flask(__name__)

@app.before_first_request
def init_db():
    Database.initialize()
    #t = threading.Thread(target=SchedulerUtils.init_schedule)
    #t.start()


@app.route('/')
def home():
    return redirect(url_for('weight.register_weight'))


from blueprints.weight import weight_blueprint

app.register_blueprint(weight_blueprint, url_prefix='/weight')


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", threaded=True)
