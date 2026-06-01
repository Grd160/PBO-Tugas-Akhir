import pygame
from Setting import *
from Stage.StageList import ALL_STAGES

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.state = "main"        
        self.selected_stage = 0
        self.selected_difficulty = 1 

        self.font_title = pygame.font.SysFont(None, 96)
        self.font_menu  = pygame.font.SysFont(None, 52)
        self.font_small = pygame.font.SysFont(None, 34)

        self.difficulties = ["Easy", "Normal", "Hard"]

        self.main_items = ["Play", "Stage", "Difficulty", "Exit"]
        self.main_hovered = 0

    # ── Public ──────────────────────────────────────────────

    def handle_event(self, event):
        """Returns 'play', 'exit', or None."""

        if self.state == "main":
            return self._handle_main(event)
        
        elif self.state == "stage":
            self._handle_stage(event)

        elif self.state == "difficulty":
            self._handle_difficulty(event)

        return None

    def draw(self):
        self.screen.fill((20, 20, 35))

        if self.state == "main":
            self._draw_main()

        elif self.state == "stage":
            self._draw_stage()

        elif self.state == "difficulty":
            self._draw_difficulty()

    def get_selected_stage(self):
        return ALL_STAGES[self.selected_stage]

    def get_difficulty(self):
        return self.difficulties[self.selected_difficulty]

    def get_difficulty_multiplier(self):
        """Returns enemy stat multiplier based on difficulty."""
        return [0.7, 1.0, 1.5][self.selected_difficulty]

    # ── Main menu ───────────────────────────────────────────

    def _handle_main(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_UP, pygame.K_w):
                self.main_hovered = (self.main_hovered - 1) % len(self.main_items)

            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.main_hovered = (self.main_hovered + 1) % len(self.main_items)

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self._select_main(self.main_hovered)

        if event.type == pygame.MOUSEMOTION:

            for i, rect in enumerate(self._main_rects()):

                if rect.collidepoint(event.pos):
                    self.main_hovered = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            for i, rect in enumerate(self._main_rects()):

                if rect.collidepoint(event.pos):

                    return self._select_main(i)
                
        return None

    def _select_main(self, idx):
        label = self.main_items[idx]

        if label == "Play":
            return "play"
        
        elif label == "Stage":
            self.state = "stage"

        elif label == "Difficulty":
            self.state = "difficulty"

        elif label == "Exit":

            return "exit"
        
        return None

    def _main_rects(self):
        rects = []
        start_y = 320

        for i in range(len(self.main_items)):
            rects.append(pygame.Rect(WIDTH // 2 - 160, start_y + i * 80, 320, 60))

        return rects

    def _draw_main(self):
        title = self.font_title.render("SHOOTER GAME", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))

        sub = self.font_small.render("by Kelompok 4", True, (120, 120, 160))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 265))

        for i, (label, rect) in enumerate(zip(self.main_items, self._main_rects())):
            is_hov = i == self.main_hovered
            bg = (60, 60, 120) if is_hov else (35, 35, 65)
            border = YELLOW if is_hov else (70, 70, 120)
            pygame.draw.rect(self.screen, bg, rect, border_radius=10)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=10)

            text = self.font_menu.render(label, True, WHITE if is_hov else (180, 180, 200))
            self.screen.blit(text, (rect.centerx - text.get_width() // 2,
                                    rect.centery - text.get_height() // 2))

        hint = self.font_small.render("↑↓ / Mouse  •  ENTER untuk pilih", True, (80, 80, 120))
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 50))

    def _handle_stage(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                self.state = "main"

            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected_stage = (self.selected_stage - 1) % len(ALL_STAGES)

            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected_stage = (self.selected_stage + 1) % len(ALL_STAGES)

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = "main"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            left_rect  = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 40, 60, 80)
            right_rect = pygame.Rect(WIDTH // 2 + 240, HEIGHT // 2 - 40, 60, 80)
            back_rect  = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 120, 160, 50)

            if left_rect.collidepoint(event.pos):
                self.selected_stage = (self.selected_stage - 1) % len(ALL_STAGES)

            if right_rect.collidepoint(event.pos):
                self.selected_stage = (self.selected_stage + 1) % len(ALL_STAGES)

            if back_rect.collidepoint(event.pos):
                self.state = "main"

    def _draw_stage(self):
        stage = ALL_STAGES[self.selected_stage]

        title = self.font_menu.render("Pilih Stage", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        card = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 130, 440, 260)
        pygame.draw.rect(self.screen, (40, 40, 80), card, border_radius=14)
        pygame.draw.rect(self.screen, (100, 100, 200), card, 2, border_radius=14)

        name_text = self.font_menu.render(stage.name, True, WHITE)
        self.screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 - 110))

        desc_text = self.font_small.render(stage.description, True, (160, 200, 160))
        self.screen.blit(desc_text, (WIDTH // 2 - desc_text.get_width() // 2, HEIGHT // 2 - 50))

        idx_text = self.font_small.render(
            f"Stage {self.selected_stage + 1} / {len(ALL_STAGES)}", True, (120, 120, 180)
        )
        self.screen.blit(idx_text, (WIDTH // 2 - idx_text.get_width() // 2, HEIGHT // 2 + 80))

        left_rect  = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 40, 60, 80)
        right_rect = pygame.Rect(WIDTH // 2 + 240, HEIGHT // 2 - 40, 60, 80)
        pygame.draw.rect(self.screen, (55, 55, 100), left_rect,  border_radius=8)
        pygame.draw.rect(self.screen, (55, 55, 100), right_rect, border_radius=8)

        arr_l = self.font_menu.render("<", True, WHITE)
        arr_r = self.font_menu.render(">", True, WHITE)
        self.screen.blit(arr_l, (left_rect.centerx  - arr_l.get_width() // 2, left_rect.centery  - arr_l.get_height() // 2))
        self.screen.blit(arr_r, (right_rect.centerx - arr_r.get_width() // 2, right_rect.centery - arr_r.get_height() // 2))

        back_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 120, 160, 50)
        pygame.draw.rect(self.screen, (50, 50, 90), back_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 170), back_rect, 2, border_radius=8)
        back_text = self.font_small.render("← Kembali", True, WHITE)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2,
                                     back_rect.centery - back_text.get_height() // 2))

    def _handle_difficulty(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.state = "main"

            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected_difficulty = (self.selected_difficulty - 1) % 3

            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected_difficulty = (self.selected_difficulty + 1) % 3

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = "main"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            back_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 120, 160, 50)

            if back_rect.collidepoint(event.pos):
                self.state = "main"

            for i, rect in enumerate(self._diff_rects()):

                if rect.collidepoint(event.pos):
                    self.selected_difficulty = i

    def _diff_rects(self):
        rects = []

        for i in range(3):
            rects.append(pygame.Rect(WIDTH // 2 - 240 + i * 170, HEIGHT // 2 - 50, 150, 100))

        return rects

    def _draw_difficulty(self):
        colors_bg = [(0, 120, 60), (30, 80, 160), (140, 20, 20)]
        colors_bd = [(0, 220, 100), (60, 140, 255), (255, 60, 60)]
        labels    = ["Easy", "Normal", "Hard"]
        descs     = ["Musuh lemah", "Standar", "Musuh kuat"]

        title = self.font_menu.render("Pilih Difficulty", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        for i, (rect, lbl, desc) in enumerate(zip(self._diff_rects(), labels, descs)):
            is_sel = i == self.selected_difficulty
            bg  = colors_bg[i] if is_sel else (35, 35, 65)
            brd = colors_bd[i] if is_sel else (70, 70, 110)
            pygame.draw.rect(self.screen, bg,  rect, border_radius=12)
            pygame.draw.rect(self.screen, brd, rect, 3, border_radius=12)

            t = self.font_menu.render(lbl, True, WHITE)
            self.screen.blit(t, (rect.centerx - t.get_width() // 2, rect.y + 20))

            d = self.font_small.render(desc, True, (180, 220, 180))
            self.screen.blit(d, (rect.centerx - d.get_width() // 2, rect.y + 66))

        cur = self.font_small.render(
            f"Saat ini: {self.difficulties[self.selected_difficulty]}", True, (160, 160, 200)
        )
        self.screen.blit(cur, (WIDTH // 2 - cur.get_width() // 2, HEIGHT // 2 + 90))

        back_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 120, 160, 50)
        pygame.draw.rect(self.screen, (50, 50, 90), back_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 170), back_rect, 2, border_radius=8)
        back_text = self.font_small.render("← Kembali", True, WHITE)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2,
                                     back_rect.centery - back_text.get_height() // 2))