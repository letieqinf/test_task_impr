import api.processf as parser
from api.vk import Vk
import os
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs.log")
    ]
)


logger = logging.getLogger("main")


def main() -> None:
    # 4415d53912385bbfd695e474845a02b0012671e5832cabc83157176e8283f06c179c9e5a2c0bae73722a5
    # 280227576 366597812

    Vk.key(input("Введите ваш API-ключ: "))
    logger.debug(f"API-key was received")
    formats: list[str, str, str] = ["csv", "json", "tsv"]
    file_format: str = formats[0]
    repos: str = "report"
    user_id: int = -1

    switch: bool = True
    while switch:
        print("Настройте параметры в соответствии с вашими требованиями:")
        choice: int = int(input("1. User ID (обяз.)\n"
                                "2. Формат выходного файла (по умолч. csv)\n"
                                "3. Путь к выходному файлу (по умолч. текущий каталог)\n"
                                "4. Продолжить\n"
                                "- "))
        if choice == 1:
            user_id = int(input("ID: "))
            logger.debug(f"'user_id' parameter was set to {user_id}")
            os.system("cls")
        elif choice == 2:
            print("Программа предусматривает экспорт в следующие форматы: csv, json и tsv")
            file_format = input("Формат: ")
            logger.debug(f"'file_format' parameter was set to {file_format}")
            os.system("cls")
        elif choice == 3:
            repos = input("Файл: ")
            logger.debug(f"'repos' parameter was set to {repos}")
            os.system("cls")
        elif choice == 4:
            if file_format not in formats:
                print("Формат не поддерживается, поэтому был установлен параметр по умолчанию")
                file_format = formats[0]
                logger.warning("'file_format' parameter was set to a inappropriate value")
            if user_id <= 0:
                print("ID пользователя недействителен")
                logger.warning("'user_id' parameter was set to a inappropriate value")
                os.system("cls")
            else:
                parser.parse_friend_list(user_id, file_format=file_format, report_to=repos)
                switch = False
        else:
            os.system("cls")


if __name__ == "__main__":
    logger.info("Starting service...")
    main()
    logger.info("Stopping service...")

