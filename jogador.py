from typing import List, Optional, Tuple
from constants import CARD_WIDTH, SCREEN_WIDTH, MARGIN
from carta import Carta
from agrupamento import Agrupamento

class Jogador:
    """Classe que representa um jogador"""
    def __init__(self, nome: str):
        self.nome = nome
        self.mao: List[Carta] = []
        self.agrupamentos: List[Agrupamento] = []
        self.pontos: int = 0
        self.selecionadas: List[Carta] = []
        self.agrupamento_selecionado: Optional[Agrupamento] = None
        self.comprou_carta: bool = False  # Controla se já comprou uma carta no turno
    
    def receber_carta(self, carta: Carta) -> None:
        """Adiciona uma carta à mão do jogador"""
        self.mao.append(carta)
        self.comprou_carta = True
    
    def descartar(self, carta: Carta) -> Carta:
        """Descarta uma carta da mão do jogador"""
        if carta in self.mao:
            self.mao.remove(carta)
            return carta
        return None
    
    def formar_agrupamento(self, cartas: List[Carta]) -> bool:
        """Tenta formar um agrupamento com as cartas selecionadas"""
        agrupamento = Agrupamento(cartas)
        if agrupamento.validar():
            self.agrupamentos.append(agrupamento)
            for carta in cartas:
                if carta in self.mao:
                    self.mao.remove(carta)
            return True
        return False
    
    def get_pontos(self) -> int:
        """Calcula a pontuação do jogador"""
        pontos_agrupamentos = sum(g.get_pontos() for g in self.agrupamentos)
        pontos_mao = sum(c.get_pontos() for c in self.mao)
        return pontos_agrupamentos - pontos_mao
    
    def tem_canastra(self) -> bool:
        """Verifica se o jogador tem pelo menos uma canastra"""
        return any(g.eh_canastra() for g in self.agrupamentos)
    
    def desenhar_mao(self, x: int, y: int) -> None:
        """Desenha a mão do jogador na tela"""
        # Calcula a sobreposição necessária para caber todas as cartas na tela
        num_cartas = len(self.mao)
        if num_cartas == 0:
            return
            
        # Calcula a sobreposição entre cartas para caber na tela
        sobreposicao = max(20, (num_cartas * (CARD_WIDTH - 20) - (SCREEN_WIDTH - x - MARGIN)) // num_cartas + 20)
        sobreposicao = min(sobreposicao, CARD_WIDTH - 10)  # Limita a sobreposição
        
        for i, carta in enumerate(self.mao):
            selecionada = carta in self.selecionadas
            carta.desenhar(x + i * (CARD_WIDTH - sobreposicao), y, selecionada)
    
    def desenhar_agrupamentos(self, x: int, y: int) -> None:
        """Desenha os agrupamentos do jogador na tela"""
        for i, agrupamento in enumerate(self.agrupamentos):
            agrupamento.desenhar(x, y + i * (CARD_HEIGHT + MARGIN))
    
    def selecionar_carta(self, pos: Tuple[int, int]) -> bool:
        """Seleciona/desseleciona uma carta com base na posição do clique"""
        for carta in reversed(self.mao):  # Verifica de trás para frente para pegar a carta no topo
            if carta.rect.collidepoint(pos):
                if carta in self.selecionadas:
                    self.selecionadas.remove(carta)
                else:
                    self.selecionadas.append(carta)
                return True
        return False
    
    def selecionar_agrupamento(self, pos: Tuple[int, int]) -> bool:
        """Seleciona um agrupamento com base na posição do clique"""
        for agrupamento in self.agrupamentos:
            if agrupamento.selecionar(pos):
                # Desseleciona todos os outros agrupamentos
                for g in self.agrupamentos:
                    g.selecionado = False
                
                agrupamento.selecionado = True
                self.agrupamento_selecionado = agrupamento
                return True
        
        # Se clicou fora de qualquer agrupamento, desseleciona todos
        for g in self.agrupamentos:
            g.selecionado = False
        self.agrupamento_selecionado = None
        return False
    
    def adicionar_carta_agrupamento(self) -> bool:
        """Tenta adicionar cartas selecionadas ao agrupamento selecionado"""
        if not self.agrupamento_selecionado or not self.selecionadas:
            return False
        
        # Faz uma cópia para testar antes de modificar
        agrupamento_temporario = Agrupamento(self.agrupamento_selecionado.cartas.copy())
        
        for carta in self.selecionadas:
            if not agrupamento_temporario.adicionar_carta(carta):
                return False
        
        # Se todas as cartas podem ser adicionadas, aplica as mudanças
        for carta in self.selecionadas:
            self.agrupamento_selecionado.adicionar_carta(carta)
            if carta in self.mao:
                self.mao.remove(carta)
        
        self.selecionadas.clear()
        return True
    
    def tentar_formar_agrupamento(self) -> bool:
        """Tenta formar um agrupamento com as cartas selecionadas"""
        if len(self.selecionadas) < 3:
            return False
        
        sucesso = self.formar_agrupamento(self.selecionadas.copy())
        if sucesso:
            self.selecionadas.clear()
        return sucesso