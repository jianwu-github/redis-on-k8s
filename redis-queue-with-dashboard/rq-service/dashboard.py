import os

from pathlib import Path
from dotenv import load_dotenv

from flask import Flask
import rq_dashboard

service_prj_dir = Path(__file__).parent.parent
service_prj_env_file = service_prj_dir / 'rq-service.env'

if service_prj_env_file.exists():
    print("Running local dev env, and loading environment variables from file: {0}".format(service_prj_env_file))
    load_dotenv(service_prj_env_file)
else:
    print(f'Running in docker, no redis env file: ${service_prj_env_file}')

app = Flask(__name__)
app.config["REDIS_HOST"] = os.environ.get("REDIS_HOST")
app.config["REDIS_PORT"] = os.environ.get("REDIS_PORT")
app.config["REDIS_DB"] = os.environ.get("REDIS_DB")
app.config["RQ_POLL_INTERVAL"] = os.environ.get("RQ_POLL_INTERVAL")

app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")


@app.route("/")
def server_info():
    return "<h3>Redis Queue Dashboard</h3>"


if __name__ == "__main__":
    app.run()
