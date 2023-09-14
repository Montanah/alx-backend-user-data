#!/usr/bin/env python3
""" Basic Flask app
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ GET /
    Return:
      - Welcome message
    """
    return jsonify({"message": "Bienvenue"})
