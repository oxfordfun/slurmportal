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


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if flask.request.method == "GET":
        return flask.render_template("submit.jinja2", title="Submit a Job")
    if flask.request.method == "POST":
        job_name = flask.request.form.get("job_name")
        job_command = flask.request.form.get("job_command")
        job = {}
        job["wrap"] = job_command
        job["job_name"] = job_name
        test_job_id = pyslurm.job().submit_batch_job(job)

        return flask.redirect("/jobs")


def main(debug=False):
    app.run(host="0.0.0.0", debug=debug)


if __name__ == "__main__":
    argh.dispatch_command(main)
