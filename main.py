import re
import webbrowser

from ulauncher.api.client.EventListener import KeywordQueryEventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.action.ShowNotificationAction import \
    ShowNotificationAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|https)://',
        re.IGNORECASE
    )
    return re.match(regex, url) is not None

class OpenUrlExtension(Extension):

    def __init__(self):
        super(OpenUrlExtension, self).__init__()
        self.subscribe(KeywordQueryEventListener(), self.on_keyword_query)

    def on_keyword_query(self, event):
        query = event.get_argument()
        if not query or not is_valid_url(query):
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='Invalid URL',
                                    description='Please enter a valid URL starting with http:// or https://',
                                    on_enter=ShowNotificationAction("Invalid URL entered"))
            ])

        items = [
            ExtensionResultItem(icon='images/icon.png',
                                name='Open URL',
                                description='Press Enter to open: %s' % query,
                                on_enter=OpenUrlAction(query))
        ]
        return RenderResultListAction(items)


if __name__ == '__main__':
    OpenUrlExtension().run()
