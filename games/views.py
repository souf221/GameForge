from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Game, Favorite

def game_list(request):
    games = Game.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'games/game_list.html', {'games': games})

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, game=game).exists()
    return render(request, 'games/game_detail.html', {
        'game': game,
        'is_favorite': is_favorite
    })

@login_required
def toggle_public(request, game_id):
    game = get_object_or_404(Game, id=game_id, creator=request.user)
    game.is_public = not game.is_public
    game.save()
    messages.success(request, f'Le jeu est maintenant {"public" if game.is_public else "privé"}!')
    return redirect('games:game_detail', game_id=game.id)

@login_required
def toggle_favorite(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)
    
    if not created:
        favorite.delete()
        messages.success(request, 'Jeu retiré des favoris!')
    else:
        messages.success(request, 'Jeu ajouté aux favoris!')
    
    return redirect('games:game_detail', game_id=game.id)

def search_games(request):
    query = request.GET.get('q', '')
    if query:
        games = Game.objects.filter(
            Q(title__icontains=query) |
            Q(genre__icontains=query) |
            Q(ambiance__icontains=query) |
            Q(keywords__icontains=query),
            is_public=True
        ).order_by('-created_at')
    else:
        games = Game.objects.filter(is_public=True).order_by('-created_at')
    
    return render(request, 'games/search_results.html', {
        'games': games,
        'query': query
    })
