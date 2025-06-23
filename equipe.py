class Equipe:
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.sequencias = []
        self.pontuacao_total = 0
        self.pegou_morto = False
        self.bateu = False

    def add_meld(self, cartas):
        self.sequencias.append(cartas)
        if self.eh_canastra_limpa(cartas):
            self.pontuacao_total += 200
        elif self.eh_canastra_suja(cartas):
            self.pontuacao_total += 100

    def eh_canastra_limpa(self, cartas):
        if len(cartas) != 7 or any(carta.is_wildcard() for carta in cartas):
            return False
        suits = {carta.naipe for carta in cartas}
        return len(suits) == 1

    def eh_canastra_suja(self, cartas):
        return len(cartas) == 7 and any(carta.eh_coringa() for carta in cartas)

    def contar_pontos_na_mesa(self):
        total = 0
        for meld in self.sequencias:
            for carta in meld:
                total += carta.pontos()
        return total
