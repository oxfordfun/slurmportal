import time
import json
import datetime as dt

import flask
import argh
import pyslurm
import humanize


def nice_time(t2):
    time_now = time.time()
    return humanize.naturaltime(dt.timedelta(seconds=(time_now - t2))).capitalize()


app = flask.Flask(__name__)


@app.route("/")
def root():
    return "Hello"


@app.route("/resources")
def resources():
    time_now = time.time()


@app.route("/jobs")
def jobs():
    jobs = pyslurm.job().get()
    return flask.render_template(
        "jobs.jinja2", title="Slurm Jobs", jobs=jobs, nice_time=nice_time
    )


@app.route("/nodes")
def nodes():
    nodes = pyslurm.node().get()
    return flask.render_template("nodes.jinja2", title="Nodes", nodes=nodes)


@app.route("/cancel/<job_id>")
def cancel(job_id):
    try:
        pyslurm.slurm_kill_job(int(job_id), 9, 1)
    except:
        pass
    return flask.redirect("/jobs")


@app.route("/detail/<job_id>")
def detail(job_id):
    pyslurmjob = pyslurm.job()
    jobs = pyslurmjob.get()
    detail = jobs[int(job_id)]
    return flask.render_template(
        "job.jinja2", title="Job Detail", job=detail, job_id=job_id
    )


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if flask.request.method == "GET":
        return flask.render_template("submit.jinja2", title="Submit a Job")
    if flask.request.method == "POST":
        job_name = flask.request.form.get("job_name")
        job_command = flask.request.form.get("job_command")
        job_output = flask.request.form.get("output")
        job_error = flask.request.form.get("error")
        job = {}
        job["wrap"] = job_command
        job["job_name"] = job_name
        job["output"] = job_output
        job["error"] = job_error
        test_job_id = pyslurm.job().submit_batch_job(job)

        return flask.redirect("/jobs")


def main(debug=False):
    app.run(host="0.0.0.0", debug=debug)


if __name__ == "__main__":
    argh.dispatch_command(main)
