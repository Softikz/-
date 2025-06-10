import pygame as pg


class MainMenu:
    def __init__(self, screen, toggle_fullscreen_callback):
        self.screen = screen
        self.toggle_fullscreen = toggle_fullscreen_callback
        self.width, self.height = screen.get_size()
        self.init_ui()

    def init_ui(self):
        self.font_large = pg.font.SysFont('Arial', int(self.height / 15), bold=True)
        self.font_medium = pg.font.SysFont('Arial', int(self.height / 20))

        # Расположение кнопок
        button_width = self.width // 4
        button_height = self.height // 12
        margin = self.height // 15

        self.buttons = {
            "Статистика": pg.Rect(margin, margin * 4, button_width, button_height),
            "Банк": pg.Rect(margin, margin * 5.5, button_width, button_height),
            "Донат": pg.Rect(self.width - button_width - margin, margin * 4, button_width, button_height),
            "Полный экран": pg.Rect(self.width - button_width - margin, margin * 5.5, button_width, button_height),
            "Выход": pg.Rect(self.width // 2 - button_width // 2, self.height - margin * 2, button_width, button_height)
        }

    def draw(self):
        self.screen.fill((30, 30, 50))

        # Заголовок
        title = self.font_large.render("Poker House", True, (220, 180, 60))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 8))

        # Кнопки
        for text, rect in self.buttons.items():
            mouse_pos = pg.mouse.get_pos()
            color = (90, 130, 180) if rect.collidepoint(mouse_pos) else (70, 100, 150)

            pg.draw.rect(self.screen, color, rect, border_radius=10)
            pg.draw.rect(self.screen, (40, 40, 60), rect, 3, border_radius=10)

            text_surf = self.font_medium.render(text, True, (255, 255, 255))
            self.screen.blit(text_surf, (
                rect.centerx - text_surf.get_width() // 2,
                rect.centery - text_surf.get_height() // 2
            ))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for text, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    if text == "Полный экран":
                        self.toggle_fullscreen()
                        return "resize"
                    elif text == "Выход":
                        return "quit"
                    else:
                        # Возвращаем текст кнопки в нижнем регистре
                        return text.lower()
        return None