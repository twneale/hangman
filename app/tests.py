from django.test import TestCase

from app.models import GameState


class TestGameActions(TestCase):

    def test_use_lost(self):
        '''Verify that the game fails when the player exceeds the
        max number of failed guesses.
        '''
        game = GameState.objects.create(word="sowpod", guessed="xyvqulktmn")
        self.assertTrue(game.user_lost())

    def test_user_won(self):
        '''Verify that the user wins when the all the letters are guessed.
        '''
        game = GameState.objects.create(word="sowpod", guessed="sowpod")
        self.assertTrue(game.user_won())

    def test_remaining_tries(self):
        '''Verify the remaining tries is correctly calculated.
        '''
        # Start with 10 tries available.
        game = GameState.objects.create(word="sowpod")
        self.assertEqual(game.remaining_tries(), 10)

        # A wrong guess decrements the number of tries.
        game.guess('x')
        self.assertEqual(game.remaining_tries(), 9)

        # Confirm that wrong guesses are idempotent.
        game.guess('x')
        self.assertEqual(game.remaining_tries(), 9)

        # A correct guess doesn't affect the number of tries remaining.
        game.guess('s')
        self.assertEqual(game.remaining_tries(), 9)

    def test_complete(self):
        '''Verify that Game.complete helper works as expected.
        '''
        # Incomplete game.
        game = GameState.objects.create(word="sowpod")
        self.assertFalse(game.complete())

        # Complete game.
        game = GameState.objects.create(word="sowpod", guessed='sowpod')
        self.assertTrue(game.complete())

    def test_successful_guesses(self):
        '''Verify that Game.successful_guesses helper works as expected.
        '''
        # Complete game.
        game = GameState.objects.create(word="sowpod", guessed='sowpxyz')
        self.assertEqual(game.successful_guesses(), set('sowp'))

    def test_failed_guesses(self):
        '''Verify that Game.failed_guesses helper works as expected.
        '''
        # Complete game.
        game = GameState.objects.create(word="sowpod", guessed='sowpxyz')
        self.assertEqual(game.failed_guesses(), set('xyz'))
