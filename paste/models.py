from django.db import models


class BaseManager(models.Manager):
    def active(self):
        return self.filter(deleted=False)

class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True


class Paste(BaseModel):
    name = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField(default="", blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s %s" % (self.pk, self.name)
