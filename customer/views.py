from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .form import CustomerForm, UploadImageForm
from .models import Customer, CustomerImage

from core.utils.common_forms import DeleteConfirmForm
from core.settings import IMAGE_CUSTOMER_ROOT
from core.utils import file_utils

import uuid
import os


@login_required
def index(request):
    customer_list = Customer.objects.all().order_by('id')
    paginator = Paginator(customer_list, 10)

    page = request.GET.get('page')
    customers = paginator.get_page(page)
    return render(request,
                  'customer/index.html',
                  {
                      'customers': customers,
                      'page_range': range(customers.paginator.num_pages)
                  })


@login_required
def show(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    images = CustomerImage.objects.filter(customer=customer)
    return render(request, 'customer/show.html', {'customer': customer, 'images': images})


def add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()

            # 新增監視器使用者
            # advan_service.add_user(customer.uuid, customer.name)
            
            messages.success(request, '新增成功')
            return redirect('customer:index')
    else:
        form = CustomerForm()
    return render(request, 'customer/add.html', {'form': form})


def edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    images = CustomerImage.objects.filter(customer=customer)
    form = CustomerForm(request.POST or None, instance=customer)

    if form.is_valid():
        form.save()
        messages.success(request, '更新成功')
        return redirect('customer:index')

    return render(request, 'customer/edit.html', {
        'form': form,
        'images': images,
        'customer_id': customer.id,
        'upload_file_form': UploadImageForm()
    })


def delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = DeleteConfirmForm(request.POST or None)
    if form.is_valid() and form.cleaned_data['check']:
        customer.delete()
        messages.success(request, '刪除成功')
        return redirect('customer:index')

    return render(request, 'customer/delete.html', {'form': form})


def delete_image(request, pk):
    image = get_object_or_404(CustomerImage, pk=pk)
    form = DeleteConfirmForm(request.POST or None)
    if form.is_valid() and form.cleaned_data['check']:
        # 取得customer_id, 重整用
        customer_id = image.customer.id
        # 刪實體圖
        file_utils.delete_file(os.path.join(
            IMAGE_CUSTOMER_ROOT, image.file_path.split("/")[-1]))
        # 刪model
        image.delete()
        messages.success(request, '刪除成功')
        return redirect('customer:edit', pk=customer_id)

    return render(request, 'customer/delete_image.html', {'form': form})


def upload_image(request, customer_id):

    form = UploadImageForm(request.POST, request.FILES)
    if form.is_valid():
        # get customer
        customer = get_object_or_404(Customer, pk=customer_id)

        # 改名, 以id為頭
        file_name = uuid.uuid4().hex.upper() + '.jpg'
        file_name = "{}_{}".format(customer.id, file_name)

        # 存檔
        file_utils.handle_uploaded_file(os.path.join(
            IMAGE_CUSTOMER_ROOT, file_name), request.FILES['file'])

        # 相對路徑
        file_relative_path = "/images/customer/{}".format(file_name)

        customer_picture = CustomerImage()
        # 存相對路徑
        customer_picture.file_path = file_relative_path
        customer_picture.type = form.cleaned_data['type']
        customer_picture.customer = customer
        customer_picture.save()
        messages.success(request, '上傳成功')
        return redirect('customer:edit', pk=customer_id)

    messages.success(request, '上傳失敗')
    return redirect('customer:edit', pk=customer_id)
