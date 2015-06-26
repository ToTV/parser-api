# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from enum import Enum
from flask import Flask, request, jsonify, render_template
from wtforms import Form, StringField, validators, SelectField
import guessit


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
        return jsonify(data)


if __name__ == "__main__":
    app.run()
