#!/usr/bin/env python

"""A meaningful docstring


"""

import argparse
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests
from jinja2 import Template
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename


def render_gist_js(code, path):
    template = Template("""script = document.querySelector('script[src$="{{ path }}"]')
    script.insertAdjacentHTML( 'afterend','{{ code|tojson }}' );""")

    return template.render(code=code, path=path)


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200, "running")
        elif re.search("https://github.com/.*/.*", self.path):
            github_raw_url = self.path[1:].replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")

            response = requests.get(url=github_raw_url)
            code = response.content.decode('UTF-8')

            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)

            style = "default"
            if 'style' in params:
                style = params['style'][0]

            if 'slice' in params:
                slice_value = params['slice'][0].split(":")
                from_ = int(slice_value[0])
                to_ = int(slice_value[1])
                lines = str(code).splitlines()
                selected_lines = lines[from_:to_]

                code = "\n".join(selected_lines)

            filename = parsed_url.path.split('/')[-1:][0]
            lexer = guess_lexer_for_filename(filename, response.content)

            formatter = HtmlFormatter(linenos=False, cssclass="gist-it-highlight", style=style)

            highlighted_code = highlight(code, lexer, formatter)
            css = formatter.get_style_defs('.gist-it-highlight')

            result = highlighted_code + f"<style> {css}</style>"

            js_rendered = render_gist_js(result, self.path)

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(js_rendered.encode('utf8'))

        else:
            self.send_response(404)

        self.end_headers()


def main():
    parser = argparse.ArgumentParser(description='HTTP Server')
    args = parser.parse_args()

    server = HTTPServer(("localhost", 4876), HTTPRequestHandler)
    print('HTTP Server Running...........')
    server.serve_forever()


if __name__ == '__main__':
    main()
