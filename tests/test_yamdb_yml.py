import os
import re

from django.conf import settings


class TestWorkflow:

    def test_workflow(self):
        api_review_workflow_basename = 'api_review_workflow'

        yaml = f'{api_review_workflow_basename}.yaml'
        is_yaml = yaml in os.listdir(settings.BASE_DIR)

        yml = f'{api_review_workflow_basename}.yml'
        is_yml = yml in os.listdir(settings.BASE_DIR)

        if not is_yaml and not is_yml:
            assert False, (
                'В корневом каталоге проекта не найден файл с описанием workflow '
                f'{yaml} или {yml}.\n'
                '(Это нужно для проверки тестами на платформе)'
            )

        if is_yaml and is_yml:
            assert False, (
                f'В корневом каталоге не должно быть двух файлов {api_review_workflow_basename} '
                'с расширениями .yaml и .yml'
            )

        filename = yaml if is_yaml else yml

        try:
            with open(f'{os.path.join(settings.BASE_DIR, filename)}', 'r') as f:
                review = f.read()
        except FileNotFoundError:
            assert False, f'Проверьте, что добавили файл {filename} в корневой каталог для проверки'

        assert (
                re.search(r'on:\s*push:\s*branches:\s*-\smaster', review) or
                'on: [push]' in review or
                'on: push' in review
        ), f'Проверьте, что добавили действие при пуше в файл {filename}'
        assert 'pytest' in review, f'Проверьте, что добавили pytest в файл {filename}'
        assert 'appleboy/ssh-action' in review, f'Проверьте, что добавили деплой в файл {filename}'
        assert 'appleboy/telegram-action' in review, (
            'Проверьте, что добавили доставку отправку telegram сообщения '
            f'в файл {filename}'
        )
