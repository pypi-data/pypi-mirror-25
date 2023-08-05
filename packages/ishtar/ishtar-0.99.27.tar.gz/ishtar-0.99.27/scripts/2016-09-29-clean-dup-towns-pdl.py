from ishtar_common.models import Town


dup_nb = 0
pdl = []
DPTS = ('44', '49', '53', '72', '85')

for dpt in DPTS:
    for town in Town.objects.filter(numero_insee__startswith=dpt):
        pdl.append(town.pk)
        for dup in Town.objects.filter(name=town.name).exclude(pk=town.pk):
            not_dup = False
            for d in DPTS:
                if dup.numero_insee.startswith(d):
                    not_dup = True
            if not_dup:
                continue
            for item in dup.file_main.all():
                item.main_town = town
                p = item.save()
            for item in dup.parcels.all():
                item.main_town = town
                p = item.save()
            for item in dup.file.all():
                item.towns.remove(dup)
                item.towns.add(town)
            for item in dup.operations.all():
                item.towns.remove(dup)
                item.towns.add(town)
            dup_nb += 1
            dup.delete()


print("{} items cleaned".format(dup_nb))

strange = []
for town in Town.objects.exclude(pk__in=pdl):
    if (town.file_main.count() or town.parcels.count() or town.file.count() or
            town.operations.count()):
        strange.append((town, town.file_main.count(), town.parcels.count(),
                        town.file.count(), town.operations.count()))
        continue
    town.delete()


print('* Problems with:')
for t in strange:
    print("{}: \n\t* {} ville principale dossier\n\t* {} parcelles\n\t* {} "
          "villes pour"
          " dossier\n\t* {} ville pour operation".format(t[0], t[1], t[2],
                                                         t[3], t[4]))
