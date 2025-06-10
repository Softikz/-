import pygame as pg


class MenuStats:
    def __init__(self, screen, player_data):
        self.screen = screen
        self.player_data = player_data
        self.width, self.height = screen.get_size()

        # Шрифты
        self.font_title = pg.font.SysFont('Arial', 48, bold=True)
        self.font_text = pg.font.SysFont('Arial', 32)

        # Цвета
        self.background_color = (30, 30, 50)
        self.title_color = (220, 180, 60)
        self.text_color = (255, 255, 255)
        self.money_color = (0, 255, 0)

        # Кнопка "Назад"
        self.back_button = pg.Rect(50, 500, 200, 50)

    def draw(self):
        self.screen.fill(self.background_color)

        # Заголовок
        title = self.font_title.render("Моя статистика", True, self.title_color)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

        # Данные игрока
        stats = [
            f"Текущий баланс: ${self.player_data.get('balance', 0):,}",
            f"Игр сыграно: {self.player_data.get('games_played', 0)}",
            f"Побед: {self.player_data.get('wins', 0)} ({self.win_rate()}%)",
            f"Макс. выигрыш: ${self.player_data.get('max_win', 0):,}",
            f"Общий доход: ${self.player_data.get('total_earnings', 0):,}"
        ]

        for i, stat in enumerate(stats):
            color = self.money_color if i == 0 else self.text_color
            text = self.font_text.render(stat, True, color)
            self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 150 + i * 50))

        # Кнопка "Назад"
        pg.draw.rect(self.screen, (70, 100, 150), self.back_button, border_radius=10)
        back_text = self.font_text.render("Назад", True, self.text_color)
        self.screen.blit(back_text, (
            self.back_button.centerx - back_text.get_width() // 2,
            self.back_button.centery - back_text.get_height() // 2
        ))

    def win_rate(self):
        games = max(1, self.player_data.get('games_played', 1))
        return int((self.player_data.get('wins', 0) / games) * 100)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.back_button.collidepoint(event.pos):
                return "back"
        return None
