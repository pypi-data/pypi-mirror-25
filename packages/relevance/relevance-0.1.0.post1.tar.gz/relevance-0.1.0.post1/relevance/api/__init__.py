"""
Relevance API package.

This package provides some common interfaces for the different REST APIs to use.
"""

from flask import Flask


def start_app(app: Flask):
    """
    Start an API application.

    app -- the application object.
    """
    app.run(debug=True)
