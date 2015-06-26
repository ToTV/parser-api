# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from datetime import datetime
from enum import Enum
import json

from flask import Flask, request, jsonify, render_template
from wtforms import Form, StringField, validators, SelectField
import guessit

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    else:
        return str(obj)


class MediaTypes(Enum):
    Unknown = "unknown"
    TV = "tv"
    Movie = "movie"


class ClassifyForm(Form):
    release_name = StringField("Release Name", [validators.Length(min=4, max=255)])
    media_type = SelectField("Media Type", choices=[
        (MediaTypes.TV.value, MediaTypes.TV.name),
        (MediaTypes.Movie.value, MediaTypes.Movie.name),
        (MediaTypes.Unknown.value, MediaTypes.Unknown.name)
    ], default=MediaTypes.TV.value)


app = Flask("parser")
app.config['DEBUG'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", form=ClassifyForm(request.form))


@app.route("/classify", methods=["POST"])
def classify():
    if request.content_type == "application/json":
        form = ClassifyForm(data=request.get_json(force=True))
    else:
        form = ClassifyForm(request.form)
    if form.validate():
        release_name = form.release_name.data
        if form.media_type.data == "unknown":
            data = guessit.guess_file_info(release_name, {})
        elif form.media_type.data == "tv":
            data = guessit.guess_episode_info(release_name, {})
        else:
            data = guessit.guess_movie_info(release_name, {})
        try:
            jsonify()
            return json.dumps(data, default=json_serial)
        except Exception as err:
            return json.dumps({"err": str(err)}, default=json_serial)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7877)
