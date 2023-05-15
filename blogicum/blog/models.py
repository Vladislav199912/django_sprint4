from django.db import models
from django.contrib.auth import get_user_model


class BaseMode(models.Model):
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text=(
                                           'Снимите галочку, чтобы'
                                           ' скрыть публикацию.')
                                       )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Category(BaseMode):
    helper = ''
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(max_length=64, unique=True,
                            verbose_name='Идентификатор',
                            help_text=(
                                'Идентификатор страницы для URL;'
                                ' разрешены символы латиницы, цифры,'
                                ' дефис и подчёркивание.')
                            )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseMode):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места',)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


User = get_user_model()


class Post(BaseMode):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text=(
                                        'Если установить дату и время'
                                        ' в будущем — можно делать'
                                        ' отложенные публикации.')
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации')
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='Местоположение')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория')
    image = models.ImageField(upload_to='posts_images',
                              blank=True,
                              verbose_name='Фото')

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comment.count()


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    post = models.ForeignKey(
        Post,
        verbose_name='Публикация',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')

    class Meta:
        ordering = ('created_at',)
        default_related_name = 'comment'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
