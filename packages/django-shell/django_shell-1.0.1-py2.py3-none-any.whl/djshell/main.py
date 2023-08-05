# -*- coding: utf-8 -*-

from django.contrib.auth.models import User


def reset_pwd(password='1q2w3e4r5t6y7u8i9o0p', username='admin'):
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
