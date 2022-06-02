import os.path

from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
        запрашиваем список всех питомцев и проверяем, что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name="Рыся", animal_type="рысь", age=2, pet_photo="images/ryska.jpg"):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_delete_self_pet_successful():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Сима', 'кошка', 3, 'image/siamcat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_my_pet_successful(name='Рысь', animal_type="рысь", age=3):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('My pets are not here.')


# Негативное тестирование:

# 1. Ввод неверного email.
def test_get_api_key_for_invalid_email(email="sunshine@yandex", password=valid_password):
    """ Проверяем, что запрос api ключа при вводе неверного email возвращает статус 403
        и в результате нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


# 2. Ввод неверного пароля.
def test_get_api_key_for_invalid_password(email=valid_email, password="sdokj13kj5ok28"):
    """ Проверяем, что запрос api ключа при вводе неверного пароля возвращает статус 403
            и в результате нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


# 3. Данные email отсутствуют.
def test_get_api_key_for_null_email(email="", password=valid_password):
    """ Проверяем, что запрос api ключа при пустом поле email возвращает статус 403
            и в результате нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


# 4. Данные пароля отсутствуют.
def test_get_api_key_for_null_password(email=valid_email, password=""):
    """ Проверяем, что запрос api ключа при пустом поле password возвращает статус 403
            и в результате нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


# 5. Вход в систему при пустых email и пароле.
def test_get_api_key_for_invalid_user(email="", password=""):
    """ Проверяем, что запрос api ключа при пустых email и пароле возвращает статус 403
            и в результате нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


# 6. При добавлении нового питомца указан некорректный возраст (age=58456488).
def test_add_new_pet_with_invalid_age(name="Рыся", animal_type="рысь",
                                      age=58456488, pet_photo="images/ryska.jpg"):
    """Проверяем, что добавление питомца с указанием некорректного значения возраста приводит
        к статусу кода 400"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


# 7. При добавлении нового питомца указано несуществующее фото питомца (images/riskaaa.jpg).
def test_add_new_pet_with_invalid_photo(name="Рыся", animal_type="рысь", age=2, pet_photo="images/riskaaa.jpg"):
    """Проверяем, что добавление питомца с некорректным фото приводит
            к статусу кода 400"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


# 8. При добавлении нового питомца отсутствует имя питомца (name="").
def test_add_new_pet_without_name(name="", animal_type="рысь", age=2, pet_photo="images/ryska.jpg"):
    """Проверяем, что добавление питомца с пустым полем 'name' приводит к статусу кода 400"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


# 9. При добавлении нового питомца отсутствует тип животного (animal_type=""):
def test_add_new_pet_without_animal_type(name="Рыся", animal_type="", age=2, pet_photo="images/ryska.jpg"):
    """Проверяем, что добавление питомца с пустым полем 'animal_type' приводит к статусу кода 400"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


# 10. Обновление информации о питомце с теми же данными.
def test_update_my_pet_with_the_same_data(name="Рыся", animal_type="рысь", age=2):
    """Проверяем, что обновление информации о питомце без изменения данных приведет к ошибке пользователя
        с кодом 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
