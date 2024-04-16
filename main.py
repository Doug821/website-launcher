import webbrowser

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class OpenWebsiteExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        # Retrieve URL from extension preferences
        url = extension.preferences['website_url']
        items = [
            ExtensionResultItem(icon='images/icon.png',
                                name='Open Website',
                                description='Click to open your configured website: {}'.format(url),
                                on_enter=OpenUrlAction(url))
        ]

        return RenderResultListAction(items)

if __name__ == '__main__':
    OpenWebsiteExtension().run()
