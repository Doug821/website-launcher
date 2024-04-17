import webbrowser

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import \
    ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from bookmark_manager import add_bookmark, load_bookmarks
from constants import DEFAULT_URL_PROTOCOL, ICON_PATH


def format_query(query):
    if not query.startswith(('http://', 'https://')):
        query = DEFAULT_URL_PROTOCOL + query
    return query


class OpenUrlExtension(Extension):
    def __init__(self):
        super(OpenUrlExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument()
        bookmarks = load_bookmarks()
        items = []

        if not query:
            if bookmarks:
                for url in bookmarks.items():
                    items.append(ExtensionResultItem(
                        icon=ICON_PATH,
                        name='Open Bookmark: ' + url,
                        description='URL: ' + url,
                        on_enter=ExtensionCustomAction(url)
                    ))
            else:
                items.append(ExtensionResultItem(
                    icon=ICON_PATH,
                    name='No bookmarks found',
                    description='Add a bookmark to open a URL'
                ))
        else:
            items.append(self.create_result_item(query))
            items.append(ExtensionResultItem(
                icon=ICON_PATH,
                name='Bookmark this URL',
                description='Press Enter to bookmark: {}'.format(query),
                on_enter=ExtensionCustomAction(
                    ('bookmark', query), keep_app_open=False)
            ))
        return RenderResultListAction(items)

    @staticmethod
    def create_result_item(query):
        return ExtensionResultItem(
            icon=ICON_PATH,
            name='Open URL',
            description='Press Enter to open: {}'.format(query),
            on_enter=ExtensionCustomAction(query)
        )


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        if isinstance(data, tuple) and data[0] == 'bookmark':
            add_bookmark(data[1])
            return HideWindowAction()

        query = data or ''
        formatted_query = format_query(query)
        webbrowser.open_new_tab(formatted_query)


if __name__ == '__main__':
    OpenUrlExtension().run()
