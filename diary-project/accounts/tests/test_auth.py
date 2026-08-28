import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestAuth:
    """Тесты для аутентификации"""

    def test_register_view(self, client):
        """Тест: регистрация пользователя"""
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        response = client.post(reverse('accounts:register'), data)
        assert response.status_code == 302
        assert User.objects.count() == 1

    def test_login_view(self, client):
        """Тест: вход в систему"""
        User.objects.create_user(username='testuser', password='testpass123')

        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = client.post(reverse('accounts:login'), data)
        assert response.status_code == 302
        assert '_auth_user_id' in client.session

    def test_logout_view(self, client):
        """Тест: выход из системы"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        client.login(username='testuser', password='testpass123')

        response = client.post(reverse('accounts:logout'))
        assert response.status_code == 302
        assert '_auth_user_id' not in client.session