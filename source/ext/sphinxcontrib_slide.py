# -*- coding: utf-8 -*-
"""
    sphinxcontrib.slide
    ~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2012 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import os

from docutils import nodes, utils
from docutils.parsers.rst import directives

from sphinx.util.compat import Directive


class slide(nodes.General, nodes.Element):
    pass


class SlideDirective(Directive):
    """Directive for embedding slide"""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
    }

    def run(self):
        node = slide()
        node['url'] = self.arguments[0]
        node['slide_options'] = get_slide_options(self.arguments[0])

        return [node]


def get_slide_options(url):
    import re
    import urllib2

    options = {}

    content = urllib2.urlopen(url).read()
    matched = re.search('http://www.slideshare.net/slideshow/embed_code/\d+', content)
    if matched:
        options['embed_url'] = matched.group(0)

    matched = re.search('<title>(.*?)</title>', content)
    if matched:
        options['title'] = matched.group(1).decode('utf-8')

    matched = re.search('<meta name="slideshow_author".*? content="(.*?)" />', content)
    if matched:
        options['author_url'] = matched.group(1)

    matched = re.search('<img class="h-author-image".*? alt="(.*?)" width="50" />', content)
    if matched:
        options['author_name'] = matched.group(1).decode('utf-8')

    return options


def visit_slide_node(self, node):
    template = """<iframe src="%s" width="427" height="356" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="%s" title="%s" target="_blank">%s</a> </strong> from <strong><a href="%s" target="_blank">%s</a></strong> </div>"""
    options = node['slide_options']
    self.body.append(template % (options.get('embed_url'),
                                 options.get('url'),
                                 options.get('title', ""),
                                 options.get('title', ""),
                                 options.get('author_url'),
                                 options.get('author_name', "")))


def depart_slide_node(self, node):
    pass


def setup(app):
    app.add_node(slide,
                 html=(visit_slide_node, depart_slide_node))
    app.add_directive('slide', SlideDirective)
