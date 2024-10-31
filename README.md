# Snippets

## Инструкция по развертыванию проекта
1. `python3 -m venv django_venv`

2. `source django_venv/bin/activate`

3. `pip install -r requirements.txt`

4. `python manage.py migrate`

5. `python manage.py runserver`


## Запуск `ipython` в контексте `django` приложений
```
python manage.py shell_plus --ipython
```

## Выгрузка и загрузка данных при работе с БД
### Выгрузить данные из БД
```
python manage.py dumpdata MainApp --indent 4 > MainApp/fixtures/save_all.json
```
### Загрузить данные в БД
```
python manage.py loaddata MainApp/fixtures/save_all.json
```
===========
ReadMe из FirstDjango:
# FirstDjango_28102024

## Инструкция по развертыванию проекта
1. 'python3 -m venv django_venv'
2. 'source django_venv/bin/activate'
3. 'pip install -r requirements.txt'
4. 'python manage.py migrate'
5. 'python manage.py runserver'

## запуск ipython в контексте приложений django:
    '''
    python manage.py shell_plus --ipython
    '''
## выгрузка всех данных из БД
    '''
    python manage.py dumpdata MainApp --indent 4 > ./fixtures/items.json
    эквивалентно
    python manage.py dumpdata MainApp --indent 4 > MainApp/fixtures/items.json
    '''
    ### примечание - если надо только Item модель (один класс):
    python manage.py dumpdata MainApp.item --indent 4 > ./fixtures/only_items.json


## загрузка данных из БД
    '''
    python manage.py loaddata ./fixtures/items.json
    '''


## Дополнительно для шаблонов:
1. Полезное дополнение для шаблонов 'Django' (в VSCode - Django Baptiste Darthenay)
'''
ext install batisteo.vscode-django
'''
Добавить в 'settings.json'
'''
"emmet.includeLanguages": {
    "django-html": "html",
},
"files.associations": {
    "*.html": "django-html"
}
'''