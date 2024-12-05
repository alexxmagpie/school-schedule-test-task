import asyncio

from collections import OrderedDict

from adrf.serializers import ModelSerializer

from asgiref.sync import sync_to_async

from django.db import models

from rest_framework.fields import SkipField


class ADRFModelSerializer(ModelSerializer):
    async def ato_representation(self, instance):
        """
        Override defalult adrf.serializers.ModelSerializer
        to get field attribute in asyncronious way.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = await sync_to_async(field.get_attribute)(instance)
            except SkipField:
                continue

            check_for_none = (
                attribute.pk if isinstance(attribute, models.Model) else attribute
            )
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if asyncio.iscoroutinefunction(
                    getattr(field, "ato_representation", None)
                ):
                    repr = await field.ato_representation(attribute)
                else:
                    repr = field.to_representation(attribute)

                ret[field.field_name] = repr

        return ret
