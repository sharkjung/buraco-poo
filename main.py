from jogo import Jogo

if __name__ == '__main__':
    nomes = ["Conrado", "Luky", "Daniel", "Yasmin"]
    jogo = Jogo(nomes)

    while not jogo.acabou and not jogo.fim_de_jogo():
        jogo.jogar_mao()
        input("Aperte Enter para o próximo turno")

    print("Fim do jogo!")