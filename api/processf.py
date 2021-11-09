import logging
import requests
import json
import csv
import os
from api.vk import Vk


logger = logging.getLogger("app/api/processf")


def parse_friend_list(user_id: int, file_format: str = "csv", report_to: str = "report") -> None:
    logger.info("Starting parsing session...")

    file_path: str = f"{report_to}.{file_format}"
    keys: dict = {
        "first_name": "Имя",
        "last_name": "Фамилия",
        "country": "Страна",
        "city": "Город",
        "bdate": "Дата рождения",
        "sex": "Пол",
        "sex-data": {
            1: "Женский",
            2: "Мужской"
        }
    }
    fields: list = list(keys.keys())[:-1]
    friends: dict = {}
    friend_list: list = []
    try:
        friends = Vk.friend_list(user_id, fields[2:])
        logger.info("API-request was done correctly")
        friend_list = friends['response']['items']
    except requests.HTTPError as http_err:
        print(f"Ошибка при обработке данных: {http_err}.")
        logger.error(http_err)
    except KeyError:
        print(f"Ошибка: '{friends['error']['error_msg']}'")
        logger.exception(KeyError)

    output: list = []
    for i in friend_list:
        logger.debug(f"Processing the item with index {friend_list.index(i)} in 'friend_list'")
        output_tmp: dict = {}
        for j in fields:
            logger.debug(f"Creating field with key name {j}")
            if j in i:
                if (j == "country") or (j == "city"):
                    output_tmp[keys[j]] = i[j]["title"]
                elif j == "sex":
                    output_tmp[keys[j]] = keys["sex-data"][i[j]]
                else:
                    output_tmp[keys[j]] = i[j]
                logger.debug(f"Field received value equals {output_tmp[keys[j]].encode('utf-8')}")
            else:
                output_tmp[keys[j]] = None
                logger.debug(f"Field received value equals None")
        output.append(output_tmp)
        logger.debug("Ending processing of the item")
        del output_tmp
    logger.info("'friend_list' list was successfully processed")

    logger.info("Creating directory...")
    if not os.path.exists(os.path.split(file_path)[0]) and os.path.split(file_path)[0] != '':
        os.makedirs(os.path.split(file_path)[0])
    logger.info("Directory was created or it is already exists")

    logger.info("Starting writing into a file session...")
    with open(file_path, "w", encoding="utf-8", newline="", errors="ignore") as file:
        logger.debug(f"File {os.path.split(file_path)[1]} was recreated")
        if file_format == "json":
            json.dump(output, file, indent=4, ensure_ascii=False)
        elif file_format == "csv" or file_format == "tsv":
            determiner: dict = {"csv": ",", "tsv": "\t"}
            j = csv.DictWriter(file, fieldnames=[keys[n] for n in fields], delimiter=determiner[file_format])
            j.writeheader()
            j.writerows(output)
        logger.debug(f"File {os.path.split(file_path)[1]} was updated")
        logger.info("Closing file...")
    logger.info("Ending writing session...")

    print(f"Файл '{file_path}' был создан!")
