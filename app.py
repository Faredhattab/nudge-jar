import os
import random

from flask import Flask, jsonify, render_template, request

nudges = []


def _serialize_nudges():
    return {"nudges": nudges}


def _clean_nudge_text(payload):
    return str(payload.get("text", "")).strip()


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/nudges")
    def get_nudges():
        return jsonify(_serialize_nudges())

    @app.post("/api/nudges")
    def add_nudge():
        data = request.get_json(silent=True) or {}
        text = _clean_nudge_text(data)

        if not text:
            return jsonify({"error": "Nudge cannot be empty."}), 400

        nudges.append(text)
        return jsonify({"ok": True, **_serialize_nudges()}), 201

    @app.get("/api/nudges/random")
    def get_random_nudge():
        if not nudges:
            return jsonify({"error": "Add a nudge first."}), 404

        return jsonify({"nudge": random.choice(nudges)})

    return app


def reset_nudges():
    nudges.clear()


def is_debug_enabled():
    return os.environ.get("FLASK_DEBUG", "0") == "1"


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=is_debug_enabled(),
    )
