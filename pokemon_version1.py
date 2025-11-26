import pygame
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ⚙️ Configurações da Tela - DIMENSÕES TOTAIS DO FIGMA
SCREEN_WIDTH = 450  
SCREEN_HEIGHT = 600 
SCREEN_TITLE = "Torne-se um treinador Pokémon!"

# 🎨 Cores 
BUTTON_BLUE = (0, 200, 200)       
BUTTON_HOVER_BLUE = (0, 180, 180) 
TEXT_COLOR = (255, 255, 255)      
BLACK = (0, 0, 0)                 
BLUE_BACKGROUND = (100, 200, 230) 

# 🚀 Inicialização do Pygame
pygame.init()

# Criação da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# 🔡 Configuração da Fonte (Ajustada para caber no novo layout)
try:
    font_path_modern = pygame.font.match_font('arial, helvetica, sans-serif')
    if font_path_modern:
        font = pygame.font.Font(font_path_modern, 28) 
        small_font = pygame.font.Font(font_path_modern, 18)
        smaller_font = pygame.font.Font(font_path_modern, 14)
    else:
        font = pygame.font.Font(None, 32) 
        small_font = pygame.font.Font(None, 20)
        smaller_font = pygame.font.Font(None, 16)
except:
    font = pygame.font.Font(None, 32) 
    small_font = pygame.font.Font(None, 20)
    smaller_font = pygame.font.Font(None, 16)

# =========================================================================
# 🖼️ CARREGAMENTO DE IMAGENS E COORDENADAS (AJUSTADAS)
# =========================================================================
# ⚠️ COORDENADAS DA ÁREA PRETA (TELA DO JOGO)
GAME_SCREEN_WIDTH = 377
GAME_SCREEN_HEIGHT = 372
# X centralizado na tela: (450 - 377) / 2 = 36.5 -> Arredondei para 36
GAME_SCREEN_X = 36  
# Y estimado: 20px do topo
GAME_SCREEN_Y = 20
GAME_SCREEN_RECT = pygame.Rect(GAME_SCREEN_X, GAME_SCREEN_Y, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)

BACKGROUND_IMAGE = None
try:
    # AGORA, usa o caminho absoluto do SCRIPT_DIR
    background_path = os.path.join(SCRIPT_DIR, "background.png")
    BACKGROUND_IMAGE = pygame.image.load(background_path).convert_alpha()
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    pass

POKEMON_SPRITES = {}
SPRITE_SIZE = 100 # Sprites menores para caber na tela de 372px de altura

def load_pokemon_sprites():
    global POKEMON_SPRITES
    sprite_names = {"Bulbasaur": "bulbasaur.png", "Charmander": "charmander.png", "Squirtle": "squirtle.png"}
    for name, file_name in sprite_names.items():
        try:
            # AGORA, usa o caminho absoluto do SCRIPT_DIR
            sprite_path = os.path.join(SCRIPT_DIR, file_name)
            image = pygame.image.load(sprite_path).convert_alpha()
            image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
            POKEMON_SPRITES[name] = image
        except pygame.error:
            # ... (o resto do bloco de erro continua igual)
            substitute = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
            substitute.fill((100, 100, 100, 128)) 
            POKEMON_SPRITES[name] = substitute
            
load_pokemon_sprites() 
# =========================================================================

# 📋 Estrutura de Dados do Quiz (Mantida)
quiz_data = [
    {
        "pergunta": "1. Como você se sente em situações desafiadoras?",
        "opcoes": {"A": "Emotivo", "B": "Tranquilo", "C": "Nervoso"},
        "pontuacao": {"A": "Squirtle", "B": "Charmander", "C": "Bulbasaur"}
    },
    {
        "pergunta": "2. Qual desses 3 itens lhe parece mais interessante?",
        "opcoes": {"A": "Óculos estiloso", "B": "Jaqueta quentinha", "C": "Boina fashion"},
        "pontuacao": {"A": "Squirtle", "B": "Charmander", "C": "Bulbasaur"}
    },
    {
        "pergunta": "3. Qual dos seguintes elementos você prefere?",
        "opcoes": {"A": "Água", "B": "Fogo", "C": "Terra"},
        "pontuacao": {"A": "Squirtle", "B": "Charmander", "C": "Bulbasaur"}
    },
    {
        "pergunta": "4. Qual das seguintes paisagens te deixa mais feliz?",
        "opcoes": {"A": "Praia no Caribe", "B": "Vulcões no Havaí", "C": "Floresta Amazônica"},
        "pontuacao": {"A": "Squirtle", "B": "Charmander", "C": "Bulbasaur"}
    },
    {
        "pergunta": "5. Qual sua cor preferida?",
        "opcoes": {"A": "Azul", "B": "Vermelho", "C": "Verde"},
        "pontuacao": {"A": "Squirtle", "B": "Charmander", "C": "Bulbasaur"}
    }
]

# Variáveis globais de pontuação
squirtle = 0
charmander = 0
bulbasaur = 0


# 🕹️ Função de Desenho do Botão 
def draw_button(surface, rect, text, font, color, hover_color, mouse_pos, border_radius=10):
    action = False
    current_color = hover_color if rect.collidepoint(mouse_pos) else color
    
    pygame.draw.rect(surface, current_color, rect, border_radius=border_radius)
    pygame.draw.rect(surface, (0, 0, 0, 100), rect, 3, border_radius=border_radius) 

    text_surf = font.render(text, True, TEXT_COLOR) 
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    
    if pygame.mouse.get_pressed()[0] == 1 and rect.collidepoint(mouse_pos):
        action = True
    return action

# ❓ Função para a Tela do Quiz
def quiz_screen():
    global squirtle, charmander, bulbasaur
    
    squirtle = 0
    charmander = 0
    bulbasaur = 0
    
    current_question_index = 0
    quiz_running = True
    
    option_rects = {}
    option_letters = ["A", "B", "C"]
    
    # Posições ajustadas para a tela de 372px de altura
    start_y = GAME_SCREEN_RECT.y + 100 
    button_spacing = 65
    button_width = GAME_SCREEN_WIDTH - 40 
    button_height = 45

    for i, letter in enumerate(option_letters):
        x = GAME_SCREEN_RECT.x + (GAME_SCREEN_WIDTH // 2) - (button_width // 2)
        y = start_y + (i * button_spacing)
        option_rects[letter] = pygame.Rect(x, y, button_width, button_height)
        
    while quiz_running:
        mouse_pos = pygame.mouse.get_pos()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for letter, rect in option_rects.items():
                    if rect.collidepoint(event.pos):
                        
                        question = quiz_data[current_question_index]
                        pokemon_chosen = question["pontuacao"][letter]
                        
                        if pokemon_chosen == "Squirtle":
                            squirtle += 1
                        elif pokemon_chosen == "Charmander":
                            charmander += 1
                        elif pokemon_chosen == "Bulbasaur":
                            bulbasaur += 1
                        
                        current_question_index += 1
                        if current_question_index >= len(quiz_data):
                            result_screen()
                            quiz_running = False 
                        break 
        
        # --- Desenho da Tela do Quiz ---
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(BLUE_BACKGROUND) 

        pygame.draw.rect(screen, BLACK, GAME_SCREEN_RECT)
        
        # Pergunta Atual
        question = quiz_data[current_question_index]
        question_text_surf = small_font.render(question["pergunta"], True, TEXT_COLOR)
        question_text_rect = question_text_surf.get_rect(center=(GAME_SCREEN_RECT.centerx, GAME_SCREEN_RECT.y + 30))
        screen.blit(question_text_surf, question_text_rect)
        
        # Desenha as Opções como Botões
        for letter, rect in option_rects.items():
            option_display_text = f"{letter}. {question['opcoes'][letter]}"
            draw_button(screen, rect, option_display_text, smaller_font, BUTTON_BLUE, BUTTON_HOVER_BLUE, mouse_pos, border_radius=10)

        pygame.display.flip()

# 🏆 Função para a Tela de Resultado
def result_screen():
    global squirtle, charmander, bulbasaur
    
    pokemon_pontos = {"Squirtle": squirtle, "Charmander": charmander, "Bulbasaur": bulbasaur}
    vencedor_chave = ""
    resultado_final = ""
    
    # SUA LÓGICA EXATA DE RESULTADO
    if(squirtle > charmander and squirtle > bulbasaur):
        resultado_final = "Parabéns! Seu pokémon é o Squirtle!"
        vencedor_chave = "Squirtle"
    elif(charmander > squirtle and charmander > bulbasaur):
        resultado_final = "Parabéns! Seu pokémon é o Charmander!"
        vencedor_chave = "Charmander"
    elif(bulbasaur > squirtle and bulbasaur > charmander):
        resultado_final = "Parabéns! Seu pokémon é o Bulbasaur!"
        vencedor_chave = "Bulbasaur"
    elif(squirtle == charmander and squirtle > bulbasaur):
        resultado_final = "OMG! Dois pokémon te escolheram! Parabéns agora você tem um Squirtle e um Charmander! <3"
        vencedor_chave = "Empate SC"
    elif(squirtle == bulbasaur and squirtle > charmander):
        resultado_final = "OMG! Dois pokémon te escolheram! Parabéns agora você tem um Squirtle e um Bulbasaur! <3"
        vencedor_chave = "Empate SB"
    elif(charmander == bulbasaur and charmander > squirtle):
        resultado_final = "OMG! Dois pokémon te escolheram! Parabéns agora você tem um Bulbasaur e um Charmander! <3"
        vencedor_chave = "Empate CB"

    result_running = True
    while result_running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()
                return 

        # Desenho
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(BLUE_BACKGROUND) 
        
        pygame.draw.rect(screen, BLACK, GAME_SCREEN_RECT)

        title_text = font.render("RESULTADO FINAL!", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(GAME_SCREEN_RECT.centerx, GAME_SCREEN_RECT.y + 30)) 
        screen.blit(title_text, title_rect)

        # 🖼️ DESENHO DO SPRITE DO VENCEDOR
        sprite_drawn = False
        if vencedor_chave in POKEMON_SPRITES:
            sprite = POKEMON_SPRITES.get(vencedor_chave)
            if sprite:
                sprite_x = GAME_SCREEN_RECT.centerx - (SPRITE_SIZE // 2)
                sprite_y = GAME_SCREEN_RECT.y + 70 
                screen.blit(sprite, (sprite_x, sprite_y))
                sprite_drawn = True

        # Posição do texto ajustada
        text_y_result = GAME_SCREEN_RECT.y + 180 if sprite_drawn else (GAME_SCREEN_RECT.centerx) 
        result_text = small_font.render(resultado_final, True, TEXT_COLOR)
        result_rect = result_text.get_rect(center=(GAME_SCREEN_RECT.centerx, text_y_result))
        screen.blit(result_text, result_rect)
        
        # Pontuações
        y_pos_scores = text_y_result + 30
        for pk, pontos in pokemon_pontos.items():
            score_text = smaller_font.render(f"{pk}: {pontos} pontos", True, TEXT_COLOR)
            score_rect = score_text.get_rect(center=(GAME_SCREEN_RECT.centerx, y_pos_scores))
            screen.blit(score_text, score_rect)
            y_pos_scores += 20
            
        # Instrução
        instruction_text = smaller_font.render("Clique para recomeçar.", True, TEXT_COLOR)
        instruction_rect = instruction_text.get_rect(center=(GAME_SCREEN_RECT.centerx, GAME_SCREEN_RECT.y + GAME_SCREEN_HEIGHT - 10))
        screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()


# 🎮 Loop Principal do Jogo (Tela Inicial)
def game_loop():
    running = True
    
    # ⚠️ COORDENADAS DO BOTÃO CIRCULAR START (Ajustar no Figma)
    start_button_center_x = SCREEN_WIDTH // 2
    start_button_center_y = 500 
    start_button_radius = 40 
    
    start_button_rect = pygame.Rect(
        start_button_center_x - start_button_radius, 
        start_button_center_y - start_button_radius, 
        start_button_radius * 2, 
        start_button_radius * 2
    )

    while running:
        mouse_pos = pygame.mouse.get_pos()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # --- Desenho ---
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill(BLUE_BACKGROUND) 
        
        pygame.draw.rect(screen, BLACK, GAME_SCREEN_RECT)

        # Título (Na tela preta)
        title_text = font.render(SCREEN_TITLE, True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(GAME_SCREEN_RECT.centerx, GAME_SCREEN_RECT.y + 50))
        screen.blit(title_text, title_rect)
        
        intro_message = small_font.render("Qual o seu Pokémon perfeito para você? Descubra!", True, TEXT_COLOR)
        intro_rect = intro_message.get_rect(center=(GAME_SCREEN_RECT.centerx, GAME_SCREEN_RECT.y + 100))
        screen.blit(intro_message, intro_rect)


        if pygame.mouse.get_pressed()[0] == 1 and start_button_rect.collidepoint(mouse_pos):
            quiz_screen() 
            running = False 

        pygame.display.flip()

# ⏱️ Relógio para controle de FPS
clock = pygame.time.Clock()

# 🚀 Inicia o Jogo
if __name__ == "__main__":
    game_loop()
