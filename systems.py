from typing import Dict
import random
from models import Player, NPC
from models import jogadores, LOJA, CLASSES

# -------- Funções --------

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
    try:
        nome = input("Nome do jogador que vai batalhar: ").strip()
        p = buscar_jogador_por_nome(nome)
        npc = NPC("Goblin", random.randint(10, 40), random.choice(CLASSES), poder=random.randint(1, 8))
        print(f"{p.nome} (Level {p.level}) vs {npc.nome} (poder {npc.poder})")
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
