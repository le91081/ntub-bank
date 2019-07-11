from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import Preset
from .forms import PresetForm
# Create your views here.


def index(request):
    preset_list = Preset.objects.all()

    return render(request, 'preset/index.html', {'preset_list': preset_list})


def edit(request, pk):
    item = get_object_or_404(Preset, pk=pk)

    form = PresetForm(request.POST or None, instance=item)

    if form.is_valid():
        with transaction.atomic():
            form.save()
            messages.success(request, '更新成功')
            return redirect('preset:index')
            
    return render(request, 'preset/edit.html', {'form': form})
