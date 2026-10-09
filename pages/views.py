from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import (
    Hero,
    Profile,
    SocialLinks,
    Skill,
    Service,
    Project,
    Experience,
    Education,
    Testimonial,
    Faq,
    ContactMessage,
)
from .forms import ContactForm


def get_home_context(form=None):
    """
    Builds the context dictionary for the homepage index view.
    Reused by ContactCreateView when form validation fails.
    """
    hero = Hero.objects.first()
    skills = Skill.objects.exclude(is_featured=False)
    services = Service.objects.exclude(is_featured=False)
    projects = (
        Project.objects.exclude(is_featured=False)
        .prefetch_related("skills")
        .select_related("links")
        .order_by("-created_at")[:6]
    )
    experiences = Experience.objects.all()
    education = Education.objects.all()
    testimonials = Testimonial.objects.exclude(is_featured=False)
    faqs = Faq.objects.exclude(is_featured=False)
    industries = (
        Project.objects.exclude(industry__isnull=True)
        .exclude(industry="")
        .exclude(is_featured=False)
        .values_list("industry", flat=True)
        .distinct()
    )

    return {
        "hero": hero,
        "skills": skills,
        "services": services,
        "projects": projects,
        "experiences": experiences,
        "education": education,
        "testimonials": testimonials,
        "faqs": faqs,
        "industries": industries,
        "form": form or ContactForm(),
    }


def index(request):
    return render(request, "index.html", get_home_context())


class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio-details.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "project"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("links")
            .prefetch_related("skills")
        )


class ContactCreateView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = "index.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Your enquiry has been sent successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error in submitting your enquiry. Please check the fields below.",
        )
        return self.render_to_response(get_home_context(form=form))


class ProjectListView(ListView):
    model = Project
    template_name = "portfolio.html"
    context_object_name = "projects"
    paginate_by = 6
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("skills")
            .select_related("links")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["industries"] = (
            Project.objects.exclude(industry__isnull=True)
            .exclude(industry="")
            .values_list("industry", flat=True)
            .distinct()
        )
        return context