from django.shortcuts import render, get_object_or_404, redirect
from .models import Cloth
from .forms import ClothForm  # Assuming you have a form for cloth model

def cloth_list(request):
    """ View to list all cloth items """
    cloths = Cloth.objects.all()
    return render(request, 'cloth/cloth_list.html', {'cloths': cloths})

def cloth_detail(request, cloth_id):
    """ View to show details of a specific cloth item """
    cloth = get_object_or_404(Cloth, id=cloth_id)
    return render(request, 'cloth/cloth_detail.html', {'cloth': cloth})

def add_cloth(request):
    """ View to add a new cloth """
    if request.method == 'POST':
        form = ClothForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cloth_list')
    else:
        form = ClothForm()
    return render(request, 'cloth/add_cloth.html', {'form': form})

def edit_cloth(request, cloth_id):
    """ View to edit an existing cloth item """
    cloth = get_object_or_404(Cloth, id=cloth_id)
    if request.method == 'POST':
        form = ClothForm(request.POST, request.FILES, instance=cloth)
        if form.is_valid():
            form.save()
            return redirect('cloth_detail', cloth_id=cloth_id)
    else:
        form = ClothForm(instance=cloth)
    return render(request, 'cloth/edit_cloth.html', {'form': form})

def delete_cloth(request, cloth_id):
    """ View to delete a cloth item """
    cloth = get_object_or_404(Cloth, id=cloth_id)
    if request.method == 'POST':
        cloth.delete()
        return redirect('cloth_list')
    return render(request, 'cloth/delete_cloth.html', {'cloth': cloth})
