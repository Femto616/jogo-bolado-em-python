#joguinho em python

from typing import List, Dict
import random

# Tuplas para dados fixos (categorias/status)
CLASSES = ('Guerreiro', 'Mago', 'Arqueiro')
STATUS = ('Ativo', 'Inativo')

# Lista global para armazenar jogadores
jogadores: List['Player'] = []

# Itens disponíveis na loja
LOJA = [
    {'id': 1, 'nome': 'Poção de Vida', 'preco': 10},
    {'id': 2, 'nome': 'Espada Curta', 'preco': 25},
    {'id': 3, 'nome': 'Cajado Místico', 'preco': 30},
    {'id': 4, 'nome': 'Arco Rústico', 'preco': 20}
]


# -------
# Classes e Herança
# -------
class Person:
    """Classe base para personagens (herdável)."""
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self._idade = idade  # atributo privado/protegido

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
        self.status = STATUS[0]  # padrão: 'Ativo'


class Player(Character):
    """Jogador com atributos privados, property e histórico de ações."""
    def __init__(self, nome: str, idade: int, classe: str):
        super().__init__(nome, idade, classe)
        self._level = 1
        self.experiencia = 0
        self.inventario: List[Dict] = []
        self.registros: List[str] = []  # registros (compras, batalhas, etc.)

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
        # sobe de nível a cada 100 XP
        while self.experiencia >= 100:
            self.experiencia -= 100
            self.level += 1
            self.registros.append("Subiu de nível!")

    def comprar(self, item: Dict):
        if item in self.inventario:
            # permitir multiplas cópias
            pass
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
        # retorna força de ataque baseada no poder + aleatório
        return self.poder + random.randint(0, 5)



# Funções do sistema (cada ação em uma função)

def cadastrar_jogador():
    try:
        nome = input("Nome do jogador: ").strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        idade = int(input("Idade: ").strip())
        print("Classes disponíveis:", ', '.join(CLASSES))
        classe = input("Escolha a classe: ").strip().title()
        if classe not in CLASSES:
            raise ValueError("Classe inválida.")
        novo = Player(nome, idade, classe)
        jogadores.append(novo)
        print(f"Jogador '{nome}' cadastrado com sucesso!")
    except ValueError as e:
        print(f"Erro ao cadastrar: {e}")
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)


def listar_jogadores():
    if not jogadores:
        print("Nenhum jogador cadastrado.")
        return
    print("\n--- Lista de Jogadores ---")
    for idx, p in enumerate(jogadores, 1):
        print(f"{idx}. {p}")
    print("--------------------------")


def buscar_jogador_por_nome(nome: str) -> Player:
    for p in jogadores:
        if p.nome.lower() == nome.lower():
            return p
    raise LookupError("Jogador não encontrado.")


def consultar_jogador():
    try:
        nome = input("Nome do jogador para consultar: ").strip()
        p = buscar_jogador_por_nome(nome)
        print(f"\n--- Perfil de {p.nome} ---")
        print(p)
        print("Inventário:")
        if p.inventario:
            for it in p.inventario:
                print(f" - {it['nome']} (preço: {it['preco']})")
        else:
            print(" (vazio)")
        print("Registros (últimos 10):")
        for r in p.registros[-10:]:
            print("  >", r)
        print("------------------------")
    except LookupError as e:
        print(e)
    except Exception as e:
        print("Erro:", e)


def editar_jogador():
    try:
        nome = input("Nome do jogador para editar: ").strip()
        p = buscar_jogador_por_nome(nome)
        print("Deixe em branco para manter o valor atual.")
        novo_nome = input(f"Novo nome (atual: {p.nome}): ").strip()
        if novo_nome:
            p.nome = novo_nome
        nova_idade = input(f"Nova idade (atual: {p.idade}): ").strip()
        if nova_idade:
            p.idade = int(nova_idade)
        print("Classes:", ', '.join(CLASSES))
        nova_classe = input(f"Nova classe (atual: {p.classe}): ").strip().title()
        if nova_classe:
            if nova_classe not in CLASSES:
                raise ValueError("Classe inválida.")
            p.classe = nova_classe
        print("Jogador atualizado.")
    except LookupError as e:
        print(e)
    except ValueError as e:
        print("Valor inválido:", e)
    except Exception as e:
        print("Erro inesperado:", e)


def excluir_jogador():
    try:
        nome = input("Nome do jogador para excluir: ").strip()
        p = buscar_jogador_por_nome(nome)
        jogadores.remove(p)
        print(f"Jogador '{nome}' removido.")
    except LookupError as e:
        print(e)
    except Exception as e:
        print("Erro:", e)


def mostrar_loja():
    print("\n--- Loja ---")
    for item in LOJA:
        print(f"{item['id']}. {item['nome']} - Preço: {item['preco']}")
    print("------------")


def comprar_item():
    try:
        nome = input("Nome do jogador que vai comprar: ").strip()
        p = buscar_jogador_por_nome(nome)
        mostrar_loja()
        escolha = int(input("ID do item que deseja comprar: ").strip())
        item = next((it for it in LOJA if it['id'] == escolha), None)
        if item is None:
            raise LookupError("Item não encontrado.")
        p.comprar(item)
        print(f"{p.nome} comprou {item['nome']}.")
    except LookupError as e:
        print(e)
    except ValueError:
        print("Entrada inválida. Use um número para ID.")
    except Exception as e:
        print("Erro:", e)


def batalhar():
    """Simula uma batalha simples entre jogador e NPC."""
    try:
        nome = input("Nome do jogador que vai batalhar: ").strip()
        p = buscar_jogador_por_nome(nome)
        # Criar um NPC aleatório
        npc = NPC("Goblin", random.randint(10, 40), random.choice(CLASSES), poder=random.randint(1, 8))
        print(f"{p.nome} (Level {p.level}) vs {npc.nome} (poder {npc.poder})")
        # Calcular quem é mais forte
        ataque_jogador = p.level + random.randint(0, 6)
        ataque_npc = npc.atacar_forca()
        print(f" - Força do jogador: {ataque_jogador}")
        print(f" - Força do inimigo: {ataque_npc}")
        if ataque_jogador >= ataque_npc:
            xp = random.randint(10, 40)
            p.ganhar_xp(xp)
            p.registros.append(f"Venceu batalha contra {npc.nome} (+{xp} XP).")
            print(f"Vitória! {p.nome} ganhou {xp} XP.")
        else:
            p.registros.append(f"Perdeu para {npc.nome}.")
            print("Derrota... tente de novo.")
    except LookupError as e:
        print(e)
    except Exception as e:
        print("Erro:", e)


def mostrar_menu():
    print("""
=== Jogo: Aventura & Loja ===
1 - Cadastrar jogador
2 - Listar jogadores
3 - Consultar jogador
4 - Editar jogador
5 - Excluir jogador
7 - Comprar item
8 - Batalhar
9 - Sair
=============================
""")


def main():
    while True:
        try:
            mostrar_menu()
            escolha = input("Escolha uma opção: ").strip()
            if escolha == '1':
                cadastrar_jogador()
            elif escolha == '2':
                listar_jogadores()
            elif escolha == '3':
                consultar_jogador()
            elif escolha == '4':
                editar_jogador()
            elif escolha == '5':
                excluir_jogador()
            elif escolha == '6':
                mostrar_loja()
            elif escolha == '7':
                comprar_item()
            elif escolha == '8':
                batalhar()
            elif escolha == '9':
                print("Saindo... obrigado por jogar!")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário. Saindo.")
            break
        except Exception as e:
            print("Erro inesperado no menu:", e)


if __name__ == "__main__":
    main()