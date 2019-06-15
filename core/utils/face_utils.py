# import face_recognition
# from os import listdir
# from os.path import isfile, join
# from core.settings import IMAGE_ROOT, IMAGE_CUSTOMER_ROOT, IMAGE_BLACK_LIST_ROOT

# """
#     return : 
#     {
#         "name1": 0.83,
#         .
#         .
#     }
# """
# def recognize(unknown_face_file_name, correct_rate):
#     result = {}
#     # all file name in faces folder
#     full_path_customer_file_names = [ join(IMAGE_CUSTOMER_ROOT, file_name) for file_name in listdir(IMAGE_CUSTOMER_ROOT) if 'selfie_picture' in file_name]
#     full_path_black_list_file_names = [ join(IMAGE_BLACK_LIST_ROOT, file_name) for file_name in listdir(IMAGE_BLACK_LIST_ROOT) if file_name.endswith('.jpg')]
#     full_path_file_names = full_path_customer_file_names + full_path_black_list_file_names

#     # load file_names face
#     known_images = [ face_recognition.load_image_file(file_name) for file_name in full_path_file_names ]

#     # load unknown face
#     unknown_image = face_recognition.load_image_file(unknown_face_file_name)

#     # encoding
#     known_encoding = []
#     for known_image in known_images:
#         face_encodings = face_recognition.face_encodings(known_image)
#         if len(face_encodings) > 0:
#             known_encoding.append(face_encodings[0])

#     unknown_encodings = face_recognition.face_encodings(unknown_image)
#     if len(unknown_encodings) == 0:
#         return result, '傳送的圖片沒有偵測到臉部'
#     unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

#     # results
#     # compare_result = face_recognition.compare_faces(known_encoding, unknown_encoding, tolerance=0.5)
#     compare_result = face_recognition.face_distance(known_encoding, unknown_encoding)
#     compare_result = list(compare_result)

#     # filter > correct_rate
#     for i in range(len(compare_result)):
#         if (1 - compare_result[i]) > correct_rate:
#             result[full_path_file_names[i].split('/')[-1]] = 1 - compare_result[i]
    
#     return result, None

# # print(is_image_in_system("unknown2.jpg"))