from flask import Flask, render_template, request, redirect, url_for
from db_helper import (
    get_subject_with_tests,
    get_all_subject_names,
    create_subject,
    reset_all_data,
    reset_tests,
    reset_chosen_test,
    update_target,
    update_test_score,
    delete_subject,
)

app = Flask(__name__)
app.secret_key = '212121'

@app.route("/")
def index():
    subjects = get_all_subject_names()
    return render_template("index.html", subjects=subjects)

@app.route("/create", methods=["GET", "POST"])
def create_subject_route():
    if request.method == "POST":
        name = request.form["name"].strip()
        weights = [float(w) for w in request.form.getlist("weights[]")]
        if abs(sum(weights) - 100) > 0.1:
            return "Weights must total 100%", 400
        create_subject(name, weights)
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/subject/<name>")
def view_subject(name):
    subject = get_subject_with_tests(name)
    if not subject:
        return "Subject not found", 404

    weights = [test["weight"] for test in subject["tests"]]
    scores = [test["score"] for test in subject["tests"]]
    target = subject["target"]

    total_weight_entered = 0
    total_score_weighted = 0
    for test in subject["tests"]:
        if test["score"] is not None:
            total_weight_entered += test["weight"]
            total_score_weighted += (test["score"] * test["weight"]) / 100

    grade_so_far = round((total_score_weighted / total_weight_entered) * 100, 2) if total_weight_entered > 0 else 0

    needed_results = []
    remaining_tests = [test for test in subject["tests"] if test["score"] is None]

    total_so_far = total_score_weighted
    total_weight_remaining = sum(test["weight"] for test in remaining_tests)

    if total_weight_remaining > 0:
        required_avg = (target - total_so_far) * 100 / total_weight_remaining
        required_avg = max(0, min(100, required_avg))  # Clamp between 0 and 100

        for test in remaining_tests:
            needed_score = required_avg  # Simplified, same needed average for all remaining tests
            needed_results.append((test["id"], round(needed_score, 2)))

    return render_template(
        "subject.html",
        name=name,
        subject=subject,
        grade_so_far=grade_so_far,
        needed_results=needed_results,
    )

@app.route("/reset-all", methods=["POST"])
def reset_all():
    reset_all_data()
    return redirect(url_for("index"))

@app.route("/reset-tests/<name>", methods=["POST"])
def reset_tests_route(name):
    subject = get_subject_with_tests(name)
    if not subject:
        return "Subject not found", 404
    reset_tests(subject["id"])
    return redirect(url_for("view_subject", name=name))

@app.route("/reset-chosenTest/<name>/<int:test_id>", methods=["POST"])
def reset_chosen_test_route(name, test_id):
    subject = get_subject_with_tests(name)
    if not subject:
        return "Subject not found", 404
    reset_chosen_test(subject["id"], test_id)
    return redirect(url_for("view_subject", name=name))

@app.route("/delete-subject/<name>", methods=["POST"])
def delete_subject_route(name):
    subject = get_subject_with_tests(name)
    if not subject:
        return "Subject not found", 404
    delete_subject(name)
    return redirect(url_for("index"))

@app.route("/subject/<name>/update", methods=["GET", "POST"])
def update_test_route(name):
    subject = get_subject_with_tests(name)
    if not subject:
        return "Subject not found", 404

    # Get the test_id from query string (GET)
    test_id = request.args.get("test_id", type=int)

    if request.method == "POST":
        # POST form has test_id and mark inputs
        test_id = int(request.form["test_id"])
        new_score = float(request.form["mark"])
        subject_id = subject['id']
        update_test_score(subject_id, test_id, new_score)
        return redirect(url_for("view_subject", name=name))

    # For GET, pass the test_id so you can set the selected option in the form
    return render_template("update_test.html", name=name, subject=subject, selected_test_id=test_id)


@app.route("/subject/<name>/target", methods=["POST"])
def update_target_route(name):
    subject = get_subject_with_tests(name)
    if not subject:
        return "Subject not found", 404
    new_target = float(request.form["target"])
    update_target(subject["id"], new_target)
    return redirect(url_for("view_subject", name=name))

if __name__ == "__main__":
    app.run(debug=True)
