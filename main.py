from systems import *
from systems import cadastrar_jogador, listar_jogadores, consultar_jogador, editar_jogador, excluir_jogador, mostrar_loja, comprar_item, batalhar

def mostrar_menu():
    print("""
=== Jogo: Aventura & Loja ===
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
