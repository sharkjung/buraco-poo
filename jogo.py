from baralho import Deck
from jogador import Jogador
from equipe import Equipe
from interface import Interface

class Jogo:
    def __init__(self, nomes_jogadores):
        self.baralho = Deck()
        self.jogadores = [Jogador(nome, i // 2) for i, nome in enumerate(nomes_jogadores)]
        self.equipes = [Equipe(self.jogadores[:2]), Equipe(self.jogadores[2:])]
        self.vez_do_jogador = 0
        self.baralho.distribuir_cartas(self.jogadores)
        self.acabou = False

    def jogar_mao(self):
        jogador = self.jogadores[self.vez_do_jogador]
        print(f"\n>> Vez de {jogador.nome}")

        Interface.exibir_mao(jogador)
        jogador.comprar(self.baralho)

        carta_descartada = Interface.escolher_carta_para_discarte(jogador)
        jogador.discarte(carta_descartada, self.baralho)

        if not jogador.mao:
            equipe = self.equipes[jogador.id_equipe]
            if not equipe.pegou_morto:
                print(f"{jogador.nome} pegou o morto!")
                jogador.mao.extend(self.baralho.mortos[jogador.id_equipe])
                equipe.pegou_morto = True
            elif equipe.bateu:
                print(f"{jogador.nome} já bateu e acabou de novo!")
                self.finalizar_jogo()
                return
            else:
                equipe.pontuacao_total += 100
                equipe.bateu = True
                print(f"{jogador.nome} bateu!")
                self.finalizar_jogo()
                return

        Interface.exibir_estado_do_jogo(self)
        Interface.pausar()
        self.vez_do_jogador = (self.vez_do_jogador + 1) % 4

    def finalizar_jogo(self):
        print("\nFIM DA RODADA")
        for equipe in self.equipes:
            equipe.pontuacao_total += equipe.contar_pontos_na_mesa()
            if not equipe.bateu and not any(len(m) >= 7 for m in equipe.sequencias):
                equipe.pontuacao_total -= 200
            if not equipe.pegou_morto:
                equipe.pontuacao_total -= 100

        for i, equipe in enumerate(self.equipes):
            print(f"Equipe {i+1}: {equipe.pontuacao_total} pontos")
        self.acabou = True

    def fim_de_jogo(self):
        return any(equipe.pontuacao_total >= 3000 for equipe in self.equipes)
