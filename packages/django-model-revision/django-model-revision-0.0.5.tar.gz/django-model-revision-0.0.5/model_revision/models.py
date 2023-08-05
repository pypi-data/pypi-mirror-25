import json
from decimal import Decimal
from itertools import groupby

import datetime
import iso8601
import time
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _


class NOT_PROVIDED:
    pass


def get_field_data(instance):
    data = {}
    for field in instance._meta.get_fields():
        try:
            if not field.is_relation and field.serialize:
                value = field.value_from_object(instance)
                try:
                    # See if value can be serialized by standard JSON encoder
                    json.dumps(value)
                except:
                    # Try encoding this value with DjangoJSONEncoder, but don't double encode
                    value = json.loads(json.dumps(value, cls=DjangoJSONEncoder))
                data[field.get_attname()] = value
        except:
            # exclude this field if an exception is thrown
            pass
    return data


class RevisionQuerySet(models.QuerySet):

    def get_historical_values(self, field, current_value=NOT_PROVIDED, asc=True, include_dates=False):
        """
        Computes the historical values for the specified field over this QuerySet.
        Consecutive identical values are removed from the history, i.e.: [1,2,2,3] is turned into [1,2,3].
        The latest revision's field value is excluded from the list of historical values if it is equivalent to 
        the current field value.
        :param field: The name of the field for which to compute the values
        :param current_value: Used to determine whether or not to include the value of the latest revision. 
        If current_value is provided and is equal to the value of the latest revision, the latest revision is omitted.
        :param asc: If True results are ordered from earliest revision to latest.
        :param include_dates: Set to True to return a list of tuples of the form (revision_date_time, value)
        :return: List of values or list of tuples, depending on the value of include_dates.
        """
        qs = self.order_by('created_at')
        values = []
        for revision in qs:
            value = revision.get_data().get(field, None)
            if include_dates:
                values.append((revision.created_at, value))
            else:
                values.append(value)

        # Group consecutive values: [1,1,2,2,1,1] -> [1,2,1]
        if include_dates:
            grouped_values = []
            for k, g in groupby(values, key=lambda x: x[1]):
                grouped_values.append((list(g)[-1][0], k))
        else:
            grouped_values = [k for k, g in groupby(values)]

        # Pop off latest value if it's identical to the current value
        if current_value != NOT_PROVIDED and len(grouped_values) > 0:
            value = grouped_values[-1][1] if include_dates else grouped_values[-1]
            if value == current_value:
                grouped_values = grouped_values[:-1]

        if asc:
            return grouped_values
        else:
            return list(reversed(grouped_values))


class RevisionManager(models.Manager):

    def create_from_instance(self, instance):
        revision = Revision(
            content_object=instance,
            data=get_field_data(instance),
        )
        revision.save()
        return revision

    def get_for_instance(self, instance):
        return self.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk
        )


class Revision(models.Model):
    objects = RevisionManager.from_queryset(RevisionQuerySet)()
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    data = JSONField(db_index=True, null=False, default=dict)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_data(self):
        revision_data = {}
        for key, value in self.data.items():
            try:
                field = self.content_object._meta.get_field(key)
                field_type = type(field)
                if field_type in (models.DateField, models.DateTimeField):
                    dt_value = iso8601.parse_date(value)
                    if field_type == models.DateField:
                        revision_data[key] = dt_value.date()
                    else:
                        revision_data[key] = dt_value
                elif field_type == models.TimeField:
                    try:
                        st = time.strptime(value, '%H:%M:%S')
                        t = datetime.time(hour=st.tm_hour, minute=st.tm_min, second=st.tm_sec)
                    except Exception as e:
                        t = None
                    revision_data[key] = t
                elif field_type == models.DecimalField:
                    revision_data[key] = Decimal(value)
                else:
                    revision_data[key] = value
            except Exception as e:
                revision_data[key] = value
        return revision_data

    def __str__(self):
        return ugettext('Revision for {} from {}'.format(
            self.content_object,
            self.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        )

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Revision')
        verbose_name_plural = _('Revisions')
