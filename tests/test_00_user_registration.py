import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class Test00UserRegistration:
    url_signup = '/api/v1/auth/signup/'
    url_token = '/api/v1/auth/token/'

    @pytest.mark.django_db(transaction=True)
    def test_00_nodata_signup(self, client):
        request_type = 'POST'
        response = client.post(self.url_signup)

        assert response.status_code != 404, (
            f'Страница `{self.url_signup}` не найдена, проверьте этот адрес в *urls.py*'
        )
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` без параметров '
            f'не создается пользователь и возвращается статус {code}'
        )
        response_json = response.json()
        empty_fields = ['email', 'username']
        for field in empty_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Проверьте, что при {request_type} запросе `{self.url_signup}` без параметров '
                f'в ответе есть сообщение о том, какие поля заполенены неправильно'
            )

    @pytest.mark.django_db(transaction=True)
    def test_00_invalid_data_signup(self, client):
        invalid_email = 'invalid_email'
        invalid_username = 'invalid_username@yamdb.fake'

        invalid_data = {
            'email': invalid_email,
            'username': invalid_username
        }
        request_type = 'POST'
        response = client.post(self.url_signup, data=invalid_data)

        assert response.status_code != 404, (
            f'Страница `{self.url_signup}` не найдена, проверьте этот адрес в *urls.py*'
        )
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` с невалидными данными '
            f'не создается пользователь и возвращается статус {code}'
        )

        response_json = response.json()
        invalid_fields = ['email']
        for field in invalid_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Проверьте, что при {request_type} запросе `{self.url_signup}` с невалидными параметрами, '
                f'в ответе есть сообщение о том, какие поля заполенены неправильно'
            )

        valid_email = 'validemail@yamdb.fake'
        invalid_data = {
            'email': valid_email,
        }
        response = client.post(self.url_signup, data=invalid_data)
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` без username '
            f'нельзя создать пользователя и возвращается статус {code}'
        )


    @pytest.mark.django_db(transaction=True)
    def test_00_valid_data_signup(self, client):

        valid_email = 'valid@yamdb.fake'
        valid_username = 'valid_username'

        valid_data = {
            'email': valid_email,
            'username': valid_username
        }
        request_type = 'POST'
        response = client.post(self.url_signup, data=valid_data)

        assert response.status_code != 404, (
            f'Страница `{self.url_signup}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` с валидными данными '
            f'создается пользователь и возвращается статус {code}'
        )
        assert response.json() == valid_data, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` с валидными данными '
            f'создается пользователь и возвращается статус {code}'
        )

        new_user = User.objects.filter(email=valid_email)
        assert new_user.exists(), (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` с валидными данными '
            f'создается пользователь и возвращается статус {code}'
        )
        new_user.delete()

    @pytest.mark.django_db(transaction=True)
    def test_00_obtain_jwt_token_invalid_data(self, client):

        request_type = 'POST'
        response = client.post(self.url_token)
        assert response.status_code != 404, (
            f'Страница `{self.url_signup}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе `{self.url_signup}` без параметров, '
            f'возвращается статус {code}'
        )

        invalid_data = {
            'confirmation_code': 12345
        }
        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе `{self.url_signup}` без username, '
            f'возвращается статус {code}'
        )

        invalid_data = {
            'username': 'unexisting_user',
            'confirmation_code': 12345
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 404
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе `{self.url_signup}` с несуществующим username, '
            f'возвращается статус {code}'
        )

        valid_email = 'valid@yamdb.fake'
        valid_username = 'valid_username'

        valid_data = {
            'email': valid_email,
            'username': valid_username
        }
        response = client.post(self.url_signup, data=valid_data)
        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` с валидными данными '
            f'создается пользователь и возвращается статус {code}'
        )

        invalid_data = {
            'username': valid_username,
            'confirmation_code': 12345
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе `{self.url_signup}` с валидным username, '
            f'но невалидным confirmation_code, возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_registration_me_username_restricted(self, client):
        valid_email = 'valid@yamdb.fake'
        invalid_username = 'me'
        request_type = 'POST'

        valid_data = {
            'email': valid_email,
            'username': invalid_username
        }
        response = client.post(self.url_signup, data=valid_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` '
            f'нельзя создать пользователя с username = "me" и возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_registration_same_email_restricted(self, client):
        valid_email_1 = 'test_duplicate_1@yamdb.fake'
        valid_email_2 = 'test_duplicate_2@yamdb.fake'
        valid_username_1 = 'valid_username_1'
        valid_username_2 = 'valid_username_2'
        request_type = 'POST'

        valid_data = {
            'email': valid_email_1,
            'username': valid_username_1
        }
        response = client.post(self.url_signup, data=valid_data)
        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` '
            f'можно создать пользователя с валидными данными и возвращается статус {code}'
        )

        duplicate_email_data = {
            'email': valid_email_1,
            'username': valid_username_2
        }
        response = client.post(self.url_signup, data=duplicate_email_data)
        assert response.status_code == 400, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` нельзя создать '
            f'пользователя, email которого уже зарегистрирован и возвращается статус {code}'
        )
        duplicate_username_data = {
            'email': valid_email_2,
            'username': valid_username_1
        }
        response = client.post(self.url_signup, data=duplicate_username_data)
        assert response.status_code == 400, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` нельзя создать '
            f'пользователя, username которого уже зарегистрирован и возвращается статус {code}'
        )
