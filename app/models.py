import re
import datetime

from django.db import models


class GameState(models.Model):

    MAX_GUESSES = 10

    word = models.CharField(max_length=6)
    guessed = models.CharField(max_length=15, default='')
    created = models.DateTimeField(default=datetime.datetime.utcnow)

    # ------------------------------------------------------------------
    # Template/view helpers.
    # ------------------------------------------------------------------
    def word_masked(self):
        return '*' * len(self.word)

    def table_row_class(self):
        if self.user_won():
            return 'success'
        elif self.user_lost():
            return 'danger'
        else:
            return 'info'

    def remaining_tries(self):
        return self.MAX_GUESSES - len(self.failed_guesses())

    def remaining_tries_percent(self):
        return self.remaining_tries() * 10

    def remaining_try_css(self):
        remaining = self.remaining_tries()
        if 8 < remaining <= 10:
            return 'success'
        if 6 < remaining <= 8:
            return 'info'
        if 4 < remaining <= 6:
            return 'warning'
        if 0 <= remaining <= 4:
            return 'danger'

    def guess(self, letter):
        self.guessed = self.guessed + letter
        self.save()
        return letter in self.word

    def failed_guesses(self):
        return set(self.guessed) - set(self.word)

    def successful_guesses(self):
        return set(self.guessed) & set(self.word)

    def user_won(self):
        if set(self.word).issubset(set(self.guessed)):
            return True

    def user_lost(self):
        if self.MAX_GUESSES <= len(self.failed_guesses()):
            return True

    def complete(self):
        return self.user_won() or self.user_lost()

    def hogan_ctx(self):
        '''Return the json required by the hogan template.
        '''
        words = []
        for letter in self.word:
            if letter in self.guessed:
                css = 'success'
            else:
                css = 'default'
                letter = '_'
            words.append(dict(letter=letter, css=css))

        ctx = {
            'remaining_tries': self.remaining_tries(),
            'remaining_try_css': self.remaining_try_css(),
            'remaining_tries_percent': self.remaining_tries_percent(),
            'hangman_picture': self.hangman_picture(),
            'failed_guesses': [{'letter': c} for c in self.failed_guesses()],
            'worddata': words,
            }
        return ctx

    def hangman_picture(self):
        '''Hangman ascii inspired by this: http://ascii.co.uk/art/hangman
        '''
        failed = len(self.failed_guesses())
        if failed is 0:
            return '''







    _____
 '''
        if failed is 1:
            return '''

     |
     |
     |
     |
     |
     |
    _|___
'''
        if failed is 2:
            return '''
      _______
     |/
     |
     |
     |
     |
     |
    _|___
'''

        if failed is 3:
            return u'''
      _______
     |/      |
     |
     |
     |
     |
     |
    _|___
'''

        if failed is 4:
            return u'''
      _______
     |/      |
     |       \u2639
     |
     |
     |
     |
    _|___
'''

        if failed is 5:
            return u'''
      _______
     |/      |
     |       \u2639
     |       |
     |
     |
     |
    _|___
 '''
        if failed is 6:
            return u'''
      _______
     |/      |
     |       \u2639
     |       |
     |       |
     |
     |
    _|___
 '''

        if failed is 7:
            return u'''
      _______
     |/      |
     |       \u2639
     |      \|
     |       |
     |
     |
    _|___
'''

        if failed is 8:
            return u'''
      _______
     |/      |
     |       \u2639
     |      \|/
     |       |
     |
     |
    _|___
 '''

        if failed is 9:
            return u'''
      _______
     |/      |
     |       \u2639
     |      \|/
     |       |
     |      /
     |
    _|___
 '''

        if failed is 10:
            return u'''
      _______
     |/      |
     |       \u2639
     |      \|/
     |       |
     |      / \\
     |
    _|___
 '''
        # Should never get here.
        raise Exception()
