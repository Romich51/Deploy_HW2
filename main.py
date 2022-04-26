from flask import Flask

from service import init_redis, init_scheduler, init_service, get_secret_number
from service import views


app = Flask(__name__)


if __name__ == '__main__':
    HOST = '167.235.242.179'
    PORT = 8501
    SERVICE_NAME = "web_app"

    get_secret_number()
    init_redis(host=HOST, port=6379, password="qwe123")
    init_service(service_name=SERVICE_NAME, host=HOST, port=PORT)
    scheduler = init_scheduler(service_name=SERVICE_NAME)
    scheduler.init_app(app)
    scheduler.start()

    app.register_blueprint(views.bp)

    app.run(host=HOST, port=PORT)
