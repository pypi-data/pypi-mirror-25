from django.contrib.auth.models import Group, Permission

for group in Group.objects.all():
    if ':' not in group.name or u"rattaché" in group.name:
        continue
    permissions = []
    for perm in group.permissions.all():
        codenames = perm.codename.split('_')
        own_codename = codenames[0] + "_own_" + '_'.join(codenames[1:])
        if Permission.objects.filter(codename=own_codename).count():
            permissions.append(Permission.objects.get(codename=own_codename))
    if not permissions:
        print(u'No permission: ' + group.name)
        continue
    names = group.name.split(':')
    if Group.objects.filter(name__startswith=names[0] + u"rattaché",
                            name__endswith=names[1]).count():
        print(u'Already here: ' + group.name)
        continue
    name = names[0] + u"rattachés " + u":" + names[1]
    new_group = Group.objects.create(name=name)
    for perm in permissions:
        new_group.permissions.add(perm)
    print(u'New: ' + group.name)
