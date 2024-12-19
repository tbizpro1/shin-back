from django.db import models

class Enterprise(models.Model):
    # Primary Key
    enterprise_id = models.AutoField(primary_key=True)

    # Strings
    name = models.CharField(max_length=255)
    problem = models.TextField()
    solution = models.TextField()
    value_proposition = models.TextField()
    differential = models.TextField()
    competitors = models.TextField()
    product = models.CharField(max_length=255)
    description = models.TextField()
    mail = models.EmailField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(max_length=255, null=True, blank=True)
    name_foment = models.CharField(max_length=255, null=True, blank=True)
    programm = models.CharField(max_length=255, null=True, blank=True)
    file = models.ImageField(upload_to='enterprise_files/', null=True, blank=True)

    # Booleans
    invested = models.BooleanField(default=False)
    boosting = models.BooleanField(default=False)

    # Numbers
    value_invested = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    value_foment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)



    def __str__(self):
        return f"{self.name} - {self.value_proposition[:30]}..."

