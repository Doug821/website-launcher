# bookmark_manager.py
import json
import os

from constants import BOOKMARKS_FILE


def load_bookmarks():
    if not os.path.exists(BOOKMARKS_FILE):
        return {}
    with open(BOOKMARKS_FILE, 'r') as file:
        return json.load(file)


def save_bookmarks(bookmarks):
    with open(BOOKMARKS_FILE, 'w') as file:
        json.dump(bookmarks, file, indent=4)


def add_bookmark(url):
    bookmarks = load_bookmarks()
    bookmarks[url] = url
    save_bookmarks(bookmarks)


def remove_bookmark(url):
    bookmarks = load_bookmarks()
    if url in bookmarks:
        del bookmarks[url]
        save_bookmarks(bookmarks)
