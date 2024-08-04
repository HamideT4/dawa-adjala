from django.db import models
from django.utils.translation import gettext_lazy as _ 


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
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    @property
    def get_full_name(self):
        return f"{self.first_name}".capitalize() + " " + f"{self.last_name}".capitalize()

    class Meta:
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.get_full_name
    
    
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
    
class Newsletter(models.Model):
    email = models.EmailField(max_length=250)

    class Meta:
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.email
    
class Support(models.Model):
    fullname = models.CharField(_('Nom complet'),max_length=250)
    email = models.EmailField(_('Email'),max_length=250)
    phone = models.CharField(_("Numero de téléphone"), max_length=20)
    subject = models.CharField(_("Objet"), max_length=100)
    message = models.TextField(_('Message'))

    class Meta:
        verbose_name_plural = 'Supports'

    def __str__(self):
        return self.subject

class Faq(models.Model):
    question = models.TextField(_('Question'))
    answer = models.TextField(_('Reponse'))

    class Meta:
        verbose_name_plural = 'Faqs'

    def __str__(self):
        return self.question

class Testimonial(models.Model):
    fullname = models.CharField(_('Nom complet'), max_length=150)
    image = models.ImageField(_("Photo"), upload_to='Testimonials/')
    role = models.CharField(_('Fonction'), max_length=250)
    testimonial = models.TextField(_("Temoignage"))

    class Meta:
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.testimonial
    
