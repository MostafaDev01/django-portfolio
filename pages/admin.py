
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    ContactMessage,
    Education,
    Experience,
    Faq,
    Hero,
    Links,
    Profile,
    Project,
    Service,
    Skill,
    SocialLinks,
    Testimonial,
)


# Profile
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = (
        "name",
        "job_title",
        "email",
        "phone",
        "is_active",
        "updated_at",
    )

    list_filter = ("is_active",)

    search_fields = (
        "name",
        "job_title",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# Skills
class SkillInline(TabularInline):
    model = Skill
    extra = 1
    fields = (
        "name",
        "level",
        "is_featured",
        "description",
    )


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = (
        "name",
        "level",
        "is_featured",
    )

    list_filter = ("is_featured",)

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "level",
        "is_featured",
    )


# Services
@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = (
        "title",
        "is_featured",
        "created_at",
    )

    list_filter = ("is_featured",)

    search_fields = (
        "title",
        "description",
    )

    list_editable = ("is_featured",)

    readonly_fields = ("created_at",)


# Projects
@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        "title",
        "client",
        "industry",
        "is_featured",
        "start_date",
        "end_date",
    )

    list_filter = (
        "is_featured",
        "industry",
        "odoo_modules",
        "skills",
    )

    search_fields = (
        "title",
        "client",
        "industry",
        "short_description",
        "description",
    )

    filter_horizontal = ("skills",)

    list_editable = ("is_featured",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "slug",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "client",
                    "industry",
                    "short_description",
                    "description",
                    "image",
                ),
            },
        ),
        (
            "Project Details",
            {
                "fields": (
                    "challenge",
                    "solution",
                    "results",
                    "links",
                ),
            },
        ),
        (
            "Technologies",
            {
                "fields": (
                    "skills",
                    "odoo_modules",
                ),
            },
        ),
        (
            "Timeline",
            {
                "fields": (
                    "start_date",
                    "end_date",
                ),
            },
        ),
        (
            "Settings",
            {
                "fields": ("is_featured",),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "slug",
                ),
            },
        ),
    )


# Experience
@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = (
        "job_title",
        "company",
        "location",
        "start_date",
        "end_date",
        "current",
    )

    list_filter = (
        "current",
        "company",
        "start_date",
    )

    search_fields = (
        "job_title",
        "company",
        "location",
        "description",
    )


# Education
@admin.register(Education)
class EducationAdmin(ModelAdmin):
    list_display = (
        "degree",
        "institution",
        "field",
        "start_date",
        "end_date",
    )

    list_filter = (
        "institution",
        "field",
    )

    search_fields = (
        "degree",
        "institution",
        "field",
        "description",
    )


# Testimonials
@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = (
        "name",
        "position",
        "company",
        "rating",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_featured",
        "company",
    )

    search_fields = (
        "name",
        "position",
        "company",
        "content",
    )

    list_editable = (
        "rating",
        "is_featured",
    )

    readonly_fields = ("created_at",)


# Contact messages
@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

    list_editable = ("is_read",)

    readonly_fields = ("created_at",)

    actions = (
        "mark_as_read",
        "mark_as_unread",
    )

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


# FAQs
@admin.register(Faq)
class FaqAdmin(ModelAdmin):
    list_display = (
        "question",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "is_featured",
        "created_at",
    )

    search_fields = (
        "question",
        "answer",
    )

    list_editable = ("is_featured",)

    readonly_fields = ("created_at",)


# General links
@admin.register(Links)
class LinksAdmin(ModelAdmin):
    list_display = (
        "name",
        "url",
    )

    search_fields = (
        "name",
        "url",
    )


# Hero section
@admin.register(Hero)
class HeroAdmin(ModelAdmin):
    list_display = (
        "title",
        "subtitle",
        "image",
        "years_of_experience",
        "happy_clients",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# Social links
@admin.register(SocialLinks)
class SocialLinksAdmin(ModelAdmin):
    list_display = (
        "name",
        "url",
    )

    search_fields = (
        "name",
        "url",
    )