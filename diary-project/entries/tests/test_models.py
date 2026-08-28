import pytest
from django.contrib.auth import get_user_model
from ..models import Entry

User = get_user_model()


@pytest.mark.django_db
class TestEntryModel:

    def test_create_entry(self):
        """Тест создания записи"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        entry = Entry.objects.create(
            user=user,
            title='Тестовая запись',
            content='Тестовое содержание записи'
        )

        assert entry.title == 'Тестовая запись'
        assert entry.user == user
        assert str(entry) == 'Тестовая запись'

    def test_entry_ordering(self):
        """Тест сортировки записей"""
        user = User.objects.create_user(username='testuser', password='testpass123')

        entry1 = Entry.objects.create(
            user=user,
            title='Первая',
            content='Content 1'
        )

        import time
        time.sleep(0.1)

        entry2 = Entry.objects.create(
            user=user,
            title='Вторая',
            content='Content 2'
        )

        entries = Entry.objects.all()
        assert entries[0] == entry2
        assert entries[1] == entry1

    def test_entry_str_method(self):
        """Тест метода __str__"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        entry = Entry.objects.create(
            user=user,
            title='Моя запись',
            content='Содержание'
        )
        assert str(entry) == 'Моя запись'

    def test_entry_encryption(self):
        """Тест шифрования содержимого"""
        user = User.objects.create_user(username='testuser', password='testpass123')

        original_content = 'Секретное сообщение'
        entry = Entry.objects.create(
            user=user,
            title='Секретная запись',
            content=original_content
        )

        assert entry.content != original_content
        assert entry.is_encrypted == True

        assert entry.decrypt_content() == original_content
