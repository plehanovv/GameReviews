import random
from django import template
import reviews_app.views as views
from reviews_app.models import Category, TagReview

register = template.Library()


@register.inclusion_tag('review_app/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats}


@register.inclusion_tag('review_app/list_tags.html')
def show_all_tags():
    return {'tags': TagReview.objects.all()}