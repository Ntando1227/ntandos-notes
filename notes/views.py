from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note


def note_list(request):
    """Display all sticky notes."""

    notes = Note.objects.all()
    context = {
        "notes": notes,
        "page_title": "My Sticky Notes",
    }
    return render(request, "notes/note_list.html", context)


def note_detail(request, pk):
    """Display one sticky note."""

    note = get_object_or_404(Note, pk=pk)
    return render(
        request,
        "notes/note_detail.html",
        {
            "note": note,
            "page_title": note.title,
        },
    )


def note_create(request):
    """Create a new sticky note."""

    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save()
            return redirect("note_detail", pk=note.pk)
    else:
        form = NoteForm()

    return render(
        request,
        "notes/note_form.html",
        {
            "form": form,
            "page_title": "Create Note",
            "form_heading": "Create a New Note",
            "submit_label": "Save Note",
        },
    )


def note_update(request, pk):
    """Update an existing sticky note."""

    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            updated_note = form.save()
            return redirect("note_detail", pk=updated_note.pk)
    else:
        form = NoteForm(instance=note)

    return render(
        request,
        "notes/note_form.html",
        {
            "form": form,
            "note": note,
            "page_title": "Edit Note",
            "form_heading": "Edit Note",
            "submit_label": "Update Note",
        },
    )


def note_delete(request, pk):
    """Delete a sticky note after confirmation."""

    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        note.delete()
        return redirect("note_list")

    return render(
        request,
        "notes/note_confirm_delete.html",
        {
            "note": note,
            "page_title": "Delete Note",
        },
    )
