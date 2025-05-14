from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GameGenerationForm
from games.models import Game
from .services import AIGameGenerator

def home(request):
    public_games = Game.objects.filter(is_public=True).order_by('-created_at')[:6]
    return render(request, 'core/home.html', {'public_games': public_games})

@login_required
def explore(request):
    public_games = Game.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'core/explore.html', {'games': public_games})

@login_required
def generate_game(request):
    if request.method == 'POST':
        form = GameGenerationForm(request.POST)
        if form.is_valid():
            try:
                # Récupération des données du formulaire
                title = form.cleaned_data['title']
                genre = form.cleaned_data['genre']
                ambiance = form.cleaned_data['ambiance']

                # Génération du contenu avec l'IA
                ai_generator = AIGameGenerator()
                generated_content = ai_generator.generate_game_content(title, genre, ambiance)

                # Création du jeu avec le contenu généré
                game = form.save(commit=False)
                game.user = request.user
                game.description = generated_content['description']
                game.gameplay = generated_content['gameplay']
                game.story = generated_content['story']
                game.characters = generated_content['characters']
                game.environment = generated_content['environment']
                game.save()

                messages.success(request, 'Votre jeu a été généré avec succès!')
                return redirect('games:game_detail', game.id)

            except Exception as e:
                messages.error(request, f'Erreur lors de la génération : {str(e)}')
                return render(request, 'core/generate_game.html', {'form': form})
    else:
        form = GameGenerationForm()
    
    return render(request, 'core/generate_game.html', {'form': form})

@login_required
def generate_random(request):
    # Logique de génération aléatoire
    return render(request, 'core/generate_random.html')
