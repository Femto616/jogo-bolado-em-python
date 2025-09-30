from typing import List
from models import Player

CLASSES = ('Guerreiro', 'Mago', 'Arqueiro')
STATUS = ('Ativo', 'Inativo')

# Lista global de jogadores
jogadores: List[Player] = []

# Loja
LOJA = [
    {'id': 1, 'nome': 'Poção de Vida', 'preco': 10},
    {'id': 2, 'nome': 'Espada Curta', 'preco': 25},
    {'id': 3, 'nome': 'Cajado Místico', 'preco': 30},
    {'id': 4, 'nome': 'Arco Rústico', 'preco': 20}
]
