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

ICON_PATH = 'images/icon.png'
DEFAULT_URL_PROTOCOL = 'http://'


def format_url(url):
    if not url.startswith(('http://', 'https://')):
        url = DEFAULT_URL_PROTOCOL + url
    return url


def open_url(url):
    webbrowser.open_new_tab(format_url(url))


class OpenUrlExtension(Extension):
    def __init__(self):
        super(OpenUrlExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ''
        items = [
            ExtensionResultItem(
                icon='images/icon.png',
                name='Open URL',
                description='Press Enter to open: {}'.format(query),
                on_enter=ExtensionCustomAction(query)
            )
        ]

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_data() or ''
        if not query.startswith(('http://', 'https://')):
            query = 'http://' + query
        open_url(query)


if __name__ == '__main__':
    OpenUrlExtension().run()
