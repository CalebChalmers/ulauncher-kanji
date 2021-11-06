from xml.sax import parse as parse_sax
from xml.sax.handler import ContentHandler

def parse(path):
    handler = KanjiDic2Handler()
    parse_sax(path, handler)
    return handler.kanji_to_info, handler.meaning_to_kanji

class KanjiDic2Handler(ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.kanji_to_info = {}
        self.meaning_to_kanji = {}
        self.kanji = None
        self.kanji_info = None
        self.element_name = None
        self.element_attr = None

    def startElement(self, name, attrs):
        self.element_name = name
        self.element_attr = attrs

        if name == 'character':
            self.kanji = None
            self.kanji_info = {'meanings': [], 'kunyomi': [], 'onyomi': []}

    def endElement(self, name):
        self.element_name = None
        self.element_attr = None

        if name == 'character':
            self.kanji_to_info[self.kanji] = self.kanji_info
            for meaning in self.kanji_info['meanings']:
                key = meaning.lower()
                if key not in self.meaning_to_kanji:
                    self.meaning_to_kanji[key] = []
                self.meaning_to_kanji[key].append(self.kanji)

    def characters(self, content):
        if self.element_name == 'literal':
            self.kanji = content
        elif self.element_name == 'meaning':
            if 'm_lang' not in self.element_attr:
                self.kanji_info['meanings'].append(content)
        elif self.element_name == 'reading':
            if self.element_attr['r_type'] == 'ja_kun':
                self.kanji_info['kunyomi'].append(content)
            elif self.element_attr['r_type'] == 'ja_on':
                self.kanji_info['onyomi'].append(content)
