from flask import Flask, request, redirect, render_template
from urllib.parse import urlencode, unquote
from wifipumpkin3.core.utility.collection import SettingsINI
import wifipumpkin3.core.utility.constants as C
import sys
import subprocess
import argparse

# app = Flask(__name__,static_url_path='/templates/flask/static',
#             static_folder='templates/flask/static',
#             template_folder='templates/flask')
app = Flask(__name__)
REDIRECT = None
FORCE_REDIRECT = None
URL_REDIRECT = None
PORT = 80
config = None


def login_user(ip, iptables_binary_path):
    subprocess.call(
        [
            iptables_binary_path,
            "-t",
            "nat",
            "-I",
            "PREROUTING",
            "1",
            "-s",
            ip,
            "-j",
            "ACCEPT",
        ]
    )
    subprocess.call([iptables_binary_path, "-I", "FORWARD", "-s", ip, "-j", "ACCEPT"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if (
        request.method == "POST"
        and "login" in request.form
        and "password" in request.form
    ):
        sys.stdout.write(
            str(
                {
                    request.remote_addr: {
                        "login": request.form["login"],
                        "password": request.form["password"],
                    }
                }
            )
        )
        global FORCE_REDIRECT, URL_REDIRECT, config
        sys.stdout.flush()
        login_user(request.remote_addr, config.get("iptables", "path_binary"))
        if URL_REDIRECT:
            return redirect(URL_REDIRECT, code=302)
        if FORCE_REDIRECT:
            return render_template("templates/login_successful.html")
        elif "orig_url" in request.args and len(request.args["orig_url"]) > 0:
            return redirect(unquote(request.args["orig_url"]))
        else:
            return render_template("templates/login_successful.html")
    else:
        return render_template(
            "templates/login.html",
            orig_url=urlencode({"orig_url": request.args.get("orig_url", "")}),
        )


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("templates/favicon.ico")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    global REDIRECT, PORT
    if PORT != 80:
        return redirect(
            "http://{}:{}/login?".format(REDIRECT, PORT)
            + urlencode({"orig_url": request.url})
        )
    return redirect(
        "http://{}/login?".format(REDIRECT) + urlencode({"orig_url": request.url})
    )


# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


_version = "1.0.2"


def main():
    global REDIRECT, FORCE_REDIRECT, URL_REDIRECT, PORT, config
    print("[*] CaptiveFlask v{} - subtool from wifipumpkin3".format(_version))
    parser = argparse.ArgumentParser(
        description="CaptiveFlask - \
    Server to create captive portal with flask\n doc: https://github.com/mh4x0f/captiveportals"
    )
    parser.add_argument(
        "-t", "--tamplate", dest="template", help="path the theme login captive portal"
    )
    parser.add_argument(
        "-s", "--static", dest="static", help="path  of the static files from webpage"
    )
    parser.add_argument(
        "-r",
        "--redirect",
        dest="redirect",
        help="IpAddress from gataway captive portal",
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        default=80,
        help="The port for captive portal",
    )
    parser.add_argument(
        "-rU",
        "--redirect-url",
        dest="redirect_url",
        default=None,
        help="Url for redirect after user insert the credentials on captive portal",
    )
    parser.add_argument(
        "-f",
        "--force-login_successful-template",
        dest="force_redirect",
        default=False,
        type=str2bool,
        help="force redirect to login_successful.html template",
    )
    parser.add_argument("-v", "--version", dest="version", help="show version the tool")
    args = parser.parse_args()
    REDIRECT = args.redirect
    FORCE_REDIRECT = args.force_redirect
    URL_REDIRECT = args.redirect_url
    PORT = args.port

    config = SettingsINI(C.CONFIG_INI)

    app.static_url_path = "\{}".format(args.static)
    app.static_folder = "{}".format(args.static)
    app.template_folder = args.template

    app.run(REDIRECT, port=args.port)
