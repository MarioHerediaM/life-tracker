from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Area, Actividad
from .forms import RegistroForm
from django.contrib.auth import login

def get_semana(offset=0):
    hoy = timezone.now().date()
    inicio = hoy - timezone.timedelta(days=hoy.weekday() + offset * 7)
    fin = inicio + timezone.timedelta(days=6)
    return inicio, fin


@login_required
def dashboard(request):
    offset = int(request.GET.get('semana', 0))
    inicio, fin = get_semana(offset)

    areas = Area.objects.filter(usuario=request.user)
    actividades = Actividad.objects.filter(
        usuario=request.user,
        fecha__range=[inicio, fin]
    )

    total_peso = sum(a.peso for a in areas) or 1
    stats = []
    for area in areas:
        acts = actividades.filter(area=area)
        pts = sum(a.puntos for a in acts)
        maximo = (area.peso / total_peso) * 15
        progreso = min(int((pts / maximo) * 100), 100) if maximo else 0
        stats.append({
            'area': area,
            'pts': pts,
            'count': acts.count(),
            'progreso': progreso,
        })

    total_pts = sum(s['pts'] for s in stats)
    score = min(sum(
        min((s['pts'] / ((s['area'].peso / total_peso) * 15)), 1) * s['area'].peso
        for s in stats
    ), 100) if stats else 0

    # Historial 4 semanas para la gráfica
    historial = []
    for i in range(3, -1, -1):
        ini, fin_h = get_semana(i)
        acts_h = Actividad.objects.filter(usuario=request.user, fecha__range=[ini, fin_h])
        pts_h = sum(a.puntos for a in acts_h)
        historial.append({'offset': i, 'pts': pts_h})

    context = {
        'stats': stats,
        'total_pts': total_pts,
        'score': int(score),
        'offset': offset,
        'inicio': inicio,
        'fin': fin,
        'historial': historial,
        'semanas': [(0, 'Esta semana'), (1, 'Sem. anterior'), (2, 'Hace 2 sem.'), (3, 'Hace 3 sem.')],
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def registrar_actividad(request):
    areas = Area.objects.filter(usuario=request.user)
    if request.method == 'POST':
        area_id = request.POST.get('area')
        descripcion = request.POST.get('descripcion')
        puntos = request.POST.get('puntos')
        area = get_object_or_404(Area, pk=area_id, usuario=request.user)
        Actividad.objects.create(
            usuario=request.user,
            area=area,
            descripcion=descripcion,
            puntos=puntos,
        )
        return redirect('dashboard')
    return render(request, 'tracker/registrar.html', {
        'areas': areas,
        'puntos_choices': Actividad.PUNTOS_CHOICES,
    })

@login_required
def gestionar_areas(request):
    areas = Area.objects.filter(usuario=request.user)
    if request.method == 'POST':
        Area.objects.create(
            usuario=request.user,
            nombre=request.POST.get('nombre'),
            emoji=request.POST.get('emoji', '⭐'),
            color=request.POST.get('color', '#4F8EF7'),
            peso=request.POST.get('peso', 10),
        )
        return redirect('gestionar_areas')
    return render(request, 'tracker/areas.html', {'areas': areas})


@login_required
def eliminar_area(request, pk):
    area = get_object_or_404(Area, pk=pk, usuario=request.user)
    area.delete()
    return redirect('gestionar_areas')


@login_required
def eliminar_actividad(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk, usuario=request.user)
    actividad.delete()
    return redirect('dashboard')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'tracker/registro.html', {'form': form})

@login_required
def editar_area(request, pk):
    area = get_object_or_404(Area, pk=pk, usuario=request.user)
    if request.method == 'POST':
        area.nombre = request.POST.get('nombre', area.nombre)
        area.emoji = request.POST.get('emoji', area.emoji)
        area.color = request.POST.get('color', area.color)
        area.peso = request.POST.get('peso', area.peso)
        area.save()
        return redirect('gestionar_areas')
    return render(request, 'tracker/editar_area.html', {'area': area})