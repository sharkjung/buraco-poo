import pygame
import random
from typing import List, Optional, Tuple
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN, 
    BACKGROUND_COLOR, WHITE, BLACK, BLUE, GREEN, YELLOW
)
from jogador import Jogador
from monte import Monte
from carta import Carta
from agrupamento import Agrupamento

class Jogo:
    """Classe principal que controla o jogo"""
    def __init__(self):
        self.jogadores: List[Jogador] = [Jogador("Jogador 1"), Jogador("Jogador 2")]
        self.jogador_atual: int = 0
        self.monte = Monte()
        self.estado: str = "inicio"  # inicio, jogando, fim
        self.criar_baralho()
        self.distribuir_cartas()
        self.mensagem: str = ""
        self.botao_formar_agrupamento_rect: Optional[pygame.Rect] = None
        self.botao_descartar_rect: Optional[pygame.Rect] = None
        self.botao_adicionar_agrupamento_rect: Optional[pygame.Rect] = None
    
    def criar_baralho(self) -> None:
        """Cria e embaralha o baralho"""
        baralho = []
        
        # Cartas normais
        for naipe in Carta.NAIPES:
            for valor in Carta.VALORES:
                baralho.append(Carta(naipe, valor))
        
        # Curingas
        baralho.append(Carta('', 'Curinga', True))
        baralho.append(Carta('', 'Curinga', True))
        
        random.shuffle(baralho)
        self.monte.cartas = baralho
    
    def distribuir_cartas(self) -> None:
        """Distribui as cartas iniciais para os jogadores"""
        for _ in range(11):
            for jogador in self.jogadores:
                carta = self.monte.comprar_carta()
                if carta:
                    jogador.receber_carta(carta)
        
        # Coloca a primeira carta no descarte
        carta_inicial = self.monte.comprar_carta()
        if carta_inicial:
            self.monte.adicionar_descarte(carta_inicial)
    
    def proximo_jogador(self) -> None:
        """Passa a vez para o próximo jogador"""
        jogador = self.jogador_atual_obj()
        jogador.comprou_carta = False  # Reseta o flag de compra
        jogador.selecionadas.clear()  # Limpa cartas selecionadas
        # Desseleciona agrupamentos
        for g in jogador.agrupamentos:
            g.selecionado = False
        jogador.agrupamento_selecionado = None
        
        self.jogador_atual = (self.jogador_atual + 1) % len(self.jogadores)
        self.mensagem = f"Vez de {self.jogador_atual_nome()}"
    
    def jogador_atual_nome(self) -> str:
        """Retorna o nome do jogador atual"""
        return self.jogadores[self.jogador_atual].nome
    
    def jogador_atual_obj(self) -> Jogador:
        """Retorna o objeto do jogador atual"""
        return self.jogadores[self.jogador_atual]
    
    def verificar_fim_jogo(self) -> bool:
        """Verifica se o jogo terminou"""
        jogador = self.jogador_atual_obj()
        return len(jogador.mao) == 0 and jogador.tem_canastra()
    
    def comprar_do_monte(self) -> None:
        """Ação de comprar do monte"""
        jogador = self.jogador_atual_obj()
        carta = self.monte.comprar_carta()
        if carta:
            jogador.receber_carta(carta)
            self.mensagem = f"{jogador.nome} comprou do monte"
        else:
            self.mensagem = "Monte vazio!"
    
    def comprar_do_descarte(self) -> None:
        """Ação de comprar do descarte"""
        jogador = self.jogador_atual_obj()
        carta = self.monte.comprar_descarte()
        if carta:
            jogador.receber_carta(carta)
            self.mensagem = f"{jogador.nome} comprou do descarte"
        else:
            self.mensagem = "Descarte vazio!"
    
    def descartar_carta(self, carta: Carta) -> None:
        """Ação de descartar uma carta"""
        jogador = self.jogador_atual_obj()
        
        # Verifica se o jogador já comprou uma carta neste turno
        if not jogador.comprou_carta:
            self.mensagem = "Você deve comprar uma carta antes de descartar!"
            return
        
        carta_descartada = jogador.descartar(carta)
        if carta_descartada:
            self.monte.adicionar_descarte(carta_descartada)
            self.mensagem = f"{jogador.nome} descartou {carta_descartada}"
            self.proximo_jogador()
    
    def processar_clique(self, pos: Tuple[int, int]) -> None:
        """Processa um clique na tela"""
        if self.estado != "jogando":
            return
        
        jogador = self.jogador_atual_obj()
        
        # Verifica se clicou em uma carta da mão
        if jogador.selecionar_carta(pos):
            return
        
        # Verifica se clicou em um agrupamento
        if jogador.selecionar_agrupamento(pos):
            return
        
        # Verifica se clicou no monte de compra
        if self.monte.rect_compra.collidepoint(pos):
            self.comprar_do_monte()
            return
        
        # Verifica se clicou no descarte
        if self.monte.rect_descarte.collidepoint(pos) and self.monte.topo_descarte():
            self.comprar_do_descarte()
            return
        
        # Verifica se clicou no botão de formar agrupamento
        if self.botao_formar_agrupamento_rect and self.botao_formar_agrupamento_rect.collidepoint(pos):
            if jogador.tentar_formar_agrupamento():
                self.mensagem = f"{jogador.nome} formou um agrupamento!"
            else:
                self.mensagem = "Agrupamento inválido!"
            return
        
        # Verifica se clicou no botão de adicionar ao agrupamento
        if self.botao_adicionar_agrupamento_rect and self.botao_adicionar_agrupamento_rect.collidepoint(pos):
            if jogador.adicionar_carta_agrupamento():
                self.mensagem = f"{jogador.nome} adicionou cartas ao agrupamento!"
            else:
                self.mensagem = "Não foi possível adicionar cartas ao agrupamento!"
            return
        
        # Verifica se clicou no botão de descartar
        if self.botao_descartar_rect and self.botao_descartar_rect.collidepoint(pos) and jogador.selecionadas:
            carta = jogador.selecionadas[0]  # Descarta a primeira carta selecionada
            self.descartar_carta(carta)
            jogador.selecionadas.clear()
            return
    
    def desenhar(self) -> None:
        """Desenha toda a interface do jogo"""
        screen.fill(BACKGROUND_COLOR)
        
        if self.estado == "inicio":
            self.desenhar_tela_inicio()
        elif self.estado == "jogando":
            self.desenhar_tela_jogo()
        elif self.estado == "fim":
            self.desenhar_tela_fim()
        
        pygame.display.flip()
    
    def desenhar_tela_inicio(self) -> None:
        """Desenha a tela de início"""
        titulo = font.render("Buraco Simplificado", True, WHITE)
        subtitulo = font.render("Clique para começar", True, WHITE)
        
        screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(subtitulo, (SCREEN_WIDTH // 2 - subtitulo.get_width() // 2, SCREEN_HEIGHT // 2))
    
    def desenhar_tela_jogo(self) -> None:
        """Desenha a tela de jogo"""
        # Desenha o monte e descarte
        self.monte.desenhar()
        
        # Desenha a mão do jogador atual
        jogador = self.jogador_atual_obj()
        jogador.desenhar_mao(MARGIN, SCREEN_HEIGHT - CARD_HEIGHT - MARGIN)
        
        # Desenha os agrupamentos do jogador atual
        jogador.desenhar_agrupamentos(SCREEN_WIDTH // 2, MARGIN)
        
        # Desenha botões de ação
        self.desenhar_botoes_acao()
        
        # Desenha mensagem
        if self.mensagem:
            texto_msg = font.render(self.mensagem, True, WHITE)
            screen.blit(texto_msg, (MARGIN, MARGIN))
        
        # Desenha nome do jogador atual
        texto_jogador = font.render(f"Jogador atual: {jogador.nome}", True, WHITE)
        screen.blit(texto_jogador, (SCREEN_WIDTH - texto_jogador.get_width() - MARGIN, MARGIN))
    
    def desenhar_botoes_acao(self) -> None:
        """Desenha os botões de ação"""
        jogador = self.jogador_atual_obj()
        
        # Posiciona os botões acima da mão do jogador
        pos_y = SCREEN_HEIGHT - CARD_HEIGHT - MARGIN - 100
        
        # Botão para formar agrupamento
        self.botao_formar_agrupamento_rect = pygame.Rect(
            SCREEN_WIDTH - 220,
            pos_y,
            200,
            40
        )
        cor_botao = WHITE if len(jogador.selecionadas) >= 3 else (200, 200, 200)
        pygame.draw.rect(screen, cor_botao, self.botao_formar_agrupamento_rect)
        pygame.draw.rect(screen, BLACK, self.botao_formar_agrupamento_rect, 2)
        texto_agrupar = small_font.render("Formar Novo Agrupamento", True, BLACK)
        screen.blit(texto_agrupar, (
            self.botao_formar_agrupamento_rect.x + (200 - texto_agrupar.get_width()) // 2,
            self.botao_formar_agrupamento_rect.y + 10
        ))
        
        # Botão para adicionar a agrupamento existente
        self.botao_adicionar_agrupamento_rect = pygame.Rect(
            SCREEN_WIDTH - 220,
            pos_y + 50,
            200,
            40
        )
        cor_botao = GREEN if jogador.agrupamento_selecionado and jogador.selecionadas else (200, 200, 200)
        pygame.draw.rect(screen, cor_botao, self.botao_adicionar_agrupamento_rect)
        pygame.draw.rect(screen, BLACK, self.botao_adicionar_agrupamento_rect, 2)
        texto_adicionar = small_font.render("Adicionar ao Agrupamento", True, BLACK)
        screen.blit(texto_adicionar, (
            self.botao_adicionar_agrupamento_rect.x + (200 - texto_adicionar.get_width()) // 2,
            self.botao_adicionar_agrupamento_rect.y + 10
        ))
        
        # Botão para descartar
        self.botao_descartar_rect = pygame.Rect(
            SCREEN_WIDTH - 220,
            pos_y + 100,
            200,
            40
        )
        cor_botao = BLUE if jogador.selecionadas and jogador.comprou_carta else (200, 200, 200)
        pygame.draw.rect(screen, cor_botao, self.botao_descartar_rect)
        pygame.draw.rect(screen, BLACK, self.botao_descartar_rect, 2)
        texto_descartar = small_font.render("Descartar", True, BLACK)
        screen.blit(texto_descartar, (
            self.botao_descartar_rect.x + (200 - texto_descartar.get_width()) // 2,
            self.botao_descartar_rect.y + 10
        ))
    
    def desenhar_tela_fim(self) -> None:
        """Desenha a tela de fim de jogo"""
        titulo = font.render("Fim de Jogo!", True, WHITE)
        screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, MARGIN))
        
        # Calcula pontuações
        pontos_jogador1 = self.jogadores[0].get_pontos()
        pontos_jogador2 = self.jogadores[1].get_pontos()
        
        # Determina o vencedor
        if pontos_jogador1 > pontos_jogador2:
            vencedor = f"{self.jogadores[0].nome} venceu!"
        elif pontos_jogador2 > pontos_jogador1:
            vencedor = f"{self.jogadores[1].nome} venceu!"
        else:
            vencedor = "Empate!"
        
        texto_vencedor = font.render(vencedor, True, YELLOW)
        screen.blit(texto_vencedor, (SCREEN_WIDTH // 2 - texto_vencedor.get_width() // 2, MARGIN * 3))
        
        # Mostra pontuações
        texto_pontos1 = font.render(f"{self.jogadores[0].nome}: {pontos_jogador1} pontos", True, WHITE)
        texto_pontos2 = font.render(f"{self.jogadores[1].nome}: {pontos_jogador2} pontos", True, WHITE)
        
        screen.blit(texto_pontos1, (SCREEN_WIDTH // 2 - texto_pontos1.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(texto_pontos2, (SCREEN_WIDTH // 2 - texto_pontos2.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        # Botão para jogar novamente
        botao_reiniciar_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - CARD_WIDTH,
            SCREEN_HEIGHT - 100,
            CARD_WIDTH * 2,
            50
        )
        pygame.draw.rect(screen, WHITE, botao_reiniciar_rect)
        pygame.draw.rect(screen, BLACK, botao_reiniciar_rect, 2)
        texto_reiniciar = font.render("Jogar Novamente", True, BLACK)
        screen.blit(texto_reiniciar, (
            SCREEN_WIDTH // 2 - texto_reiniciar.get_width() // 2,
            SCREEN_HEIGHT - 90
        ))
        
        return botao_reiniciar_rect
    
    def reiniciar(self) -> None:
        """Reinicia o jogo"""
        self.__init__()
        self.estado = "jogando"
        self.mensagem = f"Vez de {self.jogador_atual_nome()}"