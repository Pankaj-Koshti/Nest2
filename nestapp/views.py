from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, NoteUploadForm
from .models import Note , MyNotes

def landingpage(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landingpage')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def upload_note_view(request):
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            return redirect('success_page')
    else:
        form = NoteUploadForm()
    return render(request, 'upload_note.html', {'form': form})

def success_page(request):
    return render(request, 'success_page.html')

def search_notes_view(request):
    branches = ['CSE', 'ECE', 'ME']  # Replace with actual branches
    semesters = range(1, 9)  # Assuming 8 semesters

    keyword = request.GET.get('keyword', '')
    branch = request.GET.get('branch', '')
    semester = request.GET.get('semester', '')

    notes = Note.objects.filter(is_approved=True)

    if keyword:
        notes = notes.filter(subject__icontains=keyword)

    if branch:
        notes = notes.filter(branch=branch)

    if semester:
        notes = notes.filter(semester=int(semester))

    context = {
        'notes': notes,
        'branches': branches,
        'semesters': semesters,
    }

    return render(request, 'search_notes.html', context)

@login_required
def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, is_approved=True)
    
    # Check if the user has already added this note to "My Notes"
    added_to_my_notes = note in request.user.notes.all()  # Ensure you have a many-to-many relationship

    # Build the full URL for the PDF file
    pdf_url = request.build_absolute_uri(note.file.url) if note.file else None

    context = {
        'note': note,
        'added_to_my_notes': added_to_my_notes,
        'pdf_url': pdf_url,
    }
    return render(request, 'view_note.html', context)

@login_required
def add_to_my_notes(request, note_id):
    note = get_object_or_404(Note, id=note_id, is_approved=True)
    user = request.user

    # Check if the note is already added to "My Notes"
    if not MyNotes.objects.filter(user=user, note=note).exists():
        MyNotes.objects.create(user=user, note=note)  # Add to My Notes
        print("Note added to My Notes")
    else:
        print("Note already in My Notes")

    # Redirect back to the view_note page after adding the note
    return redirect('view_note', note_id=note.id)


@login_required
def my_notes(request):
    notes = MyNotes.objects.filter(user=request.user)
    return render(request, 'my_notes.html', {'notes': notes})