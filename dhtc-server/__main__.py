from flask import Flask, request, jsonify, render_template, send_from_directory
from podb import DB, DBEntry
from os.path import join, dirname
from argparse import ArgumentParser


class Torrent(DBEntry):
    def __init__(self, data: dict):
        DBEntry.__init__(self, **data)
        self.table = "torrent"


class Watch(DBEntry):
    def __init__(self, key: str, match_type: str, query: str):
        DBEntry.__init__(self)
        self.key = key
        self.match_type = match_type
        self.query = query
        self.table = "watch"


class BlacklistItem(DBEntry):
    def __init__(self, regex, match_type):
        DBEntry.__init__(self)
        self.regex = regex
        self.match_type = match_type
        self.table = "blacklist"


app = Flask(__name__)
static_folder = join(dirname(__file__), "static")
app.template_folder = join(dirname(__file__), "templates")
db = DB("dhtc")


def search_function():
    results = []
    match_type = request.form.get("match-type")
    key = request.form.get("key")
    value = request.form.get("search-input")
    if match_type == "contains":
        results = db.find_contains(key, value)
    elif match_type == "equals":
        results = db.find({"{}".format(key): value})
    elif match_type == "startswith":
        results = db.find_startswith(key, value)
    elif match_type == "endswith":
        results = db.find_endswith(key, value)
    return results


@app.route("/api/v1/add", methods=["POST"])
def api_v1_add():
    print(request.json)
    return jsonify({"error": not db.insert(Torrent(request.json))})


@app.route("/api/v1/search", methods=["POST"])
def api_v1_search():
    return jsonify(db.find_contains(request.json["key"], request.json["query"]))


@app.route("/api/v1/blacklist")
def api_v1_blacklist():
    return jsonify({"blacklist": [result.__dict__ for result in db.find({"table": "blacklist"})]})


@app.route("/")
def root():
    return render_template("dashboard.html", info_hash_count=len(db.find_all_with_key("InfoHash")))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", info_hash_count=len(db.find_all_with_key("InfoHash")))


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        return render_template("search.html", results=search_function())
    return render_template("search.html")


@app.route("/discover")
def discover():
    return render_template("discover.html", results=db.get_random_list(50))


@app.route("/watches", methods=["GET", "POST"])
def watches():
    if request.method == "POST":
        data = request.form.to_dict()
        if data["op"] == "add":
            db.insert(Watch(data["key"], data["match-type"], data["search-input"]))
        elif data["op"] == "delete":
            db.delete_by_uuid(data["id"])
    return render_template("watches.html", results=db.find({"table": "watch"}))


@app.route("/blacklist", methods=["GET", "POST"])
def blacklist():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        if data["op"] == "add":
            db.insert(BlacklistItem(data["Filter"], data["Type"]))
        elif data["op"] == "delete":
            db.delete_by_uuid(data["id"])
    return render_template("blacklist.html", results=db.find({"table": "blacklist"}))


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory(join(static_folder, "css"), path)


@app.route("/js/<path:path>")
def js(path):
    return send_from_directory(join(static_folder, "js"), path)


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1", help="server address")
    ap.add_argument("--port", default=7331, help="server port")
    a = ap.parse_args()
    app.run(a.host, a.port)
