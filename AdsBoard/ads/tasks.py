from celery import shared_task
import datetime

from .models import Comment, Post
from accounts.models import CustomUser

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives


@shared_task
def email_notifying_new_comment(pk, created, usr_pk):
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
    instance = Comment.objects.get(pk=pk)
    if created:
        usr = CustomUser.objects.get(pk=usr_pk)
        html_content = render_to_string(
            'ads/subs_email.html',
            {
                'comment': instance,
                'usr': usr,
                'full_url': full_url,
                'created': created,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Новый комментарий к посту',
            body=f'Приветствуем, {usr.first_name} {usr.last_name}. Новый комментарий к: ' + instance.post_title,
            from_email='',
            to=[f'{usr.email}'],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()


@shared_task
def email_notifying_comment_approved(pk, created, usr_pk):
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
    instance = Comment.objects.get(pk=pk)
    if instance.approved:
        usr = CustomUser.objects.get(pk=usr_pk)
        html_content = render_to_string(
            'ads/subs_email.html',
            {
                'comment': instance,
                'usr': usr,
                'full_url': full_url,
                'created': created,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Подтверждение комментария',
            body=f'Здравствуйте, {usr.first_name} {usr.last_name}. Ваш комментарий к: ' + instance.post_title + ' одобрен!',
            from_email='',
            to=[f'{usr.email}'],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()


@shared_task
def week_email_sending():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])

    list_of_posts = Post.objects.filter(date_posted__range=(start_date, end_date))
    if len(list_of_posts) > 0:
        for u in CustomUser.objects.filter(need_mailing_news=True):
            html_content = render_to_string(
                'ads/subs_email_each_week.html',
                {
                    'news': list_of_posts,
                    'usr': u,
                    'full_url': full_url,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Здравствуйте, {u.first_name} {u.last_name}. За наделю появились новые статьи',
                body='',
                from_email='',
                to=[f'{u.email}'],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()
