# -*- coding: utf-8 -*-
import inspect

from django.core.management import BaseCommand
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType

from search import indexes


class Command(BaseCommand):
    help = "Builds elasticsearch index"

    def handle(self, *args, **options):
        es = Elasticsearch()

        def is_index(cls):
            for base_cls in cls.__bases__:
                if base_cls == DocType:
                    return True

        for cls in [
            c for n, c in inspect.getmembers(indexes, inspect.isclass)
            if is_index(c)
        ]:
            self.stdout.write(
                'Indexing index {index}'.format(index=cls.__name__)
            )
            es.indices.delete(index=cls()._index, ignore=[400, 404])
            cls.bulk_index()
