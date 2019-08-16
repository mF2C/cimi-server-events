import json
import importlib
import time
import datetime
import threading
import requests
from flask import Flask, render_template
from flask_sse import sse
from datetime import datetime

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
CONFIG_FILE = "./config/config.json"
JOBS_PKG = "jobs"
CHANNELS = []
JOB_LAST_STATE = {}

class JobThread(threading.Thread):
    def __init__(self, ch, freq, server_port):
        threading.Thread.__init__(self)
        self.frequency = freq
        self.channel = ch
        self.port = server_port

    def run(self):
        while True:
            time.sleep(self.frequency)
            try:
                requests.get("http://localhost:%s/%s" % (self.port, self.channel))
            except Exception as e:
                print("Failed to run %s, with exception: %s" % (self.getName(), e))
                continue


with open(CONFIG_FILE, "r") as cfg:
    config = json.loads(cfg.read())
    CIMI_API_URL = config["cimi_api_url"]
    SERVER_PORT = config["port"]

    now = datetime.utcnow()
    now_date = "%sZ" % now.strftime(TIME_FORMAT)[:-3]

    for ch in config["channels"]:
        channel = ch["job"].replace(".py", "")

        CHANNELS.append(channel)
        JOB_LAST_STATE[channel] = {"last_timestamp": now_date}

        job_trigger = JobThread(channel, ch["frequency"], SERVER_PORT)
        job_trigger.setName("Thread for channel %s" % channel)
        job_trigger.start()

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

# @app.route('/')
# def index():
#     return render_template("index.html")

@app.route('/<channel>')
def execute_job(channel):
    if channel in CHANNELS:
        modulename = "."+channel
        importlib.invalidate_caches()
        module = importlib.import_module(modulename, package=JOBS_PKG)

        events, updated_timestamp = module.run(CIMI_API_URL, JOB_LAST_STATE[channel]["last_timestamp"])
        JOB_LAST_STATE[channel]["last_timestamp"] = updated_timestamp

        for msg in events:
            sse.publish(msg, channel=channel, type='event')

        if events:
            return "New events found at %s" % updated_timestamp
        else:
            return "No new events..."
    else:
        msg = "ERROR: this channel doesn't exist"
        sse.publish(msg, channel=channel, type='error')
        return msg
