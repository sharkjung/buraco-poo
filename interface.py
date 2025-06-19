from cartas import Carta

class Interface:
    @staticmethod
    def exibir_mao(jogador):
        print(f"Mao de {jogador.nome} " + ", ".join(str(carta) for carta in jogador.mao))

    @staticmethod
    def escolher_carta_para_discarte(jogador):
        Interface.exibir_mao(jogador)
        while True:
            try:
                escolha = int(input(f"Escolha o índice da carta para descartar (0 a {len(jogador.mao) - 1}): "))
                if 0 <= escolha < len(jogador.mao):
                    return jogador.mao[escolha]
            except ValueError:
                pass
            print("Entrada inválida. Tente novamente.")

    @staticmethod
    def exibir_estado_do_jogo(jogo):
        print("=== ESTADO DO JOGO ===")
        for i, equipe in enumerate(jogo.equipes):
            print(f"Equipe {i+1} - Pontos: {equipe.pontuacao_total} - Canastras: {len(equipe.sequencias)}")
        print(f"Cartas restantes no monte: {len(jogo.baralho.cartas)}")
        if jogo.baralho.lixo:
            print(f"Carta no topo do descarte: {jogo.baralho.lixo[-1]}")
        else:
            print("Pilha de descarte vazia.")

    @staticmethod
    def pausar():
        input("Pressione Enter para continuar...")
