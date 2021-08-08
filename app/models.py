from django.db import models
from django.contrib.auth import models as auth_models  # I would call this goth_models but that would be too sus
from dmojgon.settings import DATA_DIR
from . import history_models
import os


class UploadedFile(models.Model):
    file = models.FileField(upload_to=DATA_DIR)
    timestamp = models.DateTimeField()
    p_problem = models.ForeignKey(to='Problem', on_delete=models.CASCADE)


class Test(models.Model):
    GENERATOR = 'G'
    HAND_WRITTEN = 'H'
    type = models.CharField(max_length=1, choices=(
        (GENERATOR, 'Generator'),
        (HAND_WRITTEN, 'Handwritten')
    ), default=GENERATOR)
    data = models.CharField(max_length=256)

    # Cur I/O
    cur_input = models.FileField(upload_to=DATA_DIR, null=True)
    cur_output = models.FileField(upload_to=DATA_DIR, null=True)

    p_batch = models.ForeignKey(to='Batch', on_delete=models.CASCADE)


class Batch(models.Model):
    points = models.IntegerField()
    p_problem = models.ForeignKey(to='Problem', on_delete=models.CASCADE)  # I got 99 problems and this is one of them

    def tests(self):
        return Test.objects.filter(p_batch_id=self.id)


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

    # Files
    validator = models.FileField(upload_to=DATA_DIR, null=True)
    main_solution = models.FileField(upload_to=DATA_DIR, null=True)

    def batches(self):
        return Batch.objects.filter(p_problem_id=self.id)

    def aux_files(self):
        return UploadedFile.objects.filter(p_problem_id=self.id)

    def invocation_results(self):
        return history_models.InvocationResult.objects.filter(p_problem_id=self.id)

    def validator_results(self):
        return history_models.ValidatorResult.objects.filter(p_problem_id=self.id)
