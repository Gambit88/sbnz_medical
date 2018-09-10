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
        permission = Permission.objects.get(codename='change_diagnosis')
        groupD.permissions.add(permission)
        permission = Permission.objects.get(codename='run_rules')
        groupD.permissions.add(permission)
    groupE, created = Group.objects.get_or_create(name='expert')
    if (created):
        groupE.permissions.clear()
        permission = Permission.objects.get(codename='change_disease')
        groupE.permissions.add(permission)
        permission = Permission.objects.get(codename='change_syndrome')
        groupE.permissions.add(permission)
        permission = Permission.objects.get(codename='change_medicine')
        groupE.permissions.add(permission)
        permission = Permission.objects.get(codename='change_ingredient')
        groupE.permissions.add(permission)
        permission = Permission.objects.get(codename='manage_rules')
        groupE.permissions.add(permission)
        permission = Permission.objects.get(codename='change_patient')
        groupE.permissions.add(permission)
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
    try:
        user = User.objects.create_user(
            "exp1", "exp1@adminadminadmin.com", "nottoocomplex",first_name="exp1",last_name="Markovic")
        user.groups.add(groupE)
        user.save()
    except IntegrityError:
        pass


startup()