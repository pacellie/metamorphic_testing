from pathlib import Path
from flask import Flask, render_template, request, send_from_directory
from argparse import ArgumentParser
import glob
import os

app = Flask(__name__)


@app.route("/")
def index():
    dirs = glob.glob(f"{args.test_directory}/*/")
    return render_template("index.html",
                           module_list=["all"] + [d.split(os.sep)[-2] for d in dirs])


# Custom static data
@app.route('/custom_static/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename, conditional=True)


@app.after_request
def add_header(r):  # no response caching
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/test", methods=["POST"])
def run_test():
    dirs = glob.glob(f"{args.test_directory}/*/")
    report_name = request.form.get("report_name")
    selected_module = request.form.get("modules")
    report_name = report_name.replace(".html", "") + ".html" if report_name \
        else f"report_{selected_module}_webapp.html"

    if not request.form.get('load_previous_report'):
        command = f"poetry run pytest {args.test_directory}" if selected_module == "all" \
            else f"poetry run pytest {args.test_directory}/{selected_module}"
        command_args = f" --html=assets/reports/{report_name} --self-contained-html"
        os.system(command + command_args)  # nosec

    return render_template(
        "index.html",
        report_file=f"reports/{report_name}",
        module_list=["all"] + [d.split(os.sep)[-2] for d in dirs]
    )


if __name__ == "__main__":
    # change directory
    if Path.cwd().name == "web_app":
        # we need to be in the root directory of the repository
        os.chdir("..")

    # app configuration
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # no caching
    app.config['CUSTOM_STATIC_PATH'] = os.path.join(app.root_path, '..', 'assets')

    # input configuration
    parser = ArgumentParser()
    parser.add_argument("--test_directory", "-t",
                        type=str, default="examples",
                        help="base directory for the metamorphic tests"
                        )
    parser.add_argument("--port", "-p",
                        type=int, default=5000, help="port number where app needs to be run"
                        )
    args = parser.parse_args()

    # app trigger / start
    app.run(port=args.port, debug=False)
