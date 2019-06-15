from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.service import advan_service


@login_required
def index(request):

    # 取得使用者列表
    user_list_data = advan_service.get_user_list()
    
    return render(request, 'recognize/index.html', {'user_list_data': user_list_data})

@login_required
def show_user(request, uuid):

    # 取得圖片
    images_data = advan_service.get_face_images_by_uuid(uuid)

    return render(request, 'recognize/show_user.html', {'images_data': images_data})