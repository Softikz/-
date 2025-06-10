import pygame as pg
from datetime import datetime


class MenuBank:
    def __init__(self, screen, player_data):
        self.screen = screen
        self.player_data = player_data
        self.width, self.height = screen.get_size()

        # Шрифты и цвета (остаются без изменений)
        self.font_title = pg.font.SysFont('Arial', 48, bold=True)
        self.font_text = pg.font.SysFont('Arial', 32)
        self.font_small = pg.font.SysFont('Arial', 24)
        self.background_color = (30, 30, 50)
        self.title_color = (220, 180, 60)
        self.text_color = (255, 255, 255)
        self.money_color = (0, 255, 0)
        self.interest_color = (100, 255, 100)
        self.button_color = (70, 100, 150)

        # Кнопки
        self.back_button = pg.Rect(50, 500, 200, 50)
        self.deposit_button = pg.Rect(self.width // 2 - 250, 300, 200, 50)
        self.withdraw_button = pg.Rect(self.width // 2 + 50, 300, 200, 50)

    def check_interest(self):
        """Проверка необходимости начисления процентов"""
        today = datetime.now().date()
        last_date = datetime.fromisoformat(self.player_data['last_interest_date']).date()
        return today > last_date

    def draw(self):
        self.screen.fill(self.background_color)

        # Заголовок
        title = self.font_title.render("Банк", True, self.title_color)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

        # Баланс
        balance_text = self.font_text.render(
            f"Баланс: ${self.player_data.get('balance', 0):,}",
            True,
            self.money_color
        )
        self.screen.blit(balance_text, (self.width // 2 - balance_text.get_width() // 2, 150))

        # Депозит
        deposit_text = self.font_text.render(
            f"Депозит: ${self.player_data.get('deposit', 0):,}",
            True,
            self.text_color
        )
        self.screen.blit(deposit_text, (self.width // 2 - deposit_text.get_width() // 2, 200))

        # Проценты
        interest_text = self.font_text.render(
            f"Накопленные проценты: ${self.player_data.get('interest', 0):.2f}",
            True,
            self.interest_color
        )
        self.screen.blit(interest_text, (self.width // 2 - interest_text.get_width() // 2, 250))

        # Информация о процентах
        status = "Сегодня проценты уже начислены" if not self.check_interest() else "Проценты будут начислены в 00:00"
        status_text = self.font_small.render(status, True, (180, 180, 180))
        self.screen.blit(status_text, (self.width // 2 - status_text.get_width() // 2, 450))

        # Кнопки
        self.draw_button(self.deposit_button, "Пополнить депозит")
        self.draw_button(self.withdraw_button, "Снять с депозита")
        self.draw_button(self.back_button, "Назад")

        # Информация о процентах
        info_text = self.font_small.render(
            "Проценты начисляются ежедневно в 00:00 (5% годовых)",
            True,
            (180, 180, 180)
        )
        self.screen.blit(info_text, (self.width // 2 - info_text.get_width() // 2, 450))

    def draw_button(self, rect, text):
        mouse_pos = pg.mouse.get_pos()
        color = (90, 130, 180) if rect.collidepoint(mouse_pos) else self.button_color

        pg.draw.rect(self.screen, color, rect, border_radius=10)
        pg.draw.rect(self.screen, (40, 40, 60), rect, 3, border_radius=10)

        text_surf = self.font_text.render(text, True, self.text_color)
        self.screen.blit(text_surf, (
            rect.centerx - text_surf.get_width() // 2,
            rect.centery - text_surf.get_height() // 2
        ))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                if self.back_button.collidepoint(event.pos):
                    return "back"
                elif self.deposit_button.collidepoint(event.pos):
                    return "deposit"
                elif self.withdraw_button.collidepoint(event.pos):
                    return "withdraw"
        return None
