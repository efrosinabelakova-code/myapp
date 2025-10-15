# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
import os

from screens.welcome import WelcomeScreen
from screens.auth import AuthScreen
from screens.mainscreen import MainScreen
from screens.grammar import GrammarScreen, GrammarContentScreen
from screens.dictionary import DictionaryScreen
from screens.exercises import ExerciseScreen
from screens.profile import ProfileScreen

from database import DatabaseManager


class LanguageApp(App):
    db_manager = ObjectProperty()
    current_user = ObjectProperty(None, allownone=True)
    current_grammar_module = ObjectProperty(None, allownone=True)

    def build(self):
        # Регистрируем корейские шрифты
        self.register_korean_fonts()

        self.db_manager = DatabaseManager()
        self.current_user = None
        self.current_grammar_module = None

        sm = ScreenManager()

        # Основные экраны
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(AuthScreen(name='auth'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(GrammarScreen(name='grammar'))
        sm.add_widget(DictionaryScreen(name='dictionary'))
        sm.add_widget(ExerciseScreen(name='exercises'))
        sm.add_widget(ProfileScreen(name='profile'))

        return sm

    def register_korean_fonts(self):
        """Регистрирует корейские шрифты для использования в приложении"""
        try:
            # Проверяем существование файлов шрифтов
            font_paths = {
                'NotoSansKR': {
                    'regular': 'fonts/NotoSansKR-Bold.ttf',
                    'bold': 'fonts/NotoSansKR-Bold.ttf'
                }
            }

            # Регистрируем шрифт
            LabelBase.register(
                name='NotoSansKR',
                fn_regular=font_paths['NotoSansKR']['regular'],
                fn_bold=font_paths['NotoSansKR']['bold']
            )
            print("Корейские шрифты успешно зарегистрированы")

        except Exception as e:
            print(f"Ошибка при загрузке корейских шрифтов: {e}")
            print("Используются системные шрифты")

    def login_user(self, username, password):
        print(f"Попытка входа: {username}")
        user = self.db_manager.authenticate_user(username, password)
        if user:
            print(f"Успешный вход: {user['username']}")
            self.current_user = user
            return True
        print("Ошибка входа: неверные данные")
        return False

    def register_user(self, username, password, email=None):
        print(f"Попытка регистрации: {username}")
        user_id = self.db_manager.register_user(username, password, email)
        if user_id:
            print(f"Успешная регистрация: ID {user_id}")
            self.current_user = {
                'id': user_id,
                'username': username,
                'level': 'beginner',
                'points': 0
            }
            return True
        print("Ошибка регистрации: пользователь уже существует")
        return False

    def get_user_stats(self):
        """Получить статистику пользователя"""
        if not self.current_user:
            return None

        user_id = self.current_user['id']

        # Получаем словарь пользователя
        vocabulary = self.db_manager.get_user_vocabulary(user_id)
        vocabulary_count = len(vocabulary)

        # Получаем прогресс тестов
        progress = self.db_manager.get_user_progress(user_id)
        test_count = len(progress)

        return {
            'level': self.current_user.get('level', 'beginner'),
            'points': self.current_user.get('points', 0),
            'vocabulary_count': vocabulary_count,
            'test_count': test_count
        }


if __name__ == '__main__':
    LanguageApp().run()