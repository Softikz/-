import pygame as pg


class MenuDonate:
    def __init__(self, screen, player_data):
        self.screen = screen
        self.player_data = player_data
        self.width, self.height = screen.get_size()
        self.init_ui()

    def init_ui(self):
        self.font_title = pg.font.SysFont('Arial', int(self.height / 15), bold=True)
        self.font_text = pg.font.SysFont('Arial', int(self.height / 20))

        # Кнопки
        button_width = self.width // 3
        button_height = self.height // 10
        margin = self.height // 20

        self.back_button = pg.Rect(
            margin,
            self.height - button_height - margin,
            button_width,
            button_height
        )

        self.premium_button = pg.Rect(
            self.width // 2 - button_width // 2,
            margin * 4,
            button_width,
            button_height
        )

        # Пакеты денег
        self.packages = [
            {"amount": 1000, "price": 0.99, "rect": pg.Rect(margin, margin * 6, button_width, button_height)},
            {"amount": 5000, "price": 3.99,
             "rect": pg.Rect(self.width - button_width - margin, margin * 6, button_width, button_height)},
            {"amount": 10000, "price": 6.99, "rect": pg.Rect(margin, margin * 8, button_width, button_height)},
            {"amount": 25000, "price": 14.99,
             "rect": pg.Rect(self.width - button_width - margin, margin * 8, button_width, button_height)}
        ]

    def draw(self):
        self.screen.fill((30, 30, 50))

        # Заголовок
        title = self.font_title.render("Пополнение баланса", True, (220, 180, 60))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 10))

        # Кнопка премиума
        self.draw_button(
            self.premium_button,
            "Премиум" if self.player_data['premium'] else "Купить премиум",
            (100, 100, 100) if self.player_data['premium'] else (255, 215, 0)
        )

        # Пакеты
        for package in self.packages:
            self.draw_package_button(package)

        # Кнопка назад
        self.draw_button(self.back_button, "Назад")

    def draw_button(self, rect, text, color=None):
        color = color or (70, 100, 150)
        mouse_pos = pg.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            color = tuple(min(c + 30, 255) for c in color)

        pg.draw.rect(self.screen, color, rect, border_radius=10)
        text_surf = self.font_text.render(text, True, (255, 255, 255))
        self.screen.blit(text_surf, (
            rect.centerx - text_surf.get_width() // 2,
            rect.centery - text_surf.get_height() // 2
        ))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return "back"

            if (self.premium_button.collidepoint(event.pos) and
                    not self.player_data['premium']):
                return {"action": "buy_premium", "price": 4.99}

            for package in self.packages:
                if package["rect"].collidepoint(event.pos):
                    return {
                        "action": "buy_currency",
                        "amount": package["amount"],
                        "price": package["price"]
                    }
        return None