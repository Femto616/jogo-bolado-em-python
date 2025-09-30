# RPG Python - Joguinho de Aventuras

## Descrição

Este é um RPG em Python modularizado, onde os jogadores podem criar personagens, comprar itens, batalhar contra inimigos e gerenciar seu progresso. O projeto é ideal para iniciantes em programação, utilizando listas, dicionários, classes e funções.

O jogo permite:

* Criação de personagens com classes: Guerreiro, Mago, Arqueiro
* Sistema de status de jogadores (Ativo/Inativo)
* Loja para compra de itens
* Batalhas por turnos contra inimigos
* Registro, edição e exclusão de jogadores

## Estrutura do Projeto

* **main.py**: Contém o menu e executa o jogo.
* **systems.py**: Contém todas as classes e funções do RPG.

## Tecnologias

* Python 3.x
* Estruturas: listas, dicionários, funções, loops
* Módulos: `random`, `time`, `typing`

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

2. Entre na pasta:

```bash
cd seu-repositorio
```

3. Execute o jogo:

```bash
python main.py
```

## Como Jogar

Ao executar `main.py`, escolha uma opção do menu:

```
1 - Cadastrar jogador
2 - Listar jogadores
3 - Consultar jogador
4 - Editar jogador
5 - Excluir jogador
6 - Mostrar loja
7 - Comprar item
8 - Batalhar
9 - Sair
```

Digite o número correspondente e siga as instruções.

## Funcionalidades

### Cadastrar jogador

Escolha nome, idade e classe. Exemplo:

```text
Digite o nome do jogador: Aragon
Escolha a classe:
1 - Guerreiro
2 - Mago
3 - Arqueiro
```

### Listar jogadores

Mostra todos os jogadores cadastrados com status e level.

### Consultar jogador

Exibe detalhes de um jogador, inventário e registros das últimas ações.

### Editar jogador

Permite alterar nome, idade ou classe de um jogador.

### Excluir jogador

Remove um jogador do sistema permanentemente.

### Loja e Comprar itens

Mostra itens disponíveis e permite compra usando moedas.

### Batalhar

Inicia uma batalha contra NPCs com turnos, mostrando vitória, derrota e XP ganho.

## Estrutura de Dados

* Lista de jogadores: `jogadores: List[Player]`
* Classes fixas: `CLASSES = ('Guerreiro', 'Mago', 'Arqueiro')`
* Status: `STATUS = ('Ativo', 'Inativo')`
* Itens: dicionários com `id`, `nome`, `preco`

## Contribuição

1. Fork do repositório
2. Criar branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit das alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abrir Pull Request

## Licença

Licença MIT.
