"""Serializers for query optimizations."""

from django.db import models
from rest_framework import serializers


class QueryOptimizingListSerializer(serializers.ListSerializer):
    """
    A list serializer for query optimizations for model serializers.

    The idea is to provide an easy way to utilize `select_related()` and
    `prefetch_related()`.

    There is no way to automatically determine the correct values for these
    QuerySet methods.

    This serializer makes it easy to do query optimizations in serialized
    lists, by allowing you to define the values for `select_related()` and
    `prefetch_related()` yourself as attributes on the child serializer as
    simple lists. This serializer will then take care of adding the
    optimizations to the query before it is executed.
    """

    def to_representation(self, data):
        """
        Custom data handling, to support query optimizations.

        This one is based on the similar method of the DRF ListSerializer,
        but adds support for query optimizations.

        Currently based on the method from version 3.6.4 of DRF.
        """
        # First, make sure we're having a ModelSerializer as the child.
        # Otherwise, things will probably blow up.
        assert isinstance(self.child, serializers.ModelSerializer), (
            'The QueryOptimizingListSerializer can only be used as list '
            ' serializer for model serializers.'
        )

        # Dealing with nested relationships, data can be a Manager,
        # so, first get a queryset from the Manager if needed
        iterable = data.all() if isinstance(data, models.Manager) else data

        # Add `select_related()` to the queryset if set on the
        # child serializer.
        if hasattr(self.child.Meta, 'select_related'):
            iterable = iterable.select_related(
                *self.child.Meta.select_related
            )

        # Add `prefetch_related()` to the queryset if set on the
        # child serializer.
        if hasattr(self.child.Meta, 'prefetch_related'):
            iterable = iterable.prefetch_related(
                *self.child.Meta.prefetch_related
            )

        return [
            self.child.to_representation(item) for item in iterable
        ]
