from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

def startup():
    try:
        User.objects.create_superuser("admin","admin@adminadminadmin.com","123admin")
    except IntegrityError:
        pass
    groupD, created = Group.objects.get_or_create(name='doctor')
    if (created):
        groupD.permissions.clear()
        permission = Permission.objects.get(codename='add_disease')
        groupD.permissions.add(permission)
    #adding users
    try:
        user = User.objects.create_user(
            "doc1", "doc@adminadminadmin.com", "nottoocomplex",first_name="doc1",last_name="Einz")
        user.groups.add(groupD)
        user.save()
    except IntegrityError:
        pass
    try:
        user = User.objects.create_user(
            "doc2", "doc2@adminadminadmin.com", "nottoocomplex",first_name="doc2",last_name="Mark")
        user.groups.add(groupD)
        user.save()
    except IntegrityError:
        pass
    