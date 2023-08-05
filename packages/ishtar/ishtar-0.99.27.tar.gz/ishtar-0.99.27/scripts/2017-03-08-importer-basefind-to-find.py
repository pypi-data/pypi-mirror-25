from ishtar_common import models


def convert_field(field_name):
    if field_name.startswith('find__'):
        field_name = field_name[len('find__'):]
    else:
        field_name = "base_finds__" + field_name
    return field_name


def refac_types(types):
    find_model, created = models.ImporterModel.objects.get_or_create(
        klass='archaeological_finds.models_finds.Find',
        defaults={'name': 'Find'}
    )
    for tpe in types:
        for col in tpe.columns.all():
            for field in col.duplicate_fields.all():
                new_field_name = convert_field(field.field_name)
                field.field_name = new_field_name
                field.save()
            for field in col.targets.all():
                new_field_name = convert_field(field.target)
                field.target = new_field_name
                field.save()
        tpe.associated_models = find_model
        tpe.save()


types = list(models.ImporterType.objects.filter(
    associated_models=models.ImporterModel.objects.get(
        klass='archaeological_finds.models.BaseFind')).all())

refac_types(types)
