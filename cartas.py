class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def eh_coringa(self):
        return self.valor == '2'

    def pontos(self):
        if self.valor in ['3', '4', '5', '6', '7']:
            return 5
        elif self.valor in ['8', '9', '10', 'J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 15
        elif self.valor == '2':
            return 10
        return 0

    def __repr__(self):
        return f"{self.valor}{self.naipe}"
