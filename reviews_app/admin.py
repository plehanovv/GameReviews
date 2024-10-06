from django.contrib import admin, messages
from .models import GameReview, Category


admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Обзоры на игры'


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title', )}

    @admin.display(description='Кол-во символов в обзоре', ordering='content')
    def brief_info(self, review: GameReview):
        return f'{len(review.content)} символов'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=GameReview.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записи')

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=GameReview.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} записи', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')




