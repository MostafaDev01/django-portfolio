from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
)
from django.db import models
from django.utils.text import slugify

class Hero(models.Model):
    title = models.CharField(
        max_length=200,
    )

    subtitle = models.CharField(
        max_length=200,
        blank=True,
    )

    image = models.ImageField(
        upload_to="hero/",
        blank=True,
        null=True,
    )

    years_of_experience = models.PositiveIntegerField()
    happy_clients = models.PositiveIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Hero"

    def __str__(self):
        return self.title


class Profile(models.Model):
    name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    bio = models.TextField()

    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    email = models.EmailField()
    phone = models.CharField(
        max_length=11,
        blank=True,
        validators=[MaxLengthValidator(11), MinLengthValidator(11)],
    )
    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(15)]
    )

    nationality = models.CharField(max_length=150)



    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.name





class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )


    level = models.PositiveIntegerField(  # progress
        default=80,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text="Skill level from 0 to 100.",
    )

    description = models.TextField(
        blank=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(
        max_length=150,
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# class OdooModule(models.Model):
#     name = models.CharField(
#         max_length=100,
#         unique=True,
#     )

#     version = models.CharField(
#         max_length=20,
#         default="Odoo 19",
#     )

#     description = models.TextField(
#         blank=True,
#     )

#     icon = models.CharField(
#         max_length=100,
#         blank=True,
#     )

#     def __str__(self):
#         return self.name


class Links(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    url = models.URLField(
        blank=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    slug = models.SlugField(max_length=150 , editable=False , blank=True)
    title = models.CharField(
        max_length=200,
    )

    client = models.CharField(
        max_length=150,
        blank=True,
    )

    industry = models.CharField(
        max_length=150,
    )

    short_description = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    challenge = models.TextField(
        blank=True,
    )

    solution = models.TextField(
        blank=True,
    )

    results = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="projects",
    )

    odoo_modules = models.CharField(max_length=100 , default="")

    links = models.OneToOneField(
        Links, on_delete=models.CASCADE, related_name="links", blank=True, null=True
    )

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True) or "project"
            slug = base_slug
            counter = 1
            qs = Project.objects.filter(slug=slug)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            while qs.exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                qs = Project.objects.filter(slug=slug)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
            self.slug = slug
        super().save(*args, **kwargs)





class Experience(models.Model):
    job_title = models.CharField(
        max_length=150,
    )

    company = models.CharField(
        max_length=150,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    current = models.BooleanField(
        default=False,
    )

    description = models.TextField()

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.job_title} - {self.company}"


class Education(models.Model):
    institution = models.CharField(
        max_length=200,
    )

    degree = models.CharField(
        max_length=150,
    )

    field = models.CharField(
        max_length=150,
        blank=True,
    )

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Testimonial(models.Model):
    name = models.CharField(
        max_length=150,
    )

    position = models.CharField(
        max_length=150,
        blank=True,
    )

    company = models.CharField(
        max_length=150,
        blank=True,
    )

    photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
    )

    content = models.TextField()

    rating = models.PositiveIntegerField(
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    is_featured = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=150,
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Faq(models.Model):
    question = models.CharField(
        max_length=200,
    )

    answer = models.TextField()

    is_featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question


class SocialLinks(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    url = models.URLField(
        blank=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = "Social media links"
        verbose_name_plural = "Social media links"

    def __str__(self):
        return self.name