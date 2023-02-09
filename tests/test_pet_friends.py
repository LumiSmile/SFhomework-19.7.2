from api import PetFriends
from settings import *
from api import os


class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    def test_get_API_keyForValidUser(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_API_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_getAllPetsWithValidKey(self, filter=''):  # filter available values : my_pets
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_addNewPetWithValidData(self, name='Барбоскин', animal_type='двортерьер', age='4',
                                    pet_photo='images/cat1.jpg'):

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_successfulDeleteSelfPet(self):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = myPets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in myPets.values()

    def test_successfulUpdateSelfPetInfo(self, name='Мурзик', animal_type='Котэ', age=5):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    def test_addNewPetWithoutPhoto(self, name='Брайан', animal_type='Собака', age='11'):

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        print(f'добавлен {result}')

    def test_addPhotoOfPet(self, pet_photo='images/dog_Brayan.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = self.pf.add_photo_of_pet(auth_key, my_pets['pets'][1]['id'], pet_photo)
            _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

            assert status == 200
            assert result['pet_photo'] == my_pets['pets'][1]['pet_photo']
            print(f'фото добавлено {result}')
        else:
            raise Exception('Питомцы отсутствуют')

    def test_get_API_keyForInvalidEmailUser(self, email=invalid_email, password=valid_password):
        status, result = self.pf.get_API_key(email, password)
        assert status >= 400
        print(f'Ошибка ввода данных пользователя')

    def test_get_API_keyForInvalidPasswordUser(self, email=valid_email, password=invalid_password):
        status, result = self.pf.get_API_key(email, password)
        assert status >= 400
        print(f'Ошибка ввода данных пользователя')

    def test_successfulUpdateExixtingPetInfo(self, name='Брайан Кинни', animal_type='Собака', age=11):

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)

            assert status == 200
            assert result['name'] == name
            print('ok')
            print(result)
        else:
            raise Exception("There is no my pets")

    def test_getAllPetsWithInvalidKey(self, filter=''):
        filter = 'my__pets'
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 500
        print(f'Статус {status}')

    def test_addPetWithTooOldAge(self, name='Мишка', animal_type='Кот', age = '999', pet_photo='images/Misha.jpg'):

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        age = int(result['age'])
        assert status == 200
        assert (age > 20 or age < 0)
        print(f'Это очень древнее животное! Eму не может быть {age} лет!')

    def test_addPetWithSymbolAge(self, name='Мишель', animal_type='Кошка', pet_photo='images/Misha.jpg'):
        age = '№№№'
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        assert status == 200
        assert age
        print(f'Не нужно добавлять питомца с нечисловым возрастом {age}')

    def test_addPetWithEmptyData(self, name='', animal_type='', age=''):

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name
        print('ok')
        print(f'Сайт позволяет добавлять питомецев с пустыми значениями {result}')

    def test_addPetWithBigCountOfSymbolsInAnimaType(self, name='Брайан ', age='11', pet_photo='images/P1040103.jpg'):

        animal_type = '87ылотHKhVfcjLHb%<>|JK1!kdjвомтшгьПНГнпШГОЗЩJoiUHgobh'

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        list_animal_type = result['animal_type']
        symbol_count = len(list_animal_type)

        assert status == 200
        assert symbol_count > 25
        print(f'Порода питомца не может быть {symbol_count} символа')