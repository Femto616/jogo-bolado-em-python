from typing import List, Dict
import random
from data import CLASSES, STATUS

# ------- Classes -------

class Person:
    """Classe base para personagens (herdável)."""
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self._idade = idade

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("Idade deve ser inteiro >= 0.")
        self._idade = valor


class Character(Person):
    """Classe intermediária para atributos comuns de personagem."""
    def __init__(self, nome: str, idade: int, classe: str):
        super().__init__(nome, idade)
        if classe not in CLASSES:
            raise ValueError(f"Classe inválida. Opções: {CLASSES}")
        self.classe = classe
        self.status = STATUS[0]


class Player(Character):
    """Jogador com atributos privados, property e histórico de ações."""
    def __init__(self, nome: str, idade: int, classe: str):
        super().__init__(nome, idade, classe)
        self._level = 1
        self.experiencia = 0
        self.inventario: List[Dict] = []
        self.registros: List[str] = []

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, novo):
        if not isinstance(novo, int) or novo < 1:
            raise ValueError("Level deve ser inteiro >= 1.")
        self._level = novo

    def ganhar_xp(self, xp: int):
        if xp < 0:
            raise ValueError("XP inválido.")
        self.experiencia += xp
        self.registros.append(f"Ganhou {xp} XP.")
        while self.experiencia >= 100:
            self.experiencia -= 100
            self.level += 1
            self.registros.append("Subiu de nível!")

    def comprar(self, item: Dict):
        self.inventario.append(item)
        self.registros.append(f"Comprou {item['nome']} por {item['preco']} moedas.")

    def __str__(self):
        return (f"{self.nome} | Classe: {self.classe} | Level: {self.level} | "
                f"XP: {self.experiencia} | Itens: {len(self.inventario)}")


class NPC(Character):
    """Inimigos simples (subclasse de Character)."""
    def __init__(self, nome: str, idade: int, classe: str, poder: int):
        super().__init__(nome, idade, classe)
        self.poder = poder

    def atacar_forca(self):
        return self.poder + random.randint(0, 5)
