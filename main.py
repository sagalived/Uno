import pygame as pg
from game import UnoGame
from rendering import Renderer
from input_handler import InputHandler
from cards import can_play

pg.init()
window = pg.display.set_mode((1280, 900))
renderer = Renderer(window)
inputs = InputHandler()
game = UnoGame()

winner = None
win_reason = ""
ai_timer = 0
# 300 segundos = 5 minutos
MAX_TIME = 300
player_timer = MAX_TIME

while True:
    dt = pg.time.Clock().tick(60) # dt em milisegundos
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit(); exit()

    mouse_pos, _, mouse_click = inputs.get()

    if winner is None:
        # Lógica do Cronômetro (Apenas na vez do jogador 0)
        if game.turn == 0:
            player_timer -= dt / 1000 # Subtrai segundos
            if player_timer <= 0:
                winner = 1 # IA vence automaticamente
                win_reason = "timeout"
        else:
            # Opcional: Resetar o tempo quando a vez volta para você
            # player_timer = MAX_TIME 
            pass

        # Lógica da IA
        delay = 1500 if game.dificuldade == "Fácil" else 1000 if game.dificuldade == "Médio" else 400
        if game.turn != 0:
            ai_timer += dt
            if ai_timer > delay:
                idx = game.IA_decidir_jogada(game.players[game.turn], game.table[-1])
                if idx is not None:
                    game.play_card(game.turn, idx)
                else:
                    if game.deck: game.players[game.turn].append(game.deck.pop())
                    game.next_player()
                ai_timer = 0
                res = game.check_winner()
                if res is not None: winner = res

        # Lógica do Jogador
        elif game.turn == 0 and mouse_click:
            # Menu Dificuldade
            if 540 < mouse_pos[0] < 740 and 15 < mouse_pos[1] < 50:
                game.mudar_dificuldade()
                pg.time.delay(200)

            # Comprar
            if 520 < mouse_pos[0] < 600 and 350 < mouse_pos[1] < 460:
                if game.deck:
                    game.players[0].append(game.deck.pop())
                    game.next_player()
                    player_timer = MAX_TIME # Reset tempo após jogar/comprar
                pg.time.delay(200)

            # Jogar carta
            for i, card in enumerate(game.players[0]):
                x_pos = 200 + i * 50
                if x_pos < mouse_pos[0] < x_pos + 50 and 720 < mouse_pos[1] < 830:
                    if can_play(game.table[-1], card):
                        game.play_card(0, i)
                        player_timer = MAX_TIME # Reset tempo após jogar
                        res = game.check_winner()
                        if res is not None: winner = res
                        pg.time.delay(200)
                        break

    # RENDERIZAÇÃO
    renderer.clear()
    renderer.draw_interface(game, mouse_pos)
    renderer.draw_timer(player_timer) # Desenha o relógio
    renderer.draw_table(game)
    renderer.draw_players(game, mouse_pos)
    
    if winner is not None:
        renderer.draw_winner(winner, win_reason)
        
    pg.display.update()