import webbrowser

from ulauncher.api.client.EventListener import KeywordQueryEventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class OpenUrlExtension(Extension):

    def __init__(self):
        super(OpenUrlExtension, self).__init__()
        self.subscribe(KeywordQueryEventListener(), self.on_keyword_query)

    def on_keyword_query(self, event):
        # Default URL if none provided
        query = event.get_argument() or 'https://github.com/Doug821/website-launcher'
        items = [
            ExtensionResultItem(icon='images/icon.png',
                                name='Open URL',
                                description='Press Enter to open: %s' % query,
                                on_enter=OpenUrlAction(query))
        ]
        return RenderResultListAction(items)


if __name__ == '__main__':
    OpenUrlExtension().run()
