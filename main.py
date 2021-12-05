import os
import shutil
import stat
import sys


def print_menu():
    print('1. Отображение списка файлов и папок заданной директории с указанием их размера\n'
          '2. Создание нового файла\n'
          '3. Копирование файла\n'
          '4. Удаление файла/директории\n'
          '5. Переименование/перемещение директории\n'
          '6. Установка атрибута «Только для чтения»\n'
          '7. Снятие атрибута «Только для чтения»\n'
          '8. Проверка атрибута «Скрытый»\n'
          '0. Выход\n')


def print_dir(dir_path):
    if not os.path.exists(dir_path):
        raise FileExistsError

    if dir_path[len(dir_path) - 1] != '/':
        dir_path += '/'
    items = os.listdir(dir_path)
    for item in items:
        if os.path.isdir(dir_path + item):
            size = round(get_dir_size(dir_path + item) / 1024)
        else:
            size = round(os.path.getsize(dir_path + item) / 1024)
        print(item, size, 'KB')


def get_dir_size(dir_path):
    if not os.path.exists(dir_path):
        raise FileExistsError

    size = 0
    for path, dirs, files in os.walk(dir_path):
        for file in files:
            fp = os.path.join(path, file)
            size += os.path.getsize(fp)

    return size


def create_file(file_path):
    fd = os.open(file_path, os.O_RDWR | os.O_CREAT)
    os.close(fd)
    print('Успешно')


def copy_file(file_path_from, file_path_to):
    if not os.path.exists(file_path_from):
        raise FileExistsError

    shutil.copy2(file_path_from, file_path_to)
    print('Успешно')


def delete_item(item_path):
    if not os.path.exists(item_path):
        raise FileExistsError

    if os.path.isdir(item_path):
        shutil.rmtree(item_path)
    else:
        os.remove(item_path)
    print('Успешно')


def move_dir(dir_path_from, dir_path_to):
    if not os.path.exists(dir_path_from):
        raise FileExistsError

    shutil.move(dir_path_from, dir_path_to)
    print('Успешно')


def set_attr_readonly(item_path):
    if not os.path.exists(item_path):
        raise FileExistsError

    if sys.platform == 'win32':
        os.chmod(item_path, stat.S_IREAD)
    elif sys.platform == 'linux':
        os.system("sudo chattr +i " + item_path)
    else:
        raise Exception('Неопознанная операционная система')

    # os.chmod(item_path, 0o444)
    print('Успешно')


def unset_attr_readonly(item_path):
    if not os.path.exists(item_path):
        raise FileExistsError

    if sys.platform == 'win32':
        os.chmod(item_path, stat.S_IWRITE | stat.S_IREAD)
    elif sys.platform == 'linux':
        os.system("sudo chattr -i " + item_path)
    else:
        raise Exception('Неопознанная операционная система')

    # os.chmod(item_path, 0o777)
    print('Успешно')


def check_attr_hidden(filepath):
    if not os.path.exists(filepath):
        raise FileExistsError

    if sys.platform == 'win32':
        result = is_hidden_on_win(filepath)
    elif sys.platform == 'linux':
        result = is_hidden_on_linux(filepath)
    else:
        raise Exception('Неопознанная операционная система')

    if result:
        print('Объект скрыт')
    else:
        print('Объект не скрыт')


def is_hidden_on_win(filepath):
    if os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
        return True
    return False


def is_hidden_on_linux(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    if name.startswith('.'):
        return True
    return False


if __name__ == '__main__':

    menu = -1
    while menu != "0":
        try:
            print_menu()
            menu = input("Выберите пункт меню: ")

            if menu == "0":
                print("Пока")
            elif menu == '1':
                path = input("Введите путь: ")
                print()
                print_dir(path)
                print()
            elif menu == '2':
                path = input("Введите путь: ")
                create_file(path)
                print()
            elif menu == '3':
                pathFrom = input("Введите путь до файла: ")
                pathTo = input("Введите конечный путь: ")
                copy_file(pathFrom, pathTo)
                print()
            elif menu == '4':
                path = input("Введите путь: ")
                delete_item(path)
                print()
            elif menu == '5':
                pathFrom = input("Введите путь до объекта: ")
                pathTo = input("Введите конечный путь: ")
                move_dir(pathFrom, pathTo)
                print()
            elif menu == '6':
                path = input("Введите путь: ")
                set_attr_readonly(path)
                print()
            elif menu == '7':
                path = input("Введите путь: ")
                unset_attr_readonly(path)
                print()
            elif menu == '8':
                path = input("Введите путь: ")
                check_attr_hidden(path)
                print()
            else:
                print('Повторите ввод\n')
        except FileExistsError:
            print('Данный файл/директория не существует\n')
        except:
            print('Что-то пошло не так...\n')
