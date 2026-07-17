from django.db import models

class Setting(models.Model):
    appname = models.CharField(max_length=100)
    appeditor = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    version = models.CharField(max_length=10, null=True)
    COLORS = [
        ('bg-gradient-primary','bg-gradient-primary'),
        ('bg-gradient-info','bg-gradient-info'),
        ('bg-gradient-success','bg-gradient-success'),
        ('bg-gradient-danger','bg-gradient-danger'),
        ('bg-gradient-warning','bg-gradient-warning'),
        ('bg-gradient-secondary','bg-gradient-secondary'),
        ('bg-gradient-dark','bg-gradient-dark')
    ]
    theme = models.CharField(max_length=200, null=True, choices=COLORS)
    CT = [
        ('text-primary','text-primary'),
        ('text-info','text-info'),
        ('text-success','text-success'),
        ('text-danger','text-danger'),
        ('text-secondary','text-secondary'),
        ('text-dark','text-dark'),
        ('text-light', 'text-light')
    ]
    text_color = models.CharField(max_length=20, null=True, choices=CT)
    logo = models.ImageField(upload_to="media", null=True, blank=True)
    width_logo = models.CharField(max_length=3, null=True)
    height_logo = models.TextField(max_length=3, null=True)

    def __str__(self):
        return self.appname
