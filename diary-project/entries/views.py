from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Entry
from .forms import EntryForm


def filter_entries_by_phrase(entries, phrase):
    """Фильтрует записи по фразе (регистронезависимо)"""
    phrase_lower = phrase.casefold()
    return [
        e for e in entries
        if phrase_lower in e.title.casefold()
           or phrase_lower in e.decrypt_content().casefold()
    ]


def filter_entries_by_words(entries, *words):
    """Фильтрует записи по словам"""
    if not words:
        return []
    result = []
    for entry in entries:
        content_lower = entry.decrypt_content().casefold()
        title_lower = entry.title.casefold()
        for word in words:
            word_lower = word.casefold()
            if len(word_lower) > 1:
                if word_lower in title_lower or word_lower in content_lower:
                    result.append(entry)
                    break
    return result


class EntryListView(LoginRequiredMixin, ListView):
    """Список записей с поиском"""
    model = Entry
    template_name = 'entries/list.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        queryset = Entry.objects.filter(user=self.request.user)
        query = self.request.GET.get('q', '').strip()

        if query:
            entries_list = list(queryset)

            filtered = filter_entries_by_phrase(entries_list, query)
            if filtered:
                return filtered

            return filter_entries_by_words(entries_list, *query.split())

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class EntryDetailView(LoginRequiredMixin, DetailView):
    """Детальный просмотр с расшифровкой"""
    model = Entry
    template_name = 'entries/detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['decrypted_content'] = self.object.decrypt_content()
        return context


class EntryCreateView(LoginRequiredMixin, CreateView):
    """Создание записи"""
    model = Entry
    form_class = EntryForm
    template_name = 'entries/form.html'
    success_url = reverse_lazy('entries:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование записи с расшифровкой"""
    model = Entry
    form_class = EntryForm
    template_name = 'entries/form.html'
    success_url = reverse_lazy('entries:list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def get_initial(self):
        """Подставляем расшифрованное содержимое в форму"""
        initial = super().get_initial()
        entry = self.get_object()
        initial['content'] = entry.decrypt_content()
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена!')
        return super().form_valid(form)


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление записи с расшифровкой"""
    model = Entry
    template_name = 'entries/confirm_delete.html'
    success_url = reverse_lazy('entries:list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['decrypted_content'] = self.object.decrypt_content()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена!')
        return super().delete(request, *args, **kwargs)
