from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from cryptography.fernet import Fernet

User = get_user_model()


class ContentEncryptionError(Exception):
    """Ошибка при расшифровке контента."""
    pass


class Entry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Пользователь'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_encrypted = models.BooleanField(default=True, verbose_name='Зашифровано')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entries:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """Шифруем содержимое перед сохранением"""
        if self.content and self.is_encrypted:
            cipher = Fernet(settings.ENCRYPTION_KEY.encode())
            self.content = cipher.encrypt(self.content.encode()).decode()
        super().save(*args, **kwargs)

    def decrypt_content(self):
        """Расшифровывает содержимое записи"""
        if not self.is_encrypted:
            return self.content
        try:
            cipher = Fernet(settings.ENCRYPTION_KEY.encode())
            return cipher.decrypt(self.content.encode()).decode()
        except Exception as e:
            raise ContentEncryptionError(f"Ошибка расшифровки записи {self.id}") from e
