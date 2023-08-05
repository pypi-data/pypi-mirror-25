from __future__ import unicode_literals

import re
import unicodedata
from collections import deque

import lxml.html
import lxml.html.clean


__all__ = ('Sanitizer',)


def sanitize_href(href):
    """
    Verify that a given href is benign and allowed.

    This is a stupid check, which probably should be much more elaborate
    to be safe.
    """
    if href.startswith(
        ('/', 'mailto:', 'http:', 'https:', '#', 'tel:')
    ):
        return href
    return '#'


def bold_span_to_strong(element):
    if element.tag == 'span' and 'bold' in element.get('style', ''):
        element.tag = 'strong'
    return element


def italic_span_to_em(element):
    if element.tag == 'span' and 'italic' in element.get('style', ''):
        element.tag = 'em'
    return element


def tag_replacer(from_, to_):
    def replacer(element):
        if element.tag == from_:
            element.tag = to_
        return element
    return replacer


DEFAULT_SETTINGS = {
    'tags': {
        'a',
        'h1',
        'h2',
        'h3',
        'strong',
        'em',
        'p',
        'ul',
        'ol',
        'li',
        'br',
        'sub',
        'sup',
        'hr',
    },
    'attributes': {
        'a': ('href', 'name', 'target', 'title', 'id'),
    },
    'empty': {'hr', 'a', 'br'},
    'separate': {'a', 'p', 'li'},
    'add_nofollow': False,
    'autolink': False,
    'sanitize_href': sanitize_href,
    'element_preprocessors': [
        # convert span elements into em/strong if a matching style rule
        # has been found. strong has precedence, strong & em at the same
        # time is not supported
        bold_span_to_strong,
        italic_span_to_em,
        tag_replacer('b', 'strong'),
        tag_replacer('i', 'em'),
    ],
    'element_postprocessors': [
    ],
}


class Sanitizer(object):
    def __init__(self, settings=None):
        self.__dict__.update(DEFAULT_SETTINGS)
        self.__dict__.update(settings or {})

        # Validate the settings.
        if not self.tags.issuperset(self.empty):
            raise TypeError('Tags in "empty", but not allowed: %r' % (
                self.empty - self.tags,
            ))
        if not self.tags.issuperset(self.separate):
            raise TypeError('Tags in "separate", but not allowed: %r' % (
                self.separate - self.tags,
            ))
        if not self.tags.issuperset(self.attributes.keys()):
            raise TypeError('Tags in "attributes", but not allowed: %r' % (
                set(self.attributes.keys()) - self.tags,
            ))

    def sanitize(self, html):
        """
        Clean HTML code from ugly copy-pasted CSS and empty elements

        Removes everything not explicitly allowed in ``self.allowed_tags``.

        Requires ``lxml`` and, for especially broken HTML, ``beautifulsoup4``.
        """

        # remove all sorts of newline and nbsp characters
        whitespace = [
            '\n', '&#10;', '&#xa;',
            '\r', '&#13;', '&#xd;',
            '\xa0', '&nbsp;', '&#160;', '&#xa0',
        ]
        for ch in whitespace:
            html = html.replace(ch, ' ')
        html = re.sub(r'(?u)\s+', ' ', html)

        html = '<div>%s</div>' % html
        try:
            doc = lxml.html.fromstring(html)
            lxml.html.tostring(doc, encoding='utf-8')
        except:
            from lxml.html import soupparser
            doc = soupparser.fromstring(html)

        lxml.html.clean.Cleaner(
            remove_unknown_tags=False,
            # Remove style *tags*
            style=True,
            # Do not strip out style attributes; we still need the style
            # information to convert spans into em/strong tags
            safe_attrs_only=False,
            inline_style=False,
            add_nofollow=self.add_nofollow,
        )(doc)

        # walk the tree recursively, because we want to be able to remove
        # previously emptied elements completely
        backlog = deque(doc.iterdescendants())
        while True:
            try:
                element = backlog.pop()
            except IndexError:
                break

            for processor in self.element_preprocessors:
                element = processor(element)

            whitespace_re = re.compile(r'^\s*$')
            if element.text or element.tail:
                # remove elements containing only whitespace or linebreaks
                if element.text:
                    while True:
                        text = whitespace_re.sub('', element.text)
                        if element.text == text:
                            break
                        element.text = text

                if element.tail:
                    while True:
                        text = whitespace_re.sub(' ', element.tail)
                        if element.tail == text:
                            break
                        element.tail = text

            # remove empty tags if they are not explicitly allowed
            if (not element.text and
                    element.tag not in self.empty and
                    not len(element)):
                element.drop_tag()
                continue

            if (whitespace_re.match(element.text or '') and
                    {e.tag for e in element} == {'br'} and
                    all(whitespace_re.match(e.tail or '') for e in element)):
                element.drop_tree()
                continue

            elif element.tag == 'li':
                # remove p-in-li tags
                for p in element.findall('p'):
                    if getattr(p, 'text', None):
                        p.text = ' ' + p.text + ' '
                    p.drop_tag()

                # remove list markers
                if element.text:
                    element.text = re.sub(
                        r'^(\&nbsp;|\&#160;|\s)*(-|\*|&#183;)(\&nbsp;|\&#160;|\s)+',  # noqa
                        '',
                        element.text)

            elif element.tag == 'br':
                nx = element.getnext()
                if nx is not None and nx.tag == 'br' and not element.tail:
                    nx.drop_tag()
                    continue

                # Drop <br/>'s at the beginning of parents.
                parent = element.getparent()
                if (parent is not None and
                        element.getprevious() is None and
                        whitespace_re.match(parent.text or '')):  # noqa
                    element.drop_tag()

            if not element.text:
                first = list(element)[0] if list(element) else None
                if first is not None and first.tag == 'br':
                    first.drop_tag()

            if element.tag in (self.tags - self.separate - self.empty):
                nx = element.getnext()
                if (whitespace_re.match(element.tail or '') and
                        nx is not None and nx.tag == element.tag):
                    if nx.text:
                        if len(element):
                            list(element)[-1].tail = '%s %s' % (
                                list(element)[-1].tail or '',
                                nx.text,
                            )
                        else:
                            element.text = '%s %s' % (
                                element.text or '',
                                nx.text,
                            )

                    for child in nx:
                        element.append(child)

                    # tail is merged with previous element.
                    nx.drop_tree()

                    # Process element again
                    backlog.append(element)

            for processor in self.element_postprocessors:
                element = processor(element)

            # remove all attributes which are not explicitly allowed
            allowed = self.attributes.get(element.tag, [])
            for key in element.keys():
                if key not in allowed:
                    del element.attrib[key]

            # Clean hrefs so that they are benign
            href = element.get('href')
            if href is not None:
                element.set('href', self.sanitize_href(href))

        if self.autolink:
            lxml.html.clean.autolink(doc)
        elif isinstance(self.autolink, dict):
            lxml.html.clean.autolink(doc, **self.autolink)

        # just to be sure, run cleaner again, but this time with even more
        # strict settings
        lxml.html.clean.Cleaner(
            allow_tags=self.tags,
            remove_unknown_tags=False,
            safe_attrs_only=True,
            add_nofollow=self.add_nofollow,
        )(doc)

        html = lxml.html.tostring(doc, encoding='unicode')

        # add a space before the closing slash in empty tags
        html = re.sub(r'<([^/>]+)/>', r'<\1 />', html)

        # remove wrapping tag needed by XML parser
        html = re.sub(r'^<div>|</div>$', '', html)

        # normalize unicode
        html = unicodedata.normalize('NFKC', html)

        return html
