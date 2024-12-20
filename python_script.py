import argparse
import os
import datetime
import subprocess
import sys


def run_command(command):
    """Выполняет команду и выводит результат."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description='Prepare a pre-production git branch.')
    parser.add_argument('--branch-test', required=True, help='Имя ветки для слияния (например, test_merge).')
    parser.add_argument('--stage', required=True, choices=['prod', 'test'], help='Укажите значение prod или test.')
    args = parser.parse_args()

    # Подготовка ветки предрелиза
    # print("# Prepare a pre-production git branch")
    run_command("git checkout master")
    run_command("git pull")
    run_command("git checkout prod_trading")
    run_command("git pull")

    # Проверка наличия переменной окружения PRE_PROD_BRANCH
pre_prod_branch = os.getenv('PRE_PROD_BRANCH')
if not pre_prod_branch:
    print("Ошибка: переменная PRE_PROD_BRANCH не задана.")
    exit(1)

# Функция для выполнения команд в терминале
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Ошибка при выполнении команды: {command}")
        print(result.stderr)
        exit(1)

# Слияние с основной веткой master
run_command("git merge master")

# Получение текущей локальной даты и времени в формате "ГГГГММДД_ЧЧММСС"
current_local_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

# Коммит с сообщением о слиянии
commit_message = f"merge master {current_local_datetime}"
run_command(f"git commit -m '{commit_message}'")

# Отправка изменений в удаленный репозиторий
run_command(f"git push --set-upstream origin {pre_prod_branch}")

    # Ввод имени пользователя
your_name = input("Введите ваше имя: ")
if not your_name:
        print("error")
        sys.exit(1)
print(your_name)

    # Задаем значение task_definition в зависимости от stage
if args.stage == "prod":
        task_definition = "cmamp-test-tokyo-full-system"
elif args.stage == "test":
        task_definition = "cmamp-test-tokyo-full-system-preprod"
    
print(task_definition)

    # Переход на созданную ветку
os.chdir(os.path.expanduser("~/src/orange1/amp"))
run_command(f"git checkout {PRE_PROD_BRANCH}")
run_command("git pull")

    # Переход на prod_trading
os.chdir(os.path.expanduser("~/src/orange1"))
run_command("git checkout prod_trading")
run_command("git pull")

    # Создание образа кандидата
run_command(f"docker_create_candidate_image --task-definition {task_definition} --user-tag {your_name} --region ap-northeast-1")

    # Переключаемся на главную ветку
BRANCH_MAIN = "main"
run_command(f"git checkout {BRANCH_MAIN}")

    # Пытаемся слить ветку test_merge
try:
        run_command(f"git merge {args.branch_test}")
        print("Слияние прошло успешно!")
except SystemExit:
        print("Конфликт возник!")
        run_command("git status")  # Показать статус, чтобы увидеть конфликтные файлы

if __name__ == "__main__":
    main()