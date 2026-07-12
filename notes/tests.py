from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Note",
            content="This is test content.",
        )

    def test_note_has_correct_title(self):
        self.assertEqual(self.note.title, "Test Note")

    def test_note_has_correct_content(self):
        self.assertEqual(
            self.note.content,
            "This is test content.",
        )

    def test_note_string_representation(self):
        self.assertEqual(str(self.note), "Test Note")


class NoteURLTest(TestCase):
    """Tests for the note URL patterns."""

    def setUp(self):
        self.note = Note.objects.create(
            title="URL Test Note",
            content="Testing URL routes.",
        )

    def test_note_list_url(self):
        self.assertEqual(reverse("note_list"), "/")

    def test_note_create_url(self):
        self.assertEqual(
            reverse("note_create"),
            "/note/new/",
        )

    def test_note_detail_url(self):
        self.assertEqual(
            reverse(
                "note_detail",
                args=[self.note.id],
            ),
            f"/note/{self.note.id}/",
        )

    def test_note_update_url(self):
        self.assertEqual(
            reverse(
                "note_update",
                args=[self.note.id],
            ),
            f"/note/{self.note.id}/edit/",
        )

    def test_note_delete_url(self):
        self.assertEqual(
            reverse(
                "note_delete",
                args=[self.note.id],
            ),
            f"/note/{self.note.id}/delete/",
        )


class NoteViewTest(TestCase):
    """Tests for the note views."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Existing Note",
            content="Existing note content.",
        )

    def test_note_list_view(self):
        response = self.client.get(
            reverse("note_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Existing Note",
        )
        self.assertTemplateUsed(
            response,
            "notes/note_list.html",
        )

    def test_note_detail_view(self):
        response = self.client.get(
            reverse(
                "note_detail",
                args=[self.note.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Existing Note",
        )
        self.assertContains(
            response,
            "Existing note content.",
        )
        self.assertTemplateUsed(
            response,
            "notes/note_detail.html",
        )

    def test_note_create_page_loads(self):
        response = self.client.get(
            reverse("note_create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "notes/note_form.html",
        )

    def test_note_can_be_created(self):
        response = self.client.post(
            reverse("note_create"),
            {
                "title": "New Note",
                "content": "New note content.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Note.objects.filter(
                title="New Note"
            ).exists()
        )

    def test_invalid_note_is_not_created(self):
        note_count_before = Note.objects.count()

        response = self.client.post(
            reverse("note_create"),
            {
                "title": "",
                "content": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Note.objects.count(),
            note_count_before,
        )

    def test_note_can_be_updated(self):
        response = self.client.post(
            reverse(
                "note_update",
                args=[self.note.id],
            ),
            {
                "title": "Updated Note",
                "content": "Updated note content.",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.note.refresh_from_db()

        self.assertEqual(
            self.note.title,
            "Updated Note",
        )
        self.assertEqual(
            self.note.content,
            "Updated note content.",
        )

    def test_note_delete_confirmation_page_loads(self):
        response = self.client.get(
            reverse(
                "note_delete",
                args=[self.note.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "notes/note_confirm_delete.html",
        )

    def test_note_can_be_deleted(self):
        note_id = self.note.id

        response = self.client.post(
            reverse(
                "note_delete",
                args=[note_id],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Note.objects.filter(
                id=note_id
            ).exists()
        )

    def test_missing_note_returns_404(self):
        response = self.client.get(
            reverse(
                "note_detail",
                args=[9999],
            )
        )

        self.assertEqual(response.status_code, 404)
