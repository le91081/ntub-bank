import os
def handle_uploaded_file(full_file_name, file):
    with open(full_file_name, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


def delete_file(full_file_name):
    try:
        os.remove(full_file_name)
    except:
        pass


def delete_file_start_with(dir, text):
    for file_name in os.listdir(dir):
        if file_name.startswith(text):
            os.remove(os.path.join(dir, file_name))


def mkdir_if_not_exist(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)