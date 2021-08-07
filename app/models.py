from django.db import models
from django.contrib.auth import models as auth_models  # I would call this goth_models but that would be too sus
import os


class Test(models.Model):
    GENERATOR = 'G'
    HAND_WRITTEN = 'H'
    type = models.CharField(max_length=1, choices=(
        (GENERATOR, 'Generator'),
        (HAND_WRITTEN, 'Handwritten')
    ), default=GENERATOR)
    data = models.CharField(max_length=256)
    p_batch = models.ForeignKey(to='Batch', on_delete=models.CASCADE)


class Batch(models.Model):
    points = models.IntegerField()
    p_problem = models.ForeignKey(to='Problem', on_delete=models.CASCADE)  # I got 99 problems and this is one of them


class Problem(models.Model):
    CASE_FILE = 0
    MISC_FILE = 1
    _FILE_TYPES = {CASE_FILE, MISC_FILE}

    dir = models.FilePathField(path=os.getcwd(), allow_files=False, allow_folders=True, max_length=64)

    init_yml_extra = models.CharField(max_length=1024)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()

    # Utils and security stuff
    last_modified = models.DateTimeField()
    owners = models.ManyToManyField(auth_models.User)

    # Validation stuff
    validator_src = models.FilePathField(path=os.getcwd(), recursive=True, max_length=64, null=True)  # Can be null, in which case, yes

    def list_files(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError

    def upload_file(self, file, file_type):  # what is file?????
        if file_type not in self._FILE_TYPES:
            raise ValueError('Invalid file type')
        raise NotImplementedError

    def package(self):
        raise NotImplementedError
