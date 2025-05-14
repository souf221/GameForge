from django import forms
from games.models import Game

class GameGenerationForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'genre', 'ambiance', 'description', 'gameplay', 'story', 'characters', 'environment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Décrivez brièvement votre jeu...'}),
            'gameplay': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Décrivez les mécaniques de jeu principales...'}),
            'story': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Racontez l\'histoire de votre jeu...'}),
            'characters': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Décrivez les personnages principaux...'}),
            'environment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Décrivez l\'univers et l\'environnement...'}),
        } 