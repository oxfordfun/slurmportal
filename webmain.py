import time
import json
import datetime as dt

import flask
import argh
import pyslurm
import humanize


app = flask.Flask(__name__)


@app.route("/")
def root():
    return "Hello"


@app.route("/jobs")
def jobs():
    time_now = time.time()

    def nice_time(t2):
        return humanize.naturaltime(dt.timedelta(seconds=(time_now - t2))).capitalize()

    jobs = pyslurm.job().get()
    return flask.render_template(
        "jobs.jinja2", title="Slurm Jobs", jobs=jobs, nice_time=nice_time
    )


@app.route("/nodes")
def nodes():
    jobs = pyslurm.job().get()
    formatted = json.dumps(jobs, indent=4, sort_keys=True)
    return f"<pre>{formatted}</pre>"


def main(debug=False):
    app.run(host="0.0.0.0", debug=debug)


if __name__ == "__main__":
    argh.dispatch_command(main)
