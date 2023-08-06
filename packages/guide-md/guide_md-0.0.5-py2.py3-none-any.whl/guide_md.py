import mistune
import re
import inspect
import copy
try:
    import urlparse
except:
    import urllib.parse as urlparse

import posixpath
"""
    guide_md
    ~~~~~~~
    An extension to mistune
    :copyright: 2016 John Pickerill

    Based on and dependant on mistune :copyright: (c) 2014 - 2015 by Hsiaoming Yang.
"""

# TODO I'm unconvinced about the use of URLPARSE and whether its doing what was intended
# TODO disable embedded HTML ?


__version__ = '0.0.5'
__author__ = 'John Pickerill <john@curiouscrab.com>'
__all__ = [
    'BlockGrammar', 'BlockLexer',
    'InlineGrammar', 'InlineLexer',
    'Renderer', 'Markdown',
    'markdown'
]


def styles(context, purpose):
    return "g_default"


# TODO should switch to 'https?:\/\/[^\s\/$.?#].[^\s]*$ as the one below fails www.english-heritage.uk
# 'https://mathiasbynens.be/demo/url-regex
_reUrl = re.compile(r'^https?:\/\/(-\.)?([^\s\/?\.#-]+\.?)+(\/[^\s]*)?$')
_reEmail = re.compile(r'^(mailto\:)?[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', re.IGNORECASE)
_reSnippet = re.compile(r'@(\S{3}):(\S+)')


def url_for(*args, **kwargs):
    return kwargs['itemid']


def output_drop(self):
    hdInd = hotdropIndex(self)
    if ((self.token['hdInd'] is None) or (not self.token['hdInd'].startswith("_"))):
        self.token['hdInd'] = hdInd
    md = Markdown(hn=self.token['hdInd'], **self.kwargs)  # TODO what if using custom renderers or lexers
    cnt = md(self.token['text'])
    return self.renderer.drop(
        self.token['hdInd'],
        self.token['title'],
        self.token['level'],
        self.token['option'], cnt)


def output_blk(self):
    md = Markdown(**self.kwargs)  # TODO what about drops  see above
    cnt = md(self.token['text'])
    return self.renderer.blk(self.token['option'], cnt)


def output_box(self):
    return self.renderer.box(self.token['option'], self.token['text'])


def output_graph(self):
    return self.renderer.graph(self.token['option'], self.token['text'])


def output_item(self):
    return self.renderer.item(self.token['item'], self.token['option'])


def hotdropIndex(self):
    self.hi = self.hi + 1
    return self.hn + "_" + str(self.hi)


class Markdown(mistune.Markdown):

    elinks = []
    iLinks = []
    hi = 0
    hn = ""

    # GE: 2017-02-15 added explict 'escape' render option
    def __init__(self, renderer=None, inline=None, block=None, hn="drop", styling=None, escape=False, **kwargs):


        self.hn = hn
        self.kwargs = kwargs

        global styles
        if styling:
            styles = styling

        if not renderer:
            # GE: 2017-02-15 added explict 'escape' render option
            renderer = Renderer(escape=escape, **kwargs)
        else:
            kwargs.update(renderer.options)
        self.renderer = renderer

        if inline and inspect.isclass(inline):
            inline = inline(renderer, **kwargs)
        else:
            inline = InlineLexer(renderer, **kwargs)
        self.inline = inline

        if block and inspect.isclass(block):
            block = block(**kwargs)
        else:
            block = BlockLexer(**kwargs)
        self.block = block

        Markdown.output_drop = output_drop
        Markdown.output_blk = output_blk
        Markdown.output_item = output_item
        Markdown.output_box = output_box
        Markdown.output_graph = output_graph
        super(Markdown, self).__init__(renderer=renderer, inline=inline, block=block, **kwargs)


class Renderer(mistune.Renderer):
    hn = "hd"
    hi = 0

    def __init__(self, hn="hdx", **kwargs):

        f = kwargs.get('url_for')

        if inspect.isfunction(f):
            self.url_for = f
        else:
            self.url_for = url_for

        if kwargs.get('static'):
            self._static = kwargs.get('static')
        else:
            self._static = ""

        if kwargs.get('index'):
            self._index = kwargs.get('index')
        else:
            self._index = ""

        # TODO this is a quick way of making the mistune tests pass - we should actually have a generic way of
        # incorporating bootstrap capabilities and css styles
        if kwargs.get('testmode', False):
            self.testmode = True
            self._blank = " "
            self._top = " "
            self._table = ""
            self._img = " "
            self._images = ""
        else:
            self.testmode = False
            self._blank = ' target="_blank" '
            self._top = ' target="_self" '
            self._table = ' class="table table-striped table-bordered"'
            self._img = ' class="cc_img" '
            self._images = "images"

        self.hn = hn
        super(Renderer, self).__init__(**kwargs)

    def graph(self, option, code):
        return '\n<div class="algorithm">graph TD\n' + code + '</div>\n'

    def box(self, option, text):
        return '<pre><jpc>' + text + '</jpc></pre>'

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.
        :param header: header part of the table.
        :param body: body part of the table.
        """
        return (
            '<table%s>\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (self._table, header, body)

    def spanFormat(self, style, text):
        return '<span class="%s">%s</span>' % (style, text)

    def anchor(self, name):
        return '<a id="%s"></a>' % (name)

    def blk(self, option, text):
        return '<div class="' + option + '">' + text + '</div>'

    def drop(self, hdInd, title, level, option, text):
        if level == 0:
            stag = '<p>'
            etag = '</p>'
        else:
            stag = '<h' + str(level) + ' class="cc-drop-title">'
            etag = '</h' + str(level) + ' >'

        options = "accordion"
        opts = option.split()
        for o in opts:
            options += " cc-drop-%s" % (o)

        hd = ('<div class="%s" id="info%s">\n<div class="accordion-group ">\n'
              '<div class="cc-drop-head">\n'
              '<a class="accordion-toggle collapsed" data-toggle="collapse"'
              ' data-parent="#info%s" href="#%s">\n' % (options, hdInd, hdInd, hdInd))
        hd += ('%s' % (stag))
        hd += '%s%s</a></div>\n' % (title, etag)
        hd += ('<div id="%s" class="accordion-body collapse">\n'
               '<div class="accordion-inner cc-drop-body">\n%s' % (hdInd, text))
        hd += '</div></div></div></div>\n <!--hd end-->'

        return hd

    def item(self, item, option):
        it = '<< included item :' + item + ' >>'
        return it

    def wiki_link(self, text, link):

        # most likely a snippet so do first
        m = _reSnippet.match(link)
        if m is not None:
                snipType = m.group(1)
                snipId = m.group(2)
                url = '<span class= "cc-snip"'
                url += ' data-type = "' + snipType
                url += '" data-url = "' + self.url_for("displaySnip", index=self._index, id=snipId, type=snipType)
                url += '">[snip:' + snipType + ':' + snipId + '] </span>'
                return url
        return self.link(link, title="link to ", text=text)

    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        link = mistune.escape_link(link, quote=True)

        # If its a bare word then its an article to be rendered in the
        # current browser tab
        # If its full url its external and should be rendered in a
        # seperate browser tab
        # If its begins with a / then it should be fetched from the
        # static content store and rendered in another browser tab

        # TODO put in a friendly title and text if they are blank
        target = self._blank

        if not self.testmode:
            matchObj = _reUrl.match(link)
            if matchObj is None:
                matchObj = _reEmail.match(link)
                if matchObj is not None:
                    target = self._top  # emails shouldn't open new tab/window, at least not if we're using outlook
                else:
                    if ((len(link) > 0) and (link[0] != '/')):
                        title = u'title="{0}"'.format("link to article - scoping para here")
                        url = self.url_for("displayArticle", index=self._index, itemid=link.strip()).replace('%23', '#')
                        return u'<a {0} href="{1}" {2} >{3}</a>'.format(self._top, url, title, text)
                    else:
                        if len(self._static) > 0:
                            link = link.strip('/')
                        link = urlparse.urljoin(self._static, link[0:])

        if not title:
            return '<a%s href="%s">%s</a>' % (target, link, text)
        title = mistune.escape(title, quote=True)
        return '<a%s href="%s" title="%s">%s</a>' % (target, link, title, text)

    def image(self, src, title, alt_text):
        """Rendering a image with title and text.
        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        # TODO don't understand why the next 2 lines are different from the original mistune
        src = mistune.escape_link(src, quote=True)
        if src.lower().startswith('javascript:'):
            src = ''

        matchObj = _reUrl.match(src)
        # TODO originally relative images were relative to an image directory,
        # and did not have a leading /
        # TODO I am changing this so that relative paths for static server begin
        # with a / and are relative to the base url not an image directory
        # TODO the code that is to maintain compatibility will need to be
        # removed/changed once the content is re-exported from word.

        if matchObj is None:
            if ((len(src) > 0) and (src[0] != '/')):
                src = urlparse.urljoin(self._static, posixpath.join(self._images, src))
            else:
                src = urlparse.urljoin(self._static, src[1:])

        text = mistune.escape(alt_text, quote=True)
        if title:
            title = mistune.escape(title, quote=True)
            html = '<img%ssrc="%s" alt="%s" title="%s"' % (self._img, src, text, title)
        else:
            html = '<img%ssrc="%s" alt="%s"' % (self._img, src, text)
        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html


class InlineGrammar(mistune.InlineGrammar):
    wiki_link = re.compile(r'\[\[\s*([\S]+?)(?:\s*(?:\|| )([\s\S]+?))?\]\]')               # [[ link|text ]]
    # pc corres indicators are actually <<.*>> but I think I can get away with just escaping the leading << - johnp
    corres_tag = re.compile(r'<<')
    spanFormat = re.compile(r'^\!(\S)\!([\s\S]+?)\!:\!(?!\!)')
    anchor = re.compile(r'^\!\!\(([a-z,0-9]*)\)')


class InlineLexer(mistune.InlineLexer):
    default_rules = copy.copy(mistune.InlineLexer.default_rules)

    default_rules.insert(1, 'wiki_link')
    default_rules.insert(1, 'corres_tag')
    default_rules.insert(1, 'spanFormat')
    default_rules.insert(1, 'anchor')

    def __init__(self, renderer, rules=None, **kwargs):
        if rules is None:
            # use the inline grammar
            rules = InlineGrammar()
        super(InlineLexer, self).__init__(renderer, rules, **kwargs)

    def output_wiki_link(self, m):
        link = m.group(1)
        if m.group(2) is None:
            text = link
        else:
            text = m.group(2)
        return self.renderer.wiki_link(text, link)

    def output_corres_tag(self, m):
        return "&lt&lt"

    def output_spanFormat(self, m):
        style = styles("span", m.group(1))
        text = m.group(2)
        text = self.output(text)
        return self.renderer.spanFormat(style, text)

    def output_anchor(self, m):
        name = m.group(1)
        return self.renderer.anchor(name)


class BlockGrammar(mistune.BlockGrammar):
    blk = re.compile(r'(?:^|\n){{blk!([a-zA-Z0-9-_]+):\s*\n([\s\S]*?)\n(?:blk!\1)}}[^\n]*(?:\n|$)')
    box = re.compile(r'(?:^|\n){{((box|graph)(?:![a-z]+)?):[ \t]*([a-zA-Z0-9 \t]*)\n([\s\S]*?)\n(?:\1)}}[^\n]*(?:\n|$)')
    drop = re.compile(r'(?:^|\n){{(drop\!?(?:(?<=\!)([_a-z0-9]+))?):[ \t]*([a-zA-Z0-9 \t]*)\n([^\n]*)\n([\s\S]*?)\n\1}}[^\n]*(?:\n|$)')
    # item = re.compile(r'(?:^|\n){{item:[ \t]*([\S]+)\s*(\S*)?\s*}}[^\n]*(?:\n|$)')


class BlockLexer(mistune.BlockLexer):
    default_rules = copy.copy(mistune.BlockLexer.default_rules)
    default_rules.insert(1, 'box')
    default_rules.insert(1, 'blk')
    default_rules.insert(1, 'drop')
    # d efault_rules.insert(1,'item')
    default_rules.insert(1, 'box')

    def __init__(self, rules=None, **kwargs):
        if rules is None:
            # use the inline grammar
            rules = BlockGrammar()
        super(BlockLexer, self).__init__(rules, **kwargs)

    # TODO test invalid input ?
    def parse_box(self, m):
        option = m.group(3)
        textstr = m.group(4)
        self.tokens.append({
            'type': m.group(2),
            'option': option,
            'text': textstr
        })

    def parse_blk(self, m):
        option = styles("block", m.group(1))
        textstr = m.group(2)
        self.tokens.append({
            'type': 'blk',
            'option': option,
            'text': textstr
        })

    def parse_item(self, m):
        option = m.group(2)
        item = m.group(1)
        self.tokens.append({
            'type': 'item',
            'option': option,
            'item': item
        })

    def parse_drop(self, m):
        if ((len(m.group(4)) > 0) and (len(m.group(5)) > 0)):
            textstr = (m.group(5))
            # TODO pre compile this
            r = re.compile(r'^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)')
            capt = r.match(m.group(4))

            if capt:
                level = len(capt.group(1))
                title = capt.group(2)
            else:
                level = 0
                title = m.group(4)

            self.tokens.append({
                'hdInd': m.group(2),
                'type': 'drop',
                'option': m.group(3),
                'level': level,
                'title': title,
                'text': textstr
            })

# fix for bug in mistune - submitted to lepture
    def parse_table(self, m):
        item = self._process_table(m)
        cells = re.sub(r' *\n$', '', m.group(3))
        cells = cells.split('\n')
        for i, v in enumerate(cells):
            v = re.sub(r'^ *\| *| *\| *$', '', v)
            cells[i] = re.split(r' *\| *', v)

        item['cells'] = cells
        self.tokens.append(item)


def markdown(text, escape=True, **kwargs):
    """Render markdown formatted text to html.

    :param text: markdown formatted text content.
    :param escape: if set to False, all html tags will not be escaped.
    :param use_xhtml: output with xhtml tags.
    :param hard_wrap: if set to True, it will use the GFM line breaks feature.
    :param parse_block_html: parse text only in block level html.
    :param parse_inline_html: parse text only in inline level html.
    """

    return Markdown(escape=escape, **kwargs)(text)
