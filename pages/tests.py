import os
import shutil
import tempfile
from pathlib import Path
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pages.models import (
    Hero,
    Profile,
    SocialLinks,
    Skill,
    Service,
    Project,
    Certification,
    Experience,
    Education,
    Testimonial,
    Faq,
    ContactMessage,
)
from pages.context_processors import portfolio_globals


class ModelTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            name="Jane Doe",
            job_title="Senior Consultant",
            bio="Experienced ERP specialist.",
            email="jane@example.com",
            location="Berlin, Germany",
            age=32,
            nationality="Egyptian",
        )

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "Jane Doe")

    def test_project_slug_generation_and_collisions(self):
        # 1. Standard title
        p1 = Project.objects.create(
            title="Supply Chain ERP",
            industry="Manufacturing",
            short_description="ERP overhaul",
            description="Detailed overhaul.",
        )
        self.assertEqual(p1.slug, "supply-chain-erp")

        # 2. Collision handling with incremental counter
        p2 = Project.objects.create(
            title="Supply Chain ERP",
            industry="Manufacturing",
            short_description="Another ERP overhaul",
            description="Detailed overhaul.",
        )
        self.assertEqual(p2.slug, "supply-chain-erp-1")

        p3 = Project.objects.create(
            title="Supply Chain ERP",
            industry="Manufacturing",
            short_description="Third ERP overhaul",
            description="Detailed overhaul.",
        )
        self.assertEqual(p3.slug, "supply-chain-erp-2")

        # 3. Unicode titles
        p_unicode = Project.objects.create(
            title="نظام إدارة الموارد المؤسسية",
            industry="Enterprise",
            short_description="وصف مختصر",
            description="تفاصيل كاملة.",
        )
        self.assertEqual(p_unicode.slug, "نظام-إدارة-الموارد-المؤسسية")

        # 4. Symbols-only title fallback
        p_symbols = Project.objects.create(
            title="!@#$$%^",
            industry="Tech",
            short_description="Symbols project",
            description="Testing fallback.",
        )
        self.assertTrue(p_symbols.slug.startswith("project"))

        # 5. Existing record preservation (slug should not mutate on title update if already set)
        original_slug = p1.slug
        p1.description = "Updated description text."
        p1.save()
        p1.refresh_from_db()
        self.assertEqual(p1.slug, original_slug)

    def test_hero_str(self):
        hero = Hero.objects.create(
            title="Welcome to My Portfolio",
            subtitle="Specialist",
            years_of_experience=5,
            happy_clients=25,
        )
        self.assertEqual(str(hero), "Welcome to My Portfolio")

    def test_service_and_skill_str(self):
        service = Service.objects.create(
            title="Process Automation",
            description="Automating workflows.",
            is_featured=True,
        )
        self.assertEqual(str(service), "Process Automation")

        skill = Skill.objects.create(
            name="Python & Django",
            level=90,
            is_featured=True,
        )
        self.assertEqual(str(skill), "Python & Django")

    def test_testimonial_and_faq_str(self):
        testimonial = Testimonial.objects.create(
            name="John Smith",
            position="Operations Manager",
            company="Tech Corp",
            content="Outstanding delivery.",
            is_featured=True,
        )
        self.assertEqual(str(testimonial), "John Smith")

        faq = Faq.objects.create(
            question="What are your consultation rates?",
            answer="Rates depend on project scope.",
            is_featured=True,
        )
        self.assertEqual(str(faq), "What are your consultation rates?")

    def test_contact_message_str(self):
        msg = ContactMessage.objects.create(
            name="Alice",
            email="alice@example.com",
            subject="Project Inquiry",
            message="Let us discuss a new project.",
        )
        self.assertEqual(str(msg), "Alice - Project Inquiry")


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.create(
            name="Jane Doe",
            job_title="Senior Consultant",
            bio="ERP specialist.",
            email="jane@example.com",
            location="Berlin, Germany",
            age=30,
            nationality="Egyptian",
        )
        self.hero = Hero.objects.create(
            title="Lead Functional Consultant",
            years_of_experience=7,
            happy_clients=40,
        )
        self.skill = Skill.objects.create(
            name="Odoo 19",
            level=90,
            is_featured=True,
        )
        self.project = Project.objects.create(
            title="Global Logistics Integration",
            industry="Logistics",
            short_description="Integrated logistics workflow.",
            description="End-to-end multi-currency setup.",
            is_featured=True,
        )
        self.project.skills.add(self.skill)

    def test_index_view_loads_successfully(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIn("hero", response.context)
        self.assertIn("projects", response.context)
        self.assertIn("industries", response.context)
        self.assertIn("Logistics", response.context["industries"])

    def test_project_list_view(self):
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio.html")
        self.assertIn("projects", response.context)
        self.assertIn("industries", response.context)
        self.assertIn("Logistics", response.context["industries"])

    def test_project_detail_view_success(self):
        response = self.client.get(reverse("detail", kwargs={"slug": self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio-details.html")
        self.assertEqual(response.context["project"].title, self.project.title)

    def test_project_detail_view_404(self):
        response = self.client.get(reverse("detail", kwargs={"slug": "non-existent-project"}))
        self.assertEqual(response.status_code, 404)

    def test_custom_404_template_used(self):
        response = self.client.get("/non-existent-page-url/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_contact_form_valid_submission(self):
        payload = {
            "name": "Jane Client",
            "email": "client@example.com",
            "subject": "New Project RFP",
            "message": "We need help migrating our workflows.",
        }
        response = self.client.post(reverse("contact"), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email="client@example.com").exists())
        messages = list(response.context["messages"])
        self.assertTrue(any("Your enquiry has been sent successfully!" in str(m) for m in messages))

    def test_contact_form_invalid_submission_retains_context(self):
        payload = {
            "name": "Jane Client",
            "email": "not-an-email",
            "subject": "Incomplete",
            "message": "",
        }
        response = self.client.post(reverse("contact"), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)


class TemplateSafetyTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_user_navbar_and_footer(self):
        Profile.objects.create(
            name="Consultant Name",
            job_title="Lead ERP Consultant",
            bio="Bio text",
            email="test@example.com",
            age=29,
            nationality="Egyptian",
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="sitename">Consultant Name</h1>')
        self.assertContains(response, '<strong>Consultant Name</strong>. All rights reserved.')

    def test_null_images_do_not_crash_page(self):
        Profile.objects.create(
            name="No Image Consultant",
            job_title="Consultant",
            bio="Bio text",
            email="noimage@example.com",
            profile_image=None,
            age=35,
            nationality="Egyptian",
        )
        Hero.objects.create(
            title="No Image Hero",
            image=None,
            years_of_experience=3,
            happy_clients=10,
        )
        Testimonial.objects.create(
            name="Client Without Photo",
            position="Director",
            company="Global Co",
            content="Great job!",
            photo=None,
            is_featured=True,
        )
        Project.objects.create(
            title="Project Without Image",
            industry="Finance",
            short_description="Finance project",
            description="Details",
            image=None,
            is_featured=True,
        )

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class MediaStorageAndUploadTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.client = Client()
        # 1x1 valid PNG bytes
        self.png_bytes = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00"
            b"\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82"
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_image_upload_url_generation_and_retrieval(self):
        with override_settings(MEDIA_ROOT=Path(self.temp_dir)):
            uploaded_file = SimpleUploadedFile(
                name="test_proj.png",
                content=self.png_bytes,
                content_type="image/png",
            )
            project = Project.objects.create(
                title="Upload Verification Project",
                industry="Retail",
                short_description="Upload short desc",
                description="Upload full desc",
                image=uploaded_file,
            )

            # 1. URL generation
            self.assertTrue(project.image.url.startswith("/media/projects/"))

            # 2. Filesystem existence
            saved_path = Path(project.image.path)
            self.assertTrue(saved_path.exists())
            self.assertEqual(saved_path.read_bytes(), self.png_bytes)

            # 3. HTTP retrieval via test client
            res = self.client.get(project.image.url)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(b"".join(res.streaming_content), self.png_bytes)

    def test_missing_physical_file_does_not_crash_views(self):
        with override_settings(MEDIA_ROOT=Path(self.temp_dir)):
            # Database references a file that does NOT exist on disk
            project = Project.objects.create(
                title="Missing File Project",
                industry="Logistics",
                short_description="Missing short desc",
                description="Missing full desc",
                image="projects/ghost_file.png",
                is_featured=True,
            )
            # Physical file is absent
            self.assertFalse(Path(project.image.path).exists())

            # Index page renders without FileNotFoundError
            res_home = self.client.get(reverse("home"))
            self.assertEqual(res_home.status_code, 200)

            # Archive page renders without error
            res_archive = self.client.get(reverse("projects"))
            self.assertEqual(res_archive.status_code, 200)

            # Detail page renders without error
            res_detail = self.client.get(reverse("detail", kwargs={"slug": project.slug}))
            self.assertEqual(res_detail.status_code, 200)


class ContextProcessorAndResilienceTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_context_processor_with_empty_database(self):
        # Ensure zero profiles and zero social links
        Profile.objects.all().delete()
        SocialLinks.objects.all().delete()

        # Context processor does not fail
        context = portfolio_globals(None)
        self.assertIsNone(context["profile"])
        self.assertEqual(list(context["sociallinks"]), [])

        # Homepage renders cleanly without errors
        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, '<h1 class="sitename">Portfolio</h1>')
        self.assertContains(res, '<strong>Portfolio</strong>. All rights reserved.')
