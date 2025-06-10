import pygame as pg
from datetime import datetime, timedelta, time
from MainMenu import MainMenu
from MenuStats import MenuStats
from MenuBank import MenuBank
from MenuDonate import MenuDonate


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Poker House")
        self.clock = pg.time.Clock()
        self.running = True

        # Данные игрока
        self.player_data = {
            'balance': 15300,
            'deposit': 0,
            'interest': 0,
            'last_interest_date': datetime.now().date().isoformat(),
            'premium': False,
            'games_played': 127,
            'wins': 83,
            'losses': 44,
            'max_win': 12500,
            'total_earnings': 38200
        }

        # Инициализация экранов
        self.current_screen = None
        self.main_menu = MainMenu(self.screen)
        self.stats_screen = MenuStats(self.screen, self.player_data)
        self.bank_screen = MenuBank(self.screen, self.player_data)
        self.donate_screen = MenuDonate(self.screen, self.player_data)

        self.switch_to_menu()

    def switch_to_menu(self):
        self.current_screen = self.main_menu

    def switch_to_stats(self):
        self.stats_screen = MenuStats(self.screen, self.player_data)
        self.current_screen = self.stats_screen

    def deposit_money(self, amount=1000):
        if self.player_data['balance'] >= amount:
            self.player_data['balance'] -= amount
            self.player_data['deposit'] += amount
            print(f"Пополнен депозит на ${amount:,}")

    def withdraw_money(self, amount=1000):
        if self.player_data['deposit'] >= amount:
            self.player_data['deposit'] -= amount
            self.player_data['balance'] += amount
            print(f"Снято с депозита ${amount:,}")

    def calculate_daily_interest(self):
        """Начисление ежедневных процентов (5% годовых)"""
        today = datetime.now().date()
        last_date = datetime.fromisoformat(self.player_data['last_interest_date']).date()

        if today > last_date:
            days_passed = (today - last_date).days
            if days_passed > 0:
                daily_rate = 0.05 / 365
                interest = self.player_data['deposit'] * daily_rate * days_passed
                self.player_data['interest'] += interest
                self.player_data['last_interest_date'] = today.isoformat()
                print(f"Начислены проценты за {days_passed} дней: ${interest:.2f}")

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:
                    self.toggle_fullscreen()

            if self.current_screen:
                result = self.current_screen.handle_event(event)
                self.process_screen_result(result)

    def process_screen_result(self, result):
        if not result:
            return

        if result == "back":
            self.switch_to_menu()
        elif result == "статистика":
            self.switch_to_stats()
        elif result == "банк":
            self.current_screen = self.bank_screen
        elif result == "донат":  # Обработка кнопки доната
            self.current_screen = self.donate_screen
        elif result == "resize":
            pass  # Уже обработано в toggle_fullscreen
        elif result == "quit":
            self.running = False
        elif isinstance(result, dict):  # Обработка покупок
            self.handle_purchase(result)

    def run(self):
        last_check_date = datetime.now().date()

        while self.running:
            # Проверяем наступление нового дня
            current_date = datetime.now().date()
            if current_date != last_check_date:
                self.calculate_daily_interest()
                last_check_date = current_date

            self.handle_events()

            # Отрисовка
            self.screen.fill((30, 30, 50))
            if self.current_screen:
                self.current_screen.draw()

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run()