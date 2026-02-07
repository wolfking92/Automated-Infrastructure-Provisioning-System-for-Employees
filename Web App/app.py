from flask import Flask, render_template, request, redirect, session
from aws_utils.ec2 import (
    get_instances,
    launch_instance,
    delete_instance,
    can_launch_instance
)
from config import SUBNETS

app = Flask(__name__)
app.secret_key = "super-secret-key"

INSTANCE_TYPES = ["t2.micro", "t3.micro"]


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        emp_id = request.form.get("emp_id")

        if not name or not emp_id:
            return "Invalid input", 400

        session["employee_name"] = name
        session["employee_id"] = emp_id
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "employee_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        name=session["employee_name"],
        instances=get_instances(session["employee_id"]),
        instance_types=INSTANCE_TYPES,
        subnets=SUBNETS,
        error=session.pop("error", None)
    )


@app.route("/launch", methods=["POST"])
def launch():
    if not can_launch_instance(session["employee_id"]):
        session["error"] = "❌ Maximum 2 EC2 instances allowed per employee"
        return redirect("/dashboard")

    launch_instance(
        instance_type=request.form["instance_type"],
        subnet_id=request.form["subnet_id"],
        employee_name=session["employee_name"],
        employee_id=session["employee_id"]
    )

    return redirect("/dashboard")


@app.route("/delete/<instance_id>")
def delete(instance_id):
    delete_instance(instance_id)
    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)