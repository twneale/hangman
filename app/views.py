import json
import random

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.template import RequestContext
from django.contrib import messages
from django.middleware.csrf import get_token

from app.models import GameState


with open(settings.WORD_LIST) as f:
    word_list = json.load(f)


def home(request):
    games = GameState.objects.order_by('-created')[:50]
    ctx = dict(games=list(games))
    return render(request, "home.html", ctx)


def new_game(request):
    word = random.choice(word_list).upper()
    game = GameState.objects.create(word=word)
    ctx = dict(game=game)
    request.session['game_id'] = game.id
    return redirect('game')


def resume_game(request, game_id):
    game = GameState.objects.get(id=game_id)
    ctx = dict(game=game)
    request.session['game_id'] = game.id
    return redirect('game')


def messages_ctx(request):
    messages = []
    for message in RequestContext(request)['messages']:
        message = dict(tags=message.tags, message=message.message)
        messages.append(message)
    return messages


def game(request):
    game_id = request.session['game_id']
    game = GameState.objects.get(id=game_id)
    ctx = dict(game=game)
    return render(request, "game.html", ctx)


class GameJson(FormView):

    def get(self, request):
        game_id = request.session['game_id']
        game = GameState.objects.get(id=game_id)
        ctx = dict(
            game=game.hogan_ctx(),
            messages=[])
        response = HttpResponse(content_type='application/json')
        json.dump(ctx, response)
        return response

    def post(self, request):
        letter = request.POST['letter'].upper()
        game_id = request.session['game_id']
        game = GameState.objects.get(id=game_id)

        if letter in game.guessed:
            msg = 'Silly goose, you already guessed "%s"'
            messages.info(request, msg % letter)
        else:
            succeeded = game.guess(letter)
            if succeeded:
                # Check if the user won.
                if game.user_won():
                    ctx = dict(victory=True)
                    response = HttpResponse(content_type='application/json')
                    json.dump(ctx, response)
                    return response
                else:
                    msg = 'Success! The letter "%s" appears in the this word %d times.'
                    args = (letter, game.word.count(letter))
                    messages.success(request, msg % args)
            else:
                # Check if the user lost.
                if game.user_lost():
                    ctx = dict(failure=True)
                    response = HttpResponse(content_type='application/json')
                    json.dump(ctx, response)
                    return response
                else:
                    msg = "D'oh! The word doesn't contain \"%s\"."
                    messages.warning(request, msg % letter)

        ctx = dict(
            game=game.hogan_ctx(),
            messages=messages_ctx(request))
        response = HttpResponse(content_type='application/json')
        json.dump(ctx, response)
        return response


game_json = GameJson.as_view()


def failure(request):
    request.session['losses'] = request.session.get('losses', 0) + 1
    game_id = request.session['game_id']
    game = GameState.objects.get(id=game_id)
    ctx = dict(game=game)
    return render(request, "failure.html", ctx)


def victory(request):
    request.session['wins'] = request.session.get('wins', 0) + 1
    game_id = request.session['game_id']
    game = GameState.objects.get(id=game_id)
    ctx = dict(game=game)
    return render(request, "victory.html", ctx)