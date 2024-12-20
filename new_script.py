#!/usr/bin/python3

import argparse
import os
import datetime
import subprocess
import sys

# Добавление аргументов
def get_args_from_cmd():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--stage', choices=['prod', 'test'], required=True, help='Нужно выбрать prod or test')
    parser.add_argument('--your_name', required=True, help='Text your name')
    args = parser.parse_args()
    return args

def create_preprod_branch() -> str:
    # Prepare a pre-production git branch
    # E.g., pre_prod.scheduled_trading.20240512
    subprocess.run("git checkout master", shell=True)
    subprocess.run("git pull", shell=True)
    # Branch from prod_trading.
    subprocess.run("git checkout prod_trading", shell=True)
    subprocess.run("git pull", shell=True)
    current_date = datetime.datetime.now()
    current_date = current_date.strftime("%Y%m%d")
    pre_prod_branch_name = f'pre_prod.scheduled_trading.{current_date}'
    # pre_prod.scheduled_trading.20241217
    subprocess.run(f"git checkout -b {pre_prod_branch_name}", shell=True)
    return pre_prod_branch_name

def update_preprod_branch(pre_prod_branch_name: str) -> None:
    subprocess.run("git merge master", shell=True)
    # UTC timestamp in the commit message is just a cosmetic feature that simplifies the
    # navigation.
    current_utc_datetime = datetime.datetime.now(datetime.utc)
    current_utc_datetime = current_utc_datetime.strftime("%Y%m%d_%H%M%S")
    subprocess.run(f"git commit -m 'merge master {current_utc_datetime}'", shell=True)
    subprocess.run(f"git push --set-upstream origin {pre_prod_branch_name}", shell=True)

def merge_conflict() ->None:
    branch_main = "master"
    branch_name = "git symbolic-ref --short HEAD"
    # branch_test = subprocess.run("git merge 'указать ветку", shell=True)

    # Переключаемся на главную ветку
    subprocess.run(f"git checkout {branch_main}", shell=True)
    subprocess.run("git pull -- update master", shell=True)
    # -- go back to the prev branch
    subprocess.run(f"git checkout {branch_name}", shell=True)
    subprocess.run("git merge master", shell=True)
    
    # Пытаемся слить ветку test_merge
    if not branch_test:
        print("Конфликт возник!")
        raise ValueError ("error")
    else:
        print("Слияние прошло успешно!")

    subprocess.run("git status ", shell=True) # Показать статус, чтобы увидеть конфликтные файлы

def create_preprod(stage, your_name, pre_prod_branch_name) -> None:
    if not your_name:
        print ("error")
        raise ValueError ("Введите значение")
    if stage == "prod":
        task_definition = "cmamp-test-tokyo-full-system"
    elif stage == "test":
        task_definition = "cmamp-test-tokyo-full-system-preprod"
    else:
        print ("error")
        raise ValueError ("Введите значение")

    os.chdir("~/src/orange1/amp")
    subprocess.run(f"git checkout {pre_prod_branch_name}", shell=True)
    subprocess.run("git pull", shell=True)
    os.chdir("~/src/orange1")
    subprocess.run("git checkout prod_trading", shell=True)
    subprocess.run("git pull", shell=True)
    # The task definition name is stable while the user tag depends on who runs the cmd.
    # ( "ygjhgu"
    #   "hghgfyt"   )
    subprocess.run(f'i docker_create_candidate_image --task-definition {task_definition} --user-tag {your_name} --region "ap-northeast-1"')



def main():
    if __name__ == "__main__":
        main()