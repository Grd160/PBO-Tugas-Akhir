import pygame
from Setting import *

_PANEL_BG     = (22, 22, 40)
_PANEL_BORDER = (90, 90, 200)
_OPT_NORMAL   = (38, 38, 70)
_OPT_HOVER    = (60, 55, 120)
_BORDER_HOV   = (255, 210, 0)
_BORDER_NRM   = (65, 65, 115)

_STAT_LABELS = {
    "hp":       ("MAX HP  +25",    "Tambah HP maksimum & pulihkan 25 HP",  (80, 200, 120)),
    "damage":   ("DAMAGE  +5",     "Setiap peluru +5 damage tambahan",     (220, 100, 100)),
    "firerate": ("FIRE RATE  +15%","Kecepatan tembak meningkat 15%",       (100, 180, 255)),
}

_STAT_COLORS = {
    "hp":       (80,  200, 120),
    "damage":   (220, 100, 100),
    "firerate": (100, 180, 255),
}

PANEL_W = 580
PANEL_H = 460
OPT_W   = 500
OPT_H   = 82
OPT_GAP = 14

class LevelUpSystem:
    def __init__(self):
        self.kills = 0
        self.level = 1
        self.kills_per_level = 5
        self.pending_levelup = False

        self.damage_bonus = 0      
        self.hp_bonus = 0         
        self.fire_rate_bonus = 0 

        self.font_title = pygame.font.SysFont(None, 64)
        self.font_option = pygame.font.SysFont(None, 40)
        self.font_desc = pygame.font.SysFont(None, 28)

        self.font_title  = pygame.font.SysFont(None, 60)
        self.font_label  = pygame.font.SysFont(None, 38)
        self.font_desc   = pygame.font.SysFont(None, 27)
        self.font_hint   = pygame.font.SysFont(None, 25)

        self.options = ["hp", "damage", "firerate"]
        self.hovered = 0

    def register_kill(self):
        self.kills += 1

        if self.kills >= self.kills_per_level * self.level:
            self.pending_levelup = True

    def handle_event(self, event, player):
        if not self.pending_levelup:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.hovered = (self.hovered - 1) % len(self.options)

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.hovered = (self.hovered + 1) % len(self.options)

            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._apply(self.options[self.hovered], player)

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos

            for i, rect in enumerate(self._option_rects()):

                if rect.collidepoint(mx, my):
                    self.hovered = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            for i, rect in enumerate(self._option_rects()):

                if rect.collidepoint(mx, my):
                    self._apply(self.options[i], player)
                    break

    def _apply(self, stat, player):
        if stat == "hp":
            self.hp_bonus += 25
            new_hp = min(player.get_hp() + 25, 100 + self.hp_bonus)
            player.set_hp(new_hp)
            player.set_max_hp(100 + self.hp_bonus)

        elif stat == "damage":
            self.damage_bonus += 5
            player.set_damage_bonus(self.damage_bonus)

        elif stat == "firerate":
            self.fire_rate_bonus += 0.15
            player.set_fire_rate_bonus(self.fire_rate_bonus)

        self.level += 1
        self.pending_levelup = False
        self.hovered = 0

    def _panel_rect(self):
        return pygame.Rect(
            WIDTH  // 2 - PANEL_W // 2,
            HEIGHT // 2 - PANEL_H // 2,
            PANEL_W, PANEL_H
        )

    def _option_rects(self):
        return pygame.Rect(
            WIDTH  // 2 - PANEL_W // 2,
            HEIGHT // 2 - PANEL_H // 2,
            PANEL_W, PANEL_H
        )
    
    def _option_rects(self):
        panel = self._panel_rect()
        rects = []
        start_y = panel.top + 140
        ox = WIDTH // 2 - OPT_W // 2

        for i in range(len(self.options)):
            rects.append(pygame.Rect(ox, start_y + i * (OPT_H + OPT_GAP), OPT_W, OPT_H))

        return rects

    def draw(self, screen):
        if not self.pending_levelup:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        panel = self._panel_rect()

        shadow = panel.inflate(8, 8)
        shadow_surf = pygame.Surface((shadow.width, shadow.height), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 120))
        screen.blit(shadow_surf, shadow.topleft)

        pygame.draw.rect(screen, _PANEL_BG, panel, border_radius=18)
        pygame.draw.rect(screen, _PANEL_BORDER, panel, 2, border_radius=18)

        title_text = f"LEVEL UP!   Lv. {self.level}"
        title = self.font_title.render(title_text, True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, panel.top + 22))

        sep_y = panel.top + 90
        pygame.draw.line(screen, (60, 60, 110),
                         (panel.left + 20, sep_y), (panel.right - 20, sep_y), 1)

        sub = self.font_desc.render("Pilih satu peningkatan permanen:", True, (160, 160, 210))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, sep_y + 8))

        for i, (stat, rect) in enumerate(zip(self.options, self._option_rects())):
            is_hovered = i == self.hovered
            label_str, desc_str, accent = _STAT_LABELS[stat]
            color_dot = _STAT_COLORS[stat]

            bg  = _OPT_HOVER  if is_hovered else _OPT_NORMAL
            brd = _BORDER_HOV if is_hovered else _BORDER_NRM
            pygame.draw.rect(screen, bg,  rect, border_radius=11)
            pygame.draw.rect(screen, brd, rect, 2, border_radius=11)

            dot = pygame.Rect(rect.x + 16, rect.y + rect.height // 2 - 10, 20, 20)
            pygame.draw.rect(screen, color_dot, dot, border_radius=5)

            lbl_color = WHITE if is_hovered else (210, 210, 210)
            lbl = self.font_label.render(label_str, True, lbl_color)
            screen.blit(lbl, (rect.x + 46, rect.y + 12))

            desc = self.font_desc.render(desc_str, True, (150, 195, 155))
            screen.blit(desc, (rect.x + 46, rect.y + 50))

        hint = self.font_desc.render("W / S untuk navigasi  •  ENTER / Klik untuk pilih", True, (90, 90, 140))
        hint_y = self._option_rects()[-1].bottom + 14
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, hint_y))
 