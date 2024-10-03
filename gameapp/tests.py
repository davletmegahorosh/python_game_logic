# import base64
#
# file_path = '/Users/Davlet/Downloads/team2.py'
#
# with open(file_path, 'rb') as file:
#     file_data = file.read()
#
# encoded_data = base64.b64encode(file_data)
#
# encoded_str = encoded_data.decode('utf-8')
#
# data_uri = f'data:text/x-python;base64,{encoded_str}'
#
# print(f'Закодированный файл в base64: {encoded_str}')
# decoded_data = base64.b64decode(encoded_str)
#
# output_file_path = 'decoded_file.cpp'
#
# with open(output_file_path, 'wb') as output_file:
#     output_file.write(decoded_data)
#
# print(f'Декодированные данные записаны в файл: {output_file_path}')
# import random
#
# file_1_obj = "file_1.py"
# file_2_obj = "file_2.py"
#
# random_player = [file_1_obj, file_2_obj]
#
# random.shuffle(random_player)
#
# print(random_player)
#
# file_1_obj, file_2_obj = random_player[0], random_player[1]
# import random
# print(random.randint(0,1))

for i in range(1,2):
    print(i)