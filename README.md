# Buraco Simplificado - Jogo de Cartas em Python com Pygame

Este projeto implementa uma versão simplificada do jogo de cartas Buraco (estilo Canastra) usando Python e Pygame. O jogo segue as regras básicas do Buraco com algumas simplificações para tornar a implementação mais direta, mantendo a essência do jogo original.

## Funcionalidades Principais

-   **Dois jogadores** alternando turnos
    
-   **Sistema completo de cartas** com valores, naipes e curingas
    
-   **Formação de agrupamentos**:
    
    -   Trincas (3+ cartas do mesmo valor)
        
    -   Sequências (3+ cartas consecutivas do mesmo naipe)
        
    -   Canastras (agrupamentos com 7+ cartas)
        
-   **Sistema de pontuação** baseado nas regras do Buraco
    
-   **Interface gráfica intuitiva** com Pygame
    
-   **Regras implementadas**:
    
    -   Compra obrigatória antes do descarte
        
    -   Tratamento especial para cartas "2" (podem ser usadas como normais ou curingas)
        
    -   Validação de jogadas

## Como Jogar

1.  **Início do jogo**:
    
    -   Cada jogador recebe 11 cartas
        
    -   Uma carta é virada para iniciar o descarte
        
2.  **Durante o jogo**:
    
    -   **Compre uma carta**: clique no monte de compra ou na pilha de descarte
        
    -   **Forme agrupamentos**:
        
        -   Selecione 3+ cartas válidas e clique em "Formar Novo Agrupamento"
            
        -   Para adicionar a um agrupamento existente, selecione-o e depois selecione as cartas para adicionar
            
    -   **Descartar**: selecione uma carta e clique em "Descartar" (após ter comprado)
        
3.  **Fim do jogo**:
    
    -   O jogo termina quando um jogador fica sem cartas na mão e tem pelo menos uma canastra
        
    -   A pontuação é calculada baseada nos agrupamentos formados e cartas restantes
        

## Estrutura do Código

O projeto está organizado em classes principais:

-   `Carta`: Representa uma carta individual com valor, naipe e propriedades
    
-   `Agrupamento`: Gerencia conjuntos de cartas (trincas, sequências)
    
-   `Jogador`: Controla a mão do jogador e seus agrupamentos
    
-   `Monte`: Gerencia o monte de compra e a pilha de descarte
    
-   `Jogo`: Classe principal que orquestra a lógica do jogo
    

## Regras Implementadas

1.  **Cartas**:
    
    -   Valores: A, 2-10, J, Q, K
        
    -   Naipes: ♠, ♥, ♦, ♣
        
    -   Curingas: 🃏 (verdadeiro) e '2' (funciona como curinga em sequências)
        
2.  **Agrupamentos válidos**:
    
    -   **Trinca**: 3+ cartas do mesmo valor (incluindo trincas de '2's)
        
    -   **Sequência**: 3+ cartas consecutivas do mesmo naipe (com possibilidade de usar curingas)
        
    -   **Canastra**: Agrupamento com 7+ cartas (bonus de pontos)
        
3.  **Pontuação**:
    
    -   Curinga: 20 pontos
        
    -   Ás: 15 pontos
        
    -   2, 8, 9, 10, J, Q, K: 10 pontos
        
    -   3-7: 5 pontos
        
    -   Bônus de canastra: 100 (com curinga) ou 200 (sem curinga) pontos
      


## Diagrama UML
```mermaid
classDiagram

class Carta {

+NAIPES: List<String>

+VALORES: List<String>

+ESPECIAIS: Dict<String, String>

+naipe: String

+va1lor: String

+curinga: Boolean

+virada: Boolean

+rect: pygame.Rect

+__str__(): String

+get_pontos(): int

+get_cor(): Tuple<int,int,int>

+desenhar(x: int, y: int, selecionada: Boolean): void

+pode_sequenciar(outra: Carta): Boolean

+eh_consecutiva(outra: Carta): Boolean

+pode_adicionar_trinca(agrupamento: Agrupamento): Boolean

+pode_adicionar_sequencia(agrupamento: Agrupamento): Boolean

}

  

class Agrupamento {

+cartas: List<Carta>

+rect: pygame.Rect

+posicao: Tuple<int,int>

+selecionado: Boolean

+adicionar_carta(carta: Carta): Boolean

+ordenar_sequencia(): void

+validar(): Boolean

+eh_trinca(): Boolean

+eh_sequencia(): Boolean

+eh_canastra(): Boolean

+get_pontos(): int

+desenhar(x: int, y: int): void

+selecionar(pos: Tuple<int,int>): Boolean

}

  

class Jogador {

+nome: String

+mao: List<Carta>

+agrupamentos: List<Agrupamento>

+pontos: int

+selecionadas: List<Carta>

+agrupamento_selecionado: Agrupamento

+comprou_carta: Boolean

+receber_carta(carta: Carta): void

+descartar(carta: Carta): Carta

+formar_agrupamento(cartas: List<Carta>): Boolean

+get_pontos(): int

+tem_canastra(): Boolean

+desenhar_mao(x: int, y: int): void

+desenhar_agrupamentos(x: int, y: int): void

+selecionar_carta(pos: Tuple<int,int>): Boolean

+selecionar_agrupamento(pos: Tuple<int,int>): Boolean

+adicionar_carta_agrupamento(): Boolean

+tentar_formar_agrupamento(): Boolean

}

  

class Monte {

+cartas: List<Carta>

+descarte: List<Carta>

+rect_compra: pygame.Rect

+rect_descarte: pygame.Rect

+comprar_carta(): Carta

+comprar_descarte(): Carta

+adicionar_descarte(carta: Carta): void

+topo_descarte(): Carta

+desenhar(): void

}

  

class Jogo {

+jogadores: List<Jogador>

+jogador_atual: int

+monte: Monte

+estado: String

+mensagem: String

+botao_formar_agrupamento_rect: pygame.Rect

+botao_descartar_rect: pygame.Rect

+botao_adicionar_agrupamento_rect: pygame.Rect

+criar_baralho(): void

+distribuir_cartas(): void

+proximo_jogador(): void

+jogador_atual_nome(): String

+jogador_atual_obj(): Jogador

+verificar_fim_jogo(): Boolean

+comprar_do_monte(): void

+comprar_do_descarte(): void

+descartar_carta(carta: Carta): void

+processar_clique(pos: Tuple<int,int>): void

+desenhar(): void

+desenhar_tela_inicio(): void

+desenhar_tela_jogo(): void

+desenhar_tela_fim(): void

+desenhar_botoes_acao(): void

+reiniciar(): void

}

  

Jogo "1" *-- "2" Jogador

Jogo "1" *-- "1" Monte

Monte "1" *-- "0.." Carta

Jogador "1" *-- "0..*" Carta

Jogador "1" *-- "0..*" Agrupamento

Agrupamento "1" *-- "3..*" Carta
```