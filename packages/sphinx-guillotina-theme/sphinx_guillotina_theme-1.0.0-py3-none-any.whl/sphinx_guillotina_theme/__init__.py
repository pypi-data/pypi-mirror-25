import os


def setup(app):
    app.add_html_theme(
        'guillotina', os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'theme'))
