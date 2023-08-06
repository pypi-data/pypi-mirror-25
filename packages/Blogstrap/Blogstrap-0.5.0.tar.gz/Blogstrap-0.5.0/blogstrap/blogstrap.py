# Copyright 2015 Joe H. Rahme <joehakimrahme@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import argparse
import os

import flask
import mimerender
import six
if six.PY2:
    from exceptions import IOError
    import sys
    reload(sys)  # noqa
    sys.setdefaultencoding('utf-8')

    import builder
else:
    import blogstrap.builder as builder


class ArticleNotFound(IOError):
    pass


class ArticleHidden(Exception):
    pass


class ArticleReader(object):

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        try:
            with open(self.path) as f:
                return ''.join(f.read())
        except IOError:
            raise ArticleNotFound(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class DefaultConfig(object):
    DEBUG = True
    BLOGROOT = "."
    THEME = "simplex"
    BLOGTITLE = "Powered by Blogstrap"
    HOMEPAGE_MESSAGE = "SUCCESS"


# Registering markdown as a valid MIME.
# More info: https://tools.ietf.org/html/rfc7763
mimerender.register_mime('markdown', ('text/markdown',))
mimerender = mimerender.FlaskMimeRender()


def create_app(config_file=None):
    app = flask.Flask(__name__)
    if config_file:
        app.config.from_pyfile(config_file)
    else:
        app.config.from_object(DefaultConfig)

    def render_html(message):
        return flask.render_template("strapdown.html",
                                     theme=app.config['THEME'],
                                     text=message,
                                     title=app.config['BLOGTITLE'])

    def render_html_exception(exception):
        return flask.render_template('404.html',
                                     theme=app.config['THEME'],
                                     title=app.config['BLOGTITLE'])

    def render_markdown(message):
        return message

    def render_md_exception(exception):
        return flask.render_template('404.md')

    @app.route("/")
    def nothing():
        return app.config['HOMEPAGE_MESSAGE']

    @app.route("/<blogpost>")
    @mimerender.map_exceptions(
        mapping=(
            (ArticleNotFound, '404 Article Not Found'),
            (ArticleHidden, '404 Article Hidden'),
        ),
        default='markdown',
        markdown=render_md_exception,
        html=render_html_exception,
    )
    @mimerender(
        default='markdown',
        html=render_html,
        markdown=render_markdown)
    def serve_blog(blogpost):
        if blogpost.startswith("."):
            raise ArticleHidden()
        root_directory = app.config['BLOGROOT']

        blogpost = "/".join((root_directory, blogpost))
        accept_header = flask.request.headers.get('Accept', [])
        suffix = ""
        if "text/html" in accept_header:
            if os.path.exists(blogpost + ".html"):
                suffix = ".html"
        else:
            if os.path.exists(blogpost + ".md"):
                suffix = ".md"

        blogpost += suffix

        with ArticleReader(blogpost) as article:
            return {'message': article}

    return app


def build_parser():
    """Builds the argument parser."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Blogstrap commands')
    init_parser = subparsers.add_parser('init', help='Default')
    init_parser.set_defaults(func=init)
    init_parser.add_argument('-t', '--target',
                             dest='target',
                             type=str,
                             default='.',
                             help='Target folder to generate files in')
    run_parser = subparsers.add_parser(
        'run', help="Run the Flask development server")
    run_parser.set_defaults(func=run)
    run_parser.add_argument('-c', '--config',
                            dest='config',
                            type=str,
                            default=None,
                            help='path to a config file')

    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


def init(args):
    builder.build(args)


def run(args):
    application = create_app(args.config)
    application.run()
