# systems.py
from typing import List, Dict
import random
import time #Import utilizado para ter um delay em cada etapa

# Tuplas para dados fixos
CLASSES = ('Guerreiro', 'Mago', 'Arqueiro')
STATUS = ('Ativo', 'Inativo')

# Lista global de jogadores
jogadores: List['Player'] = []

# Itens da loja
LOJA = [
    {'id': 1, 'nome': 'Poção de Vida', 'preco': 10},
    {'id': 2, 'nome': 'Espada Curta', 'preco': 25},
    {'id': 3, 'nome': 'Cajado Místico', 'preco': 30},
    {'id': 4, 'nome': 'Arco Rústico', 'preco': 20}
]

# ------- Classes -------

class Person: #classe base
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self._idade = idade

    @property #faz eu poder usar ele como um atributo simples
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        if not isinstance(valor, int) or valor < 0:#impede deixar numero quebrado ou negativo
            raise ValueError("Idade deve ser inteiro >= 0.")
        self._idade = valor

class Character(Person): #herda a classe person
    def __init__(self, nome: str, idade: int, classe: str):
        super().__init__(nome, idade) #para reusar a logica do person
        if classe not in CLASSES: #ele vê se a classe está no CLASSES e se n estiver dá erro
            raise ValueError(f"Classe inválida. Opções: {CLASSES}")
        self.classe = classe
        self.status = STATUS[0]


class Player(Character): # herda de Character e repesenta um personagem jogavel
    def __init__(self, nome: str, idade: int, classe: str): #reusa a logica do Character
        super().__init__(nome, idade, classe)
        self._level = 1                           # novos atributos para o jogador
        self.experiencia = 0
        self.inventario: List[Dict] = []
        self.registros: List[str] = []

    @property #similar a idade garante que o level seja sempre inteiro
    def level(self):
        return self._level

    @level.setter
    def level(self, novo):
        if not isinstance(novo, int) or novo < 1:
            raise ValueError("Level deve ser inteiro >= 1.")
        self._level = novo

    def ganhar_xp(self, xp: int): #usamos um loop para fazer a logica de upar de nivel assim a cada 100 de xp aument um level automaticamente chamando o setter de level
        self.experiencia += xp
        self.registros.append(f"Ganhou {xp} XP.")
        while self.experiencia >= 100:
            self.experiencia -= 100
            self.level += 1
            self.registros.append("Subiu de nível!") #registra a ação

    def comprar(self, item: Dict): #adiciona o item no inventario do jogador e registra a compra
        self.inventario.append(item)
        self.registros.append(f"Comprou {item['nome']} por {item['preco']} moedas.")

    def __str__(self): #define como objeto o player para exibir um resumo das estatisticas principais quando impresso
        return f"{self.nome} | Classe: {self.classe} | Level: {self.level} | XP: {self.experiencia} | Itens: {len(self.inventario)}"


class NPC(Character):#herda Character dnv para fazer os inimigos/NPC (personagem n jogavel)
    def __init__(self, nome: str, idade: int, classe: str, poder: int):#adiciona o atributo poder
        super().__init__(nome, idade, classe)
        self.poder = poder

    def atacar_forca(self): #calcula a força do NPC e adiciona um valor aleatorio ao seu poder
        return self.poder + random.randint(0, 5)


jogadores.extend([ #jogadores pre estabelecidos 
    Player("Albino", 20, "Mago"),
    Player("Pitbull", 18, "Guerreiro"),
    Player("Xanxerê", 20, "Arqueiro")
])


# ------- Funções -------
def escolher_classe(): #exibe as classes disponiveis no Classes e usa um loop while para foçar a usar um numero valido
    while True:
        print("=== Escolha sua Classe ===")
        for i, c in enumerate(CLASSES, start=1):
            print(f"[{i}] {c}")
        try:
            escolha = int(input("Digite o número da classe: "))
            if 1 <= escolha <= len(CLASSES):
                return CLASSES[escolha - 1]
            else:
                print(f"Escolha inválida! Digite um número entre 1 e {len(CLASSES)}.")
        except ValueError:
            print("Entrada inválida! Digite apenas números.")

def cadastrar_jogador(): #pede um nome e idade, dps chama escolher_classe para pegar a classe, cria um novo objeto player e coloca na lista jogadores
    try:
        nome = input("Nome do jogador: ").strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        idade = int(input("Idade: ").strip())
        classe = escolher_classe()  # chama a função com validação
        novo = Player(nome, idade, classe)
        jogadores.append(novo)
        print(f"Jogador '{nome}' cadastrado com sucesso!")
        time.sleep(1.2)
        listar_jogadores()
    except ValueError as e:
        print(f"Erro ao cadastrar: {e}")
        time.sleep(1.2)
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
        time.sleep(1.2)


def listar_jogadores(): #passa pela lista jogadores e imprime o resumo de cada um usando o __str__ da classe player
    if not jogadores:
        print("Nenhum jogador cadastrado.")
        time.sleep(1.2)
        return
    print("\n--- Lista de Jogadores ---")
    time.sleep(0.8)
    for idx, p in enumerate(jogadores, 1):
        if isinstance(p, Player):
            print(f"{idx}. {p}")
        else:
            print(f"{idx}. [ERRO] Objeto inválido na lista: {p}")
        time.sleep(0.7)
    print("--------------------------")
    time.sleep(1.2)
    input('Aperte ENTER para continuar:    ')


def buscar_jogador_por_nome(nome: str) -> Player: #procura um jogador na lista jogadores pelo nome ignorando maiuscula ou minuscula e dando erro se n encontrar
    for p in jogadores:
        if p.nome.lower() == nome.lower():
            return p
    raise LookupError("Jogador não encontrado.")


def consultar_jogador(): #pede um nome, busca o jogador e imprime seu perfil,inventario e registros de açoes
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


def editar_jogador(): #permite um jogador mudar o nome,idade e classe usando o setter com a validaçao do Person 
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


def excluir_jogador(): #remove o jogador 
    try:
        nome = input("Nome do jogador para excluir: ").strip()
        p = buscar_jogador_por_nome(nome)
        jogadores.remove(p)
        print(f"Jogador '{nome}' removido.")
        time.sleep(1.2)
    except LookupError as e:
        print(e)
        time.sleep(1.2)
    except Exception as e:
        print("Erro:", e)
        time.sleep(1.2)


def mostrar_loja(): #mostra a loja pegando o id,nome e preço na lista no começo do codigo
    print("\n--- Loja ---")
    time.sleep(0.8)
    for item in LOJA:
        print(f"{item['id']}. {item['nome']} - Preço: {item['preco']}")
        time.sleep(0.7)
    print("------------")
    time.sleep(1.2)


def comprar_item(): #permite que o jogador compre itens mas sem verificar o dinheiro no fim de simplificar as coisas
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
        time.sleep(1.2)
    except LookupError as e:
        print(e)
        time.sleep(1.2)
    except ValueError:
        print("Entrada inválida. Use um número para ID.")
        time.sleep(1.2)
    except Exception as e:
        print("Erro:", e)
        time.sleep(1.2)


def batalhar():
    try:
        nome = input("Nome do jogador que vai batalhar: ").strip() #busca o jogador
        p = buscar_jogador_por_nome(nome)
        npc = NPC("Goblin", random.randint(10, 40), random.choice(CLASSES), poder=random.randint(1, 8))
        print(f"{p.nome} (Level {p.level}) vs {npc.nome} (poder {npc.poder})")
        time.sleep(1.2)
        ataque_jogador = p.level + random.randint(0, 6)
        ataque_npc = npc.atacar_forca()
        print(f" - Força do jogador: {ataque_jogador}") #compara força do jogador com a do npc sendo a do jogador com base no level e do npc com valor aleatorio
        time.sleep(0.7)
        print(f" - Força do inimigo: {ataque_npc}")
        time.sleep(0.7)
        if ataque_jogador >= ataque_npc: #se o jogador ganhar chama o p.ganhar_xp() dando xp para o level up sendo de 10 a 40 de xp
            xp = random.randint(10, 40)
            p.ganhar_xp(xp)
            p.registros.append(f"Venceu batalha contra {npc.nome} (+{xp} XP).") #registra o resultado
            print(f"Vitória! {p.nome} ganhou {xp} XP.")
            time.sleep(1.2)
        else:
            p.registros.append(f"Perdeu para {npc.nome}.") #registra a derrota do jogador
            print("Derrota... tente de novo.")
            time.sleep(1.2)
    except LookupError as e:
        print(e)
        time.sleep(1.2)
    except Exception as e:
        print("Erro:", e)
        time.sleep(1.2)
