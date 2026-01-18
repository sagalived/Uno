import pygame

CARD_W, CARD_H = 80, 110
COLORS_RGB = {
    "red": (220, 60, 60), "green": (60, 180, 90),
    "blue": (60, 100, 220), "yellow": (240, 200, 60),
    "wild": (40, 40, 40)
}

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arialblack", 16)
        self.ui_font = pygame.font.SysFont("arialblack", 20)
        self.timer_font = pygame.font.SysFont("arialblack", 25)
        self.win_font = pygame.font.SysFont("arialblack", 70)

    def clear(self):
        self.screen.fill((20, 70, 20))

    def draw_timer(self, seconds_left):
        # Converte segundos para formato MM:SS
        mins = int(seconds_left // 60)
        secs = int(seconds_left % 60)
        timer_str = f"TEMPO: {mins:02d}:{secs:02d}"
        
        # Cor muda para vermelho se faltar menos de 30 segundos
        cor = (255, 255, 255) if seconds_left > 30 else (255, 50, 50)
        txt = self.timer_font.render(timer_str, True, cor)
        self.screen.blit(txt, (1050, 12))

    def draw_interface(self, game, mouse_pos):
        pygame.draw.rect(self.screen, (10, 30, 10), (0, 0, 1280, 60))
        # Botão Dificuldade
        cor_diff = (200, 0, 0) if game.dificuldade == "Difícil" else (0, 200, 0)
        pygame.draw.rect(self.screen, cor_diff, (540, 15, 200, 35), border_radius=8)
        txt_diff = self.ui_font.render(game.dificuldade, True, (255, 255, 255))
        self.screen.blit(txt_diff, txt_diff.get_rect(center=(640, 32)))

        status = ["Sua Vez", "Vez P1", "Vez P2", "Vez P3"]
        txt_s = self.ui_font.render(status[game.turn], True, (255, 255, 255))
        self.screen.blit(txt_s, (20, 15))

    def draw_card(self, card, x, y, scale=1.0):
        val, cor = card
        w, h = int(CARD_W * scale), int(CARD_H * scale)
        color_rgb = COLORS_RGB.get(cor, (100, 100, 100))
        if scale > 1.0:
            x -= (w - CARD_W) // 2
            y -= (h - CARD_H) // 2
        pygame.draw.rect(self.screen, color_rgb, (x, y, w, h), border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (x+4, y+4, w-8, h-8), border_radius=8)
        txt = self.font.render(str(val), True, color_rgb)
        self.screen.blit(txt, txt.get_rect(center=(x + w//2, y + h//2)))

    def draw_players(self, game, mouse_pos):
        for i, card in enumerate(game.players[0]):
            x_pos = 200 + i * 50
            y_pos = 720
            scale = 1.15 if (x_pos < mouse_pos[0] < x_pos + 50 and y_pos < mouse_pos[1] < y_pos + 110) else 1.0
            self.draw_card(card, x_pos, y_pos, scale)
        for i, card in enumerate(game.players[1]): self.draw_card(card, 20, 150 + i * 40)
        for i, card in enumerate(game.players[2]): self.draw_card(card, 350 + i * 50, 60)
        for i, card in enumerate(game.players[3]): self.draw_card(card, 1170, 150 + i * 40)

    def draw_table(self, game):
        pygame.draw.rect(self.screen, (0, 0, 0), (520, 350, CARD_W, CARD_H), border_radius=10)
        if game.table:
            pygame.draw.rect(self.screen, (255, 255, 255), (635, 345, CARD_W+10, CARD_H+10), border_radius=12)
            self.draw_card(game.table[-1], 640, 350)

    def draw_winner(self, winner_idx, motivo=""):
        overlay = pygame.Surface((1280, 900), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))
        
        texto = "VOCÊ VENCEU!" if winner_idx == 0 else f"PLAYER {winner_idx} VENCEU!"
        if motivo == "timeout":
            texto = "TEMPO ESGOTADO! VOCÊ PERDEU!"
            
        res = self.win_font.render(texto, True, (255, 215, 0))
        self.screen.blit(res, res.get_rect(center=(640, 450)))