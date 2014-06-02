from django.db import models
from django.contrib.auth.models import User


class BaseManager(models.Manager):
    def all(self):
        return super(BaseManager, self).all().order_by("-pk")

    def active(self):
        return self.all().filter(deleted=False)

class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True

class Profile(BaseModel):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u"%s" % self.user

class Paste(BaseModel):
    owner = models.ForeignKey(Profile, null=True, blank=True)

    name = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField(default="", blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField()

    def __unicode__(self):
        return u"#%s %s" % (self.pk, self.name)

    def save(self, *args, **kwargs):
        if not self.owner:
            self.private = False
        return super(Paste, self).save(*args, **kwargs)
