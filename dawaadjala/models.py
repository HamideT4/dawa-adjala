from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='Service/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name
    
class Team(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='Team/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.first_name
    
    @property
    def get_full_name(self):
        return f"{self.first_name}".capitalize() + " " + f"{self.last_name}".capitalize()

class Image(models.Model):
    name = models.CharField(max_length=100, default="Activité")
    image = models.ImageField(upload_to='News/')

    def __str__(self):
        return self.name

class New(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    image = models.ManyToManyField(Image)

    class Meta:
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title
