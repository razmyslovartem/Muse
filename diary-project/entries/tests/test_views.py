import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Entry

User = get_user_model()


@pytest.mark.django_db
class TestEntryViews:
    """Тесты для представлений записей"""

    def test_list_view_requires_login(self, client):
        """Тест: список записей требует авторизации"""
        response = client.get(reverse('entries:list'))
        assert response.status_code == 302

    def test_list_view_authenticated(self, client):
        """Тест: авторизованный пользователь видит свои записи"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')

        Entry.objects.create(user=user, title='Запись 1', content='Content 1')
        Entry.objects.create(user=user, title='Запись 2', content='Content 2')

        response = client.get(reverse('entries:list'))
        assert response.status_code == 200
        assert len(response.context['entries']) == 2

    def test_create_view_authenticated(self, client):
        """Тест: создание записи авторизованным пользователем"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')

        data = {
            'title': 'Новая запись',
            'content': 'Содержание новой записи'
        }
        response = client.post(reverse('entries:create'), data)
        assert response.status_code == 302
        assert Entry.objects.count() == 1
        assert Entry.objects.first().title == 'Новая запись'

    def test_update_view_authenticated(self, client):
        """Тест: редактирование записи"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')

        entry = Entry.objects.create(user=user, title='Старая запись', content='Old content')

        data = {
            'title': 'Обновленная запись',
            'content': 'Новое содержание'
        }
        response = client.post(reverse('entries:update', kwargs={'pk': entry.pk}), data)
        assert response.status_code == 302
        entry.refresh_from_db()
        assert entry.title == 'Обновленная запись'

    def test_delete_view_authenticated(self, client):
        """Тест: удаление записи"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')

        entry = Entry.objects.create(user=user, title='Удаляемая запись', content='Content')

        response = client.post(reverse('entries:delete', kwargs={'pk': entry.pk}))
        assert response.status_code == 302
        assert Entry.objects.count() == 0

    def test_search_view(self, client):
        """Тест: поиск по записям"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')

        Entry.objects.create(user=user, title='Важная задача', content='Срочно сделать')
        Entry.objects.create(user=user, title='Обычная заметка', content='Не срочно')

        response = client.get(reverse('entries:list'), {'q': 'важная'})
        assert response.status_code == 200
        assert len(response.context['entries']) == 1
        assert response.context['entries'][0].title == 'Важная задача'
