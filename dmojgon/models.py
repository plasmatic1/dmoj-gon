from django.db import models
from django.contrib.postgres.fields import ArrayField


class Test(models.Model):
    GENERATOR = 'G'
    HAND_WRITTEN = 'H'
    type = models.CharField(max_length=1, choices=(
        (GENERATOR, 'Generator'),
        (HAND_WRITTEN, 'Handwritten')
    ), default=GENERATOR)

    data = models.CharField(max_length=256)


class Batch(models.Model):
    points = models.IntegerField()
    tests = ArrayField(models.ForeignKey(to='Test', on_delete=models.CASCADE))


class Problem(models.Model):
    CASE_FILE = 0
    MISC_FILE = 1
    _FILE_TYPES = {CASE_FILE, MISC_FILE}

    dir = models.CharField(max_length=64)
    batches = ArrayField(Batch)

    init_yml_extra = models.CharField(max_length=1024)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()

    def list_files(self):
        pass

    def generate(self):
        pass

    def upload_file(self, file, file_type):  # what is file?????
        if file_type not in self._FILE_TYPES:
            raise ValueError('Invalid file type')
        pass

    def package(self):
        pass
