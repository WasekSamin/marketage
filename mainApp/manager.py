from random import randint
from django.db import models
from django.db.models import Count

class RandomQustionManager(models.query.QuerySet):
    def random_qustion(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class GigRaningKindManager(models.query.QuerySet):
    def gig_ranked(self):
        pass