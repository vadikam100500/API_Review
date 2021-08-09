from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()

class Review(models.Model):
    title_id = models.ForeignKey(
        "Title", on_delete=models.CASCADE,
        related_name="reviews", verbose_name='Произведениe'
    )
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                     blank=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_name_reviews'
            )
        ]    
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Коментарий')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True,  blank=True)

    class Meta:
        ordering = ('-pub_date',)    

    def __str__(self):
        return self.text            