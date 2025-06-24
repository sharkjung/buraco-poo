import pygame
from typing import Tuple
from constants import CARD_WIDTH, CARD_HEIGHT, WHITE, BLACK, RED, YELLOW

class Carta:
    """Classe que representa uma carta do jogo"""
    NAIPES = ['♠', '♥', '♦', '♣']
    VALORES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    ESPECIAIS = {'Curinga': 'C'}

    def __init__(self, naipe: str, valor: str, curinga: bool = False):
        self.naipe = naipe
        self.valor = valor
        self.curinga = curinga  # '2' não é automaticamente curinga
        self.virada = False
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        
    def __str__(self) -> str:
        if self.curinga and self.valor == 'Curinga':
            return self.ESPECIAIS['Curinga']
        return f"{self.valor}{self.naipe}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_pontos(self) -> int:
        """Retorna os pontos da carta"""
        if self.curinga and self.valor == 'Curinga':
            return 20
        if self.valor == 'A':
            return 15
        if self.valor in ['2', '8', '9', '10', 'J', 'Q', 'K']:
            return 10
        return 5
    
    def get_cor(self) -> Tuple[int, int, int]:
        """Retorna a cor da carta com base no naipe"""
        if self.curinga and self.valor == 'Curinga':
            return YELLOW
        if self.naipe in ['♥', '♦']:
            return RED
        return BLACK
    
    def desenhar(self, x: int, y: int, selecionada: bool = False) -> None:
        """Desenha a carta na tela"""
        self.rect.x = x
        self.rect.y = y
        
        # Desenha o retângulo da carta
        cor_borda = BLUE if selecionada else BLACK
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, cor_borda, self.rect, 2)
        
        if self.virada:
            pygame.draw.rect(screen, BLUE, self.rect)
            return
        
        # Desenha o valor e naipe da carta
        texto = font.render(str(self), True, self.get_cor())
        texto_rect = texto.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
        screen.blit(texto, texto_rect)
    
    def pode_sequenciar(self, outra: 'Carta') -> bool:
        """Verifica se esta carta pode sequenciar com outra"""
        if self.curinga or outra.curinga or self.valor == '2' or outra.valor == '2':
            return True
        
        if self.naipe != outra.naipe:
            return False
        
        idx_atual = self.VALORES.index(self.valor)
        idx_outra = self.VALORES.index(outra.valor)
        
        return abs(idx_atual - idx_outra) == 1
    
    def eh_consecutiva(self, outra: 'Carta') -> bool:
        """Verifica se esta carta é consecutiva à outra"""
        if self.curinga or outra.curinga or self.valor == '2' or outra.valor == '2':
            return True
        
        if self.naipe != outra.naipe:
            return False
        
        idx_atual = self.VALORES.index(self.valor)
        idx_outra = self.VALORES.index(outra.valor)
        
        return idx_atual == idx_outra + 1 or idx_atual == idx_outra - 1
    
    def pode_adicionar_trinca(self, agrupamento: 'Agrupamento') -> bool:
        """Verifica se a carta pode ser adicionada a uma trinca"""
        if not agrupamento.eh_trinca():
            return False
        
        # Curingas verdadeiros não podem ser adicionados a trincas
        if self.curinga and self.valor == 'Curinga':
            return False
        
        # Se é um '2', pode ser adicionado como carta normal
        if self.valor == '2':
            # Verifica se o agrupamento já tem um '2'
            return '2' in [c.valor for c in agrupamento.cartas]
        
        # Se o agrupamento tem curingas, verifica se o valor bate com as cartas não curingas
        valores_nao_curingas = [c.valor for c in agrupamento.cartas if not c.curinga and c.valor != '2']
        if not valores_nao_curingas:  # Todas são curingas ou '2's
            return True
            
        return self.valor == valores_nao_curingas[0]
    
    def pode_adicionar_sequencia(self, agrupamento: 'Agrupamento') -> bool:
        """Verifica se a carta pode ser adicionada a uma sequência"""
        if not agrupamento.eh_sequencia():
            return False
        
        # Se é curinga ou '2', pode ser adicionada a qualquer sequência
        if self.curinga or self.valor == '2':
            return True
        
        # Pega as cartas não curingas do agrupamento (excluindo '2's)
        cartas_nao_curingas = [c for c in agrupamento.cartas if not c.curinga and c.valor != '2']
        
        # Verifica naipe
        if cartas_nao_curingas and self.naipe != cartas_nao_curingas[0].naipe:
            return False
        
        # Verifica se pode ser adicionada no início ou no fim
        valores = [Carta.VALORES.index(c.valor) for c in cartas_nao_curingas]
        if not valores:
            return True
        
        min_valor = min(valores)
        max_valor = max(valores)
        meu_valor = Carta.VALORES.index(self.valor)
        
        return meu_valor == min_valor - 1 or meu_valor == max_valor + 1