import pygame
from typing import Optional
from constants import CARD_WIDTH, CARD_HEIGHT, MARGIN, SCREEN_HEIGHT, WHITE, BLACK
from carta import Carta

class Monte:
    """Classe que representa o monte de compra e a pilha de descarte"""
    def __init__(self):
        self.cartas: List[Carta] = []
        self.descarte: List[Carta] = []
        self.rect_compra = pygame.Rect(MARGIN, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
        self.rect_descarte = pygame.Rect(MARGIN + CARD_WIDTH + MARGIN, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
    
    def comprar_carta(self) -> Optional[Carta]:
        """Compra uma carta do monte"""
        if self.cartas:
            return self.cartas.pop()
        return None
    
    def comprar_descarte(self) -> Optional[Carta]:
        """Compra a carta do topo do descarte"""
        if self.descarte:
            return self.descarte.pop()
        return None
    
    def adicionar_descarte(self, carta: Carta) -> None:
        """Adiciona uma carta ao descarte"""
        self.descarte.append(carta)
    
    def topo_descarte(self) -> Optional[Carta]:
        """Retorna a carta do topo do descarte sem removê-la"""
        if self.descarte:
            return self.descarte[-1]
        return None
    
    def desenhar(self) -> None:
        """Desenha o monte e o descarte na tela"""
        # Desenha o monte de compra
        pygame.draw.rect(screen, WHITE, self.rect_compra)
        pygame.draw.rect(screen, BLACK, self.rect_compra, 2)
        texto = font.render("Compra", True, BLACK)
        screen.blit(texto, (self.rect_compra.x + 10, self.rect_compra.y + CARD_HEIGHT // 2 - 10))
        
        # Desenha a pilha de descarte
        if self.descarte:
            self.topo_descarte().desenhar(self.rect_descarte.x, self.rect_descarte.y)
        else:
            pygame.draw.rect(screen, WHITE, self.rect_descarte)
            pygame.draw.rect(screen, BLACK, self.rect_descarte, 2)
            texto = font.render("Descarte", True, BLACK)
            screen.blit(texto, (self.rect_descarte.x + 10, self.rect_descarte.y + CARD_HEIGHT // 2 - 10))
