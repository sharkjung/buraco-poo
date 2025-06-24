import pygame
import sys
from jogo import Jogo

# Inicialização do Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Buraco")
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

def main():
    """Função principal do jogo"""
    clock = pygame.time.Clock()
    jogo = Jogo()
    botao_reiniciar = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if jogo.estado == "inicio":
                    jogo.estado = "jogando"
                    jogo.mensagem = f"Vez de {jogo.jogador_atual_nome()}"
                
                elif jogo.estado == "jogando":
                    jogo.processar_clique(pos)
                    
                    # Verifica se o jogo terminou
                    if jogo.verificar_fim_jogo():
                        jogo.estado = "fim"
                
                elif jogo.estado == "fim":
                    if botao_reiniciar and botao_reiniciar.collidepoint(pos):
                        jogo.reiniciar()
        
        jogo.desenhar()
        
        if jogo.estado == "fim":
            botao_reiniciar = jogo.desenhar_tela_fim()
        
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()