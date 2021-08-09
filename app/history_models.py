from django.db import models
from dmojgon.settings import EPS


class ValidatorResult(models.Model):
    validator_src = models.CharField(max_length=65536)  # Max DMOJ TL
    verdicts = models.CharField(max_length=2048)  # JSON list
    ok = models.BooleanField()
    timestamp = models.DateTimeField()


class CaseResult(models.Model):
    input = models.CharField(max_length=512)
    output = models.CharField(max_length=512)
    e_time = models.FloatField()  # s
    e_memory = models.IntegerField()  # kib
    verdict = models.CharField(max_length=2)
    feedback = models.CharField(max_length=128)

    p_batch = models.ForeignKey(to='BatchResult', on_delete=models.CASCADE)


class BatchResult(models.Model):
    index = models.IntegerField()
    points = models.FloatField()
    max_points = models.FloatField()

    p_sinvocation = models.ForeignKey(to='SingleInvocationResult', on_delete=models.CASCADE)

    def tests(self):
        return CaseResult.objects.filter(p_batch_id=self.id)


class SingleInvocationResult(models.Model):
    src_name = models.CharField(max_length=64)
    src = models.CharField(max_length=65536)

    verdict = models.CharField(max_length=2)
    exp_verdict = models.CharField(max_length=2)
    points = models.FloatField()
    max_points = models.FloatField()

    p_invocation = models.ForeignKey(to='InvocationResult', on_delete=models.CASCADE)

    def batches(self):
        return BatchResult.objects.filter(p_sinvocation_id=self.id)

    def ok(self):
        return self.verdict == self.exp_verdict and abs(self.points - self.max_points) <= EPS


class InvocationResult(models.Model):
    timestamp = models.DateTimeField()
    p_problem = models.ForeignKey(to='Problem', on_delete=models.CASCADE)

    def invocations(self):
        return SingleInvocationResult.objects.filter(p_invocation_id=self.id)

    def ok(self):
        return all(map(lambda res: res.ok(), self.invocations().all()))
