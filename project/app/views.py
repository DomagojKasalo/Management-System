from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, PredmetiForm, KorisnikForm, UpisniForm, StatusForm, AssignForm
from .models import Uloge, Predmeti, Korisnik, Upis
from .decorators import admin_required, profesor_required, student_required
from django.db.models import Count
from django.db.models import Q


# Create your views here.

@admin_required
def zad(request):
    subjects = Predmeti.objects.all()
    subject_data = []
    for subject in subjects:
        redovni = Upis.objects.filter(
            predmet_id=subject,
            status='polozen',
            student_id__status='red'
        ).count()
        vanredni = Upis.objects.filter(
            predmet_id=subject,
            status='polozen',
            student_id__status='izv'
        ).count()
        subject_info = {
            'id': subject.id,
            'name': subject.name,
            'polozeni': redovni+vanredni,
            'polozeni_redovni': redovni,
            'polozeni_izvanredni': vanredni,
        }
        subject_data.append(subject_info)

    context = {'subjects': subject_data}
    return render(request, 'zad1.html', context)


@admin_required
def drugi(request, predmet_id):
    subject = get_object_or_404(Predmeti, pk=predmet_id)

    redovni = Upis.objects.filter(
        predmet_id=predmet_id,
        status='polozen',
        student_id__status='red'
    )
    vanredni = Upis.objects.filter(
        predmet_id=predmet_id,
        status='polozen',
        student_id__status='izv'
    )
    
    redovni_studenti = [upis.student_id.username for upis in redovni]
    izvanredni_studenti = [upis.student_id.username for upis in vanredni]
    
    subject_info = {
        'name': subject.name,
        'polozeni_redovni': redovni_studenti,
        'polozeni_izvanredni': izvanredni_studenti,
    }

    context = {'subject': subject_info}
    return render(request, 'vidi-detalje.html', context)

@login_required(login_url='login')
def index(request):
    user = request.user
    if user.is_authenticated:
        role = user.uloge.uloga
        if role == 'admin':
            return render(request, 'admin_home.html')
        elif role == 'profesor':
            return render(request, 'profesor_home.html')
        elif role == 'student':
            return render(request, 'student_home.html')
    return render(request, 'error.html')

def error(request):
    return render(request, 'error.html')

def create_user(request):
    if request.user.uloge.uloga == 'admin':
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = CreateUserForm()
        context = {'form': form}
        return render(request, 'create_user.html', context)
    else:
        return render(request, 'error.html')

@admin_required
def predmeti_list(request):
    predmeti = Predmeti.objects.all()
    context = {'predmeti': predmeti}
    return render(request, 'predmeti.html', context)

@admin_required
def predmet_edit(request, pk):
    predmet = get_object_or_404(Predmeti, pk=pk)
    
    if request.method == 'POST':
        form = AssignForm(request.POST)
        if form.is_valid():
            profesor = form.cleaned_data['profesor']
            predmet = form.cleaned_data['predmet']
            predmet.nositelj = profesor
            predmet.save()
            return redirect('predmeti')
    else:
        form = AssignForm()
    
    return render(request, 'predmet-edit.html', {'predmet': predmet, 'form': form})

@admin_required
def predmeti_detail(request, pk):
    predmet = get_object_or_404(Predmeti, id=pk)
    context = {
        'predmet': predmet
    }
    return render(request, 'predmet-details.html', context)

@admin_required
def predmeti_create(request):
    if request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('predmeti')
    else:
        form = PredmetiForm()
    
    return render(request, 'predmet-create.html', {'form': form})

@admin_required
def student_list(request):
    students = Korisnik.objects.filter(uloge__uloga='student')
    return render(request, 'studenti.html', {'students': students})

@admin_required
def student_edit(request, pk):
    student = get_object_or_404(Korisnik, pk=pk)
    
    if request.method == 'POST':
        form = KorisnikForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('studenti')
    else:
        form = KorisnikForm(instance=student)
    
    return render(request, 'student-edit.html', {'student': student, 'form': form})

@admin_required
def student_detail(request, pk):
    student = get_object_or_404(Korisnik, pk=pk)
    context = {
        'student': student
    }
    return render(request, 'student-details.html', context)

@admin_required
def student_create(request):
    if request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studenti')
    else:
        form = KorisnikForm()
    return render(request, 'student-create.html', {'form': form})

@admin_required
def profesor_list(request):
    profesori = Korisnik.objects.filter(uloge__uloga='profesor')
    return render(request, 'profesori.html', {'profesori': profesori})

@admin_required
def profesor_edit(request, pk):
    profesor = get_object_or_404(Korisnik, pk=pk)
    
    if request.method == 'POST':
        form = KorisnikForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('profesor-edit', pk=pk)
    else:
        form = KorisnikForm(instance=profesor)
    
    return render(request, 'profesor-edit.html', {'profesor': profesor, 'form': form})

@admin_required
def profesor_detail(request, pk):
    profesor = get_object_or_404(Korisnik, pk=pk)
    context = {
        'profesor': profesor
    }
    return render(request, 'profesor-details.html', context)

@admin_required
def profesor_create(request):
    if request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profesori')
    else:
        form = KorisnikForm()
    return render(request, 'profesor-create.html', {'form': form})
    
@profesor_required
def predmeti_list_for_each_profesor(request):
    profesor = request.user
    predmeti = Predmeti.objects.filter(nositelj=profesor)
    return render(request, 'predmet-profesor.html', {'predmeti': predmeti})

@profesor_required
def studenti_popis(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    upisi = Upis.objects.filter(predmet_id=predmet)
    students = []
    for upis in upisi:
        student = upis.student_id
        students.append(student)
    return render(request, 'studenti-popis.html', {'students': students, 'predmet_id': predmet_id})

@profesor_required
def popis_studenata(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    upisi = Upis.objects.filter(predmet_id=predmet)
    students = []
    for upis in upisi:
        student = upis.student_id
        students.append(student)
    return render(request, 'popis-studenata.html', {'students': students, 'predmet_id': predmet_id})

@profesor_required
def status_edit(request, predmet_id, student_id):
    upis = Upis.objects.get(predmet_id=predmet_id, student_id=student_id)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=upis)
        if form.is_valid():
            form.save()
            return redirect('popis-studenata', predmet_id=predmet_id)
    else:
        form = StatusForm(instance=upis)

    return render(request, 'status-edit.html', {'upis':upis, 'form': form}, )

@profesor_required
def popis_studenata_izgubljen_potpis(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    upisi = Upis.objects.filter(predmet_id=predmet, status='izgubio potpis')
    students = []
    for upis in upisi:
        student = upis.student_id
        students.append(student)
    return render(request, 'izgubio-potpis.html', {'students': students, 'predmet_id': predmet_id})

@profesor_required
def popis_studenata_upisan(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    upisi = Upis.objects.filter(predmet_id=predmet, status='upisan')
    students = []
    for upis in upisi:
        student = upis.student_id
        students.append(student)
    return render(request, 'upisan.html', {'students': students, 'predmet_id': predmet_id})

@profesor_required
def popis_studenata_polozen(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    upisi = Upis.objects.filter(predmet_id=predmet, status='polozen')
    students = []
    for upis in upisi:
        student = upis.student_id
        students.append(student)
    return render(request, 'polozen.html', {'students': students, 'predmet_id': predmet_id})

@admin_required
def upisni_listovi(request):
    upisni = Upis.objects.all()
    context = {'upisni': upisni}
    return render(request, 'upisni-listovi.html', context)

@admin_required
def upisni_list_edit(request, pk):
    upisni = get_object_or_404(Upis, pk=pk)
    
    if request.method == 'POST':
        form = UpisniForm(request.POST, instance=upisni)
        if form.is_valid():
            form.save()
            return redirect('upisni-listovi')
    else:
        form = UpisniForm(instance=upisni)
    
    return render(request, 'upisni-list-edit.html', {'upisni': upisni, 'form': form})

@admin_required
def upisni_list_create(request):
    if request.method == 'POST':
        form = UpisniForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upisni-listovi')
    else:
        form = UpisniForm()
    return render(request, 'upisni-list-create.html', {'form': form})

# Upis/ispis

@student_required
def upis_predmeta(request):
    student = request.user
    upisani_predmeti_ids = Upis.objects.filter(student_id=student, status__in=['upisan', 'polozen']).values_list('predmet_id', flat=True)
    predmeti_not_upisan_polozen = Predmeti.objects.exclude(id__in=upisani_predmeti_ids)
    
    semesters = {}
    for predmet in predmeti_not_upisan_polozen:
        if student.status == 'red':
            semester_field = predmet.sem_red
        elif student.status == 'izv':
            semester_field = predmet.sem_izv
        else:
            semester_field = None
        
        if semester_field is not None:
            if semester_field not in semesters:
                semesters[semester_field] = []
            semesters[semester_field].append(predmet)
    
    return render(request, 'predmeti-list.html', {'semesters': semesters})

@student_required
def add_predmet(request, predmet_id):
    student = request.user
    predmet = Predmeti.objects.get(id=predmet_id)
    Upis.objects.create(student_id=student, predmet_id=predmet, status='upisan')
    return redirect('upisi_list')

@student_required
def upisni_list(request):
    student = request.user
    upisi = Upis.objects.filter(student_id=student)
    return render(request, 'upisi_list.html', {'upisi': upisi})

@student_required
def upisi_delete(upis_id):
    upis = get_object_or_404(Upis, id=upis_id)
    upis.delete()
    return redirect('upisi_list')

