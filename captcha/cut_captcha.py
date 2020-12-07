from PIL import Image
import os
import re


def get_id_in_captcha_name(file_name: str):
    fn = file_name.split('\\')[-1]
    id = fn.split('.')[0]
    return id

def cut_and_save_captcha(file_name, folder):
    # Mở ảnh
    im = Image.open(file_name) 

    # Đặt vị trí cắt cho ảnh
    img_1 = (0, 0, 30, 32)
    img_2 = (30, 0, 60, 32)
    img_3 = (60, 0, 90, 32)
    img_4 = (90, 0, 120, 32)

    # Cắt ảnh
    img_cha_1 = im.crop(img_1)
    img_cha_2 = im.crop(img_2)
    img_cha_3 = im.crop(img_3)
    img_cha_4 = im.crop(img_4)

    # Lưu ảnh
    captcha_id = get_id_in_captcha_name(file_name)
    img_cha_1.save('{0}\\img1__{1}.jpeg'.format(folder, captcha_id))
    img_cha_2.save('{0}\\img2__{1}.jpeg'.format(folder, captcha_id))
    img_cha_3.save('{0}\\img3__{1}.jpeg'.format(folder, captcha_id))
    img_cha_4.save('{0}\\img4__{1}.jpeg'.format(folder, captcha_id))

def create_folder_contains_letter():
    if os.path.exists('letters') == False:
        os.mkdir('letters')
    upper_alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for letter in upper_alphabets:
        if os.path.exists('letters\\{0}'.format(letter)) == False:
            os.mkdir('letters\\{0}'.format(letter))

def cut_captcha_with_name_is_resolved(file_name: str):
    # Mở ảnh
    im = Image.open(file_name)

    # Đặt vị trí cắt cho ảnh
    img_1 = (0, 0, 30, 32)
    img_2 = (30, 0, 60, 32)
    img_3 = (60, 0, 90, 32)
    img_4 = (90, 0, 120, 32)

    # Cắt ảnh
    img_cha_1 = im.crop(img_1)
    img_cha_2 = im.crop(img_2)
    img_cha_3 = im.crop(img_3)
    img_cha_4 = im.crop(img_4)

    # Lưu ảnh
    letter = get_id_in_captcha_name(file_name).upper()
    img_cha_1.save('letters\\{0}\\{1}.jpeg'.format(letter[0], letter))
    img_cha_2.save('letters\\{0}\\{1}.jpeg'.format(letter[1], letter))
    img_cha_3.save('letters\\{0}\\{1}.jpeg'.format(letter[2], letter))
    img_cha_4.save('letters\\{0}\\{1}.jpeg'.format(letter[3], letter))

def cut_captcha_and_move():
    for file_name in os.listdir('resolved_captchas'):
        id = get_id_in_captcha_name(file_name)
        if re.search('^[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9]', id) and len(id)==4:
            path = 'resolved_captchas\\{0}'.format(file_name)
            cut_captcha_with_name_is_resolved(path)

if __name__ == "__main__":
    # create_folder_contains_letter()
    # cut_captcha_with_name_is_resolved('resolved_captchas\\2AQD.jpeg')
    cut_captcha_and_move()