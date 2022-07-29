from flask import Flask, render_template, request, send_from_directory
from argparse import ArgumentParser
import glob
import os

app = Flask(__name__)


@app.route("/")
def index():
    cwd = os.getcwd()
    if cwd.split(os.sep)[-1] == "web_app":
        os.chdir("..")
    dirs = glob.glob(f"{args.test_directory}/*/")
    return render_template("index.html",
                           module_list=["all"] + [d.split(os.sep)[-2] for d in dirs])


# Custom static data
@app.route('/custom_static/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename, conditional=True)


@app.route("/test", methods=["POST"])
def run_test():
    cwd = os.getcwd()
    if cwd.split(os.sep)[-1] == "web_app":
        os.chdir("..")
    dirs = glob.glob(f"{args.test_directory}/*/")
    report_name = request.form.get("report_name")

    selected_module = request.form.get("modules")
    report_name = report_name.replace(".html", "") + ".html" if report_name \
        else f"report_{selected_module}_webapp.html"
    if not request.form.get('load_previous_report'):
        command_args = f" --html=assets/reports/{report_name} --self-contained-html"
        command = f"poetry run pytest {args.test_directory}" if selected_module == "all" \
            else f"poetry run pytest {args.test_directory}/{selected_module}"
        os.system(command + command_args)  # nosec
    if "web_app" not in os.getcwd():
        os.chdir(os.path.join(os.getcwd(), "web_app"))
    return render_template(
        "index.html",
        report_file=f"reports/{report_name}",
        module_list=["all"] + [d.split(os.sep)[-2] for d in dirs]
    )


if __name__ == "__main__":
    app.config['CUSTOM_STATIC_PATH'] = os.path.join(app.root_path, '..', 'assets')
    parser = ArgumentParser()
    parser.add_argument("--test_directory", "-t",
                        type=str, default="examples",
                        help="base directory for the metamorphic tests"
                        )
    parser.add_argument("--port", "-p",
                        type=int, default=5000, help="port number where app needs to be run"
                        )

    args = parser.parse_args()
    app.run(port=args.port, debug=False)
