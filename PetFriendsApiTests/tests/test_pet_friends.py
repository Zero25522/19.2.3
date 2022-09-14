from api import PetFriends
from settings import valid_email, valid_password, string_of_256, string_of_1000, some_numbers
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_all_pats_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >0

def test_add_new_pet_with_valid_data(name='Белыш', animal_type='гусь',
                                     age='3', pet_photo='images/photo2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Atkbrc", "кот", "4", "images/photo2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Густав', animal_type='Гусь', age=2):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_get_all_my_pets_with_valid_key(filter="my_pets"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200

def test_get_all_pats_with_long_filter(filter=string_of_256):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_get_all_pats_with_to_long_filter(filter=string_of_1000):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_get_all_pats_with_nembers_in_filter(filter= some_numbers):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_failed_delete_self_pet_empty_id():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # if len(my_pets['pets']) == 0:
    #     pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
    #     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = ''
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 404

def test_get_api_key_with_wrong_email(email="valid_email", password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_with_wrong_password(email=valid_email, password="valid_password"):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_with_text_file(name='Белыш', animal_type='гусь',
                                     age='1', pet_photo='images/photo3.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert result['name'] == name

def test_add_simple_pet_with_valid_data(name='Алекс', animal_type='бульдог',age='8'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_to_pet(pet_photo='images/photo2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, 'Алекс', "бульдог", "8")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert 'pet_photo' in result

def test_add_simple_pet_with_invalid_animal_type(name='Алекс', animal_type=9,age='8'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple_wrong(auth_key, name, animal_type, age)

    assert status == 403

def test_add_new_pet_with_broke_photo(name='Белыш', animal_type='гусь',
                                     age='3', pet_photo='images/photo4.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] == name

