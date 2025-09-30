#joguinho em python
from typing import List, Dict
import random
import time  # <- import para delay

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


# ------- Classes e Herança -------
class Person:
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
    def __init__(self, nome: str, idade: int, classe: str):
        super().__init__(nome, idade)
        if classe not in CLASSES:
            raise ValueError(f"Classe inválida. Opções: {CLASSES}")
        self.classe = classe
        self.status = STATUS[0]


class Player(Character):
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
    def __init__(self, nome: str, idade: int, classe: str, poder: int):
        super().__init__(nome, idade, classe)
        self.poder = poder

    def atacar_forca(self):
        return self.poder + random.randint(0, 5)


# Jogadores pré-cadastrados
jogadores.extend([
    Player("Albino", 20, "Mago"),
    Player("Pitbull", 18, "Guerreiro"),
    Player("Xanxerê", 20, "Arqueiro")
])


# ------- Funções do sistema -------
def escolher_classe():
    while True:
        print("=== Escolha sua Classe ===")
        for i, c in enumerate(CLASSES, start=1):
            print(f"[{i}] {c}")
        try:
            escolha = int(input("Digite o número da classe: "))
            if 1 <= escolha <= len(CLASSES):
                return CLASSES[escolha - 1]  # retorna a classe correta
            else:
                print(f"Escolha inválida! Digite um número entre 1 e {len(CLASSES)}.")
        except ValueError:
            print("Entrada inválida! Digite apenas números.")


def cadastrar_jogador():
    try:
        nome = input("Nome do jogador: ").strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        idade = int(input("Idade: ").strip())
        classe = escolher_classe()  # chama a função com validação
        novo = Player(nome, idade, classe)
        jogadores.append(novo)
        print(f"Jogador '{nome}' cadastrado com !")
        listar_jogadores()
    except ValueError as e:
        print(f"Erro ao cadastrar: {e}")
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
    

def listar_jogadores():
    if not jogadores:
        print("Nenhum jogador cadastrado.")
        time.sleep(1)
        return
    print("\n--- Lista de Jogadores ---")
    for idx, p in enumerate(jogadores, 1):
        if isinstance(p, Player):
            print(f"{idx}. {p}")
        else:
            print(f"{idx}. [ERRO] Objeto inválido na lista: {p}")
        time.sleep(1)
    print("--------------------------")
    time.sleep(1)
    input("Aperte qualquer tecla pra continuar")


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
        time.sleep(1)
        print("Inventário:")
        if p.inventario:
            for it in p.inventario:
                print(f" - {it['nome']} (preço: {it['preco']})")
                time.sleep(0.5)
        else:
            print(" (vazio)")
            time.sleep(1)
        print("Registros (últimos 10):")
        for r in p.registros[-10:]:
            print("  >", r)
            time.sleep(0.5)
        print("------------------------")
        time.sleep(1)
    except LookupError as e:
        print(e)
        time.sleep(1)
    except Exception as e:
        print("Erro:", e)
        time.sleep(1)


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
        time.sleep(1)
    except LookupError as e:
        print(e)
        time.sleep(1)
    except ValueError as e:
        print("Valor inválido:", e)
        time.sleep(1)
    except Exception as e:
        print("Erro inesperado:", e)
        time.sleep(1)


def excluir_jogador():
    try:
        nome = input("Nome do jogador para excluir: ").strip()
        p = buscar_jogador_por_nome(nome)
        jogadores.remove(p)
        print(f"Jogador '{nome}' removido.")
        time.sleep(1)
    except LookupError as e:
        print(e)
        time.sleep(1)
    except Exception as e:
        print("Erro:", e)
        time.sleep(1)


def mostrar_loja():
    print("\n--- Loja ---")
    for item in LOJA:
        print(f"{item['id']}. {item['nome']} - Preço: {item['preco']}")
        time.sleep(0.5)
    print("------------")
    time.sleep(1)


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
        time.sleep(1)
    except LookupError as e:
        print(e)
        time.sleep(1)
    except ValueError:
        print("Entrada inválida. Use um número para ID.")
        time.sleep(1)
    except Exception as e:
        print("Erro:", e)
        time.sleep(1)


def batalhar():
    try:
        nome = input("Nome do jogador que vai batalhar: ").strip()
        p = buscar_jogador_por_nome(nome)
        npc = NPC("Goblin", random.randint(10, 40), random.choice(CLASSES), poder=random.randint(1, 8))
        print(f"{p.nome} (Level {p.level}) vs {npc.nome} (poder {npc.poder})")
        time.sleep(1)
        ataque_jogador = p.level + random.randint(0, 6)
        ataque_npc = npc.atacar_forca()
        print(f" - Força do jogador: {ataque_jogador}")
        time.sleep(0.5)
        print(f" - Força do inimigo: {ataque_npc}")
        time.sleep(0.5)
        if ataque_jogador >= ataque_npc:
            xp = random.randint(10, 40)
            p.ganhar_xp(xp)
            p.registros.append(f"Venceu batalha contra {npc.nome} (+{xp} XP).")
            print(f"Vitória! {p.nome} ganhou {xp} XP.")
        else:
            p.registros.append(f"Perdeu para {npc.nome}.")
            print("Derrota... tente de novo.")
        time.sleep(1)
    except LookupError as e:
        print(e)
        time.sleep(1)
    except Exception as e:
        print("Erro:", e)
        time.sleep(1)


def mostrar_menu():
    print("""
=== Jogo de Aventura ===
1 - Cadastrar jogador
2 - Listar jogadores
3 - Consultar jogador
4 - Editar jogador
5 - Excluir jogador
6 - Mostrar loja
7 - Comprar item
8 - Batalhar
9 - Sair
=============================
""")
    time.sleep(1)


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
                print("Saindo do jogo...")
                break
            else:
                print("Opção inválida.")
                time.sleep(1)
        except Exception as e:
            print("Erro inesperado no menu:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()

