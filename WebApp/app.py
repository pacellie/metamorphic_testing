from flask import Flask, render_template, request, redirect
from argparse import ArgumentParser
import glob
import os

app = Flask(__name__)


@app.route("/")
def index():
    cwd = os.getcwd()
    if cwd.split(os.sep)[-1] == "WebApp":
        os.chdir("..")
    dirs = glob.glob(f"{args.test_directory}/*/")
    return render_template("index.html",
                           module_list=["all"] + [d.split(os.sep)[-2] for d in dirs])


@app.route("/test", methods=["POST"])
def run_test():
    cwd = os.getcwd()
    if cwd.split(os.sep)[-1] == "WebApp":
        os.chdir("..")
    dirs = glob.glob(f"{args.test_directory}/*/")
    # report_name = "reports/audio_test_new.html"
    # print(f"Check box value: {request.form.get('check_box')}")
    report_name = request.form.get("report_name")

    selected_module = request.form.get("modules")
    report_name = report_name.replace(".html", "")+".html" if report_name else f"report_{selected_module}_webapp.html"
    if not request.form.get('check_box'):
        if selected_module == "all":
            test_result = os.system(
                f"poetry run pytest {args.test_directory} --html=WebApp/static/reports/{report_name} --self-contained-html")
        else:
            test_result = os.system(
                f"poetry run pytest {args.test_directory}/{selected_module} --html=WebApp/static/reports/{report_name} --self-contained-html")
    if "WebApp" not in os.getcwd():
        os.chdir(os.path.join(os.getcwd(), "WebApp"))
    print(os.getcwd())
    return render_template("index.html", report_file=f"reports/{report_name}", module_list=["all"] + [d.split(os.sep)[-2] for d in dirs])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test_directory", "-t",
                        type=str, default="examples",
                        help="base directory for the metamorphic tests"
                        )
    parser.add_argument("--port", "-p",
                        type=int, default=5000, help="port number where app needs to be run"
                        )

    args = parser.parse_args()
    app.run(port=args.port)
