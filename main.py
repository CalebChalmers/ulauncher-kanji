from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction as ResultList
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem as Result

from kanjidic2 import parse as parse_kanjidic2
import os.path as path


class KanjiExtension(Extension):
    def __init__(self):
        super().__init__()
        kanjidic2_path = path.join(path.dirname(path.realpath(__file__)), 'kanjidic2.xml')
        self.kanji_to_info, self.meaning_to_kanji = parse_kanjidic2(kanjidic2_path)
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension: KanjiExtension):
        query = event.get_argument().strip().lower()
        kanji_to_info = extension.kanji_to_info
        meaning_to_kanji = extension.meaning_to_kanji
        icon = 'images/icon.png'

        if query in kanji_to_info:
            kanji = query
            kanji_info = kanji_to_info[kanji]
            open_jisho_action = OpenUrlAction('https://jisho.org/search/%23kanji%20' + kanji)
            meanings = ', '.join(kanji_info['meanings'])
            kunyomi = ', '.join(kanji_info['kunyomi'])
            onyomi = ', '.join(kanji_info['onyomi'])

            return ResultList([
                Result(icon=icon, name=kanji, description=meanings, on_enter=open_jisho_action),
                Result(icon=icon, name=kunyomi, description='Kun\'yomi', on_enter=open_jisho_action),
                Result(icon=icon, name=onyomi, description='On\'yomi', on_enter=open_jisho_action)
            ])

        if query in meaning_to_kanji:
            kanji_list = meaning_to_kanji[query]
            results = []

            for kanji in kanji_list:
                other_meanings = ', '.join(kanji_to_info[kanji]['meanings'])
                action = SetUserQueryAction(extension.preferences['keyword'] + ' ' + kanji)
                results.append(Result(icon=icon, name=kanji, description=other_meanings, on_enter=action))

            return ResultList(results)

        return ResultList([
            Result(icon=icon, name='No result found', description='', on_enter=DoNothingAction())
        ])


if __name__ == '__main__':
    KanjiExtension().run()