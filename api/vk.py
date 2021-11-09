import requests


class Vk:
    _api_base_endpoint: str = "https://api.vk.com"
    _headers: dict[str, str] = {"Access": "application/json"}
    _user_api_key: str = ...

    @classmethod
    def key(cls, user_key: str):
        cls._user_api_key = user_key

    @classmethod
    def friend_list(cls, user_id: int, fields: list) -> dict:
        route: str = "/method/friends.get"
        args = f"?user_id={user_id}&order=name&fields={','.join(fields)}&access_token={cls._user_api_key}&v=V"

        response = requests.get(f"{cls._api_base_endpoint}{route}{args}", headers=cls._headers)
        response.raise_for_status()
        res: dict = response.json()

        return res
