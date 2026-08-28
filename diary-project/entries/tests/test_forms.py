import pytest
from django.contrib.auth import get_user_model
from ..forms import EntryForm

User = get_user_model()


@pytest.mark.django_db
class TestEntryForm:
    """Тесты для формы EntryForm"""

    def test_valid_form(self):
        """Тест валидной формы"""
        data = {
            'title': 'Тестовый заголовок',
            'content': 'Тестовое содержание'
        }
        form = EntryForm(data=data)
        assert form.is_valid()

    def test_invalid_form_empty_title(self):
        """Тест формы с пустым заголовком"""
        data = {
            'title': '',
            'content': 'Тестовое содержание'
        }
        form = EntryForm(data=data)
        assert not form.is_valid()
        assert 'title' in form.errors

    def test_invalid_form_empty_content(self):
        """Тест формы с пустым содержанием"""
        data = {
            'title': 'Тестовый заголовок',
            'content': ''
        }
        form = EntryForm(data=data)
        assert not form.is_valid()
        assert 'content' in form.errors
