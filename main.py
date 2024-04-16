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
        webbrowser.open_new_tab(query)

if __name__ == '__main__':
    OpenUrlExtension().run()
