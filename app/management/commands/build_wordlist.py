import os
import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Generate the wordlist the game will use.'

    sowpods_url = (
        'https://scrabblehelper.googlecode.com/svn-history/r20/trunk'
        '/ScrabbleHelper/src/dictionaries/sowpods.txt')

    def handle(self, *args, **options):
        words = requests.get(self.sowpods_url).text.splitlines()
        words = filter(lambda s: len(s) == 6, words)
        with open(settings.WORD_LIST, 'w') as f:
            json.dump(words, f)
