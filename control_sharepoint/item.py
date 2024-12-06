import json
import requests

from graph_auth import read_token
from graph_auth import ApiError


class Item:
    def __init__(self, site_id: str, path: str):
        """
        コンストラクタ

        Params
        -------
        site_id: str
            SharePointのサイトID
        path: str
            ファイルまでのパス
        """
        for k, v in self.get_item(site_id, path).items():
            setattr(self, k, v)

    def get_item(self, site_id: str, path: str) -> dict:
        """
        アイテム情報を取得する

        Params
        -------
        site_id: str
            SharePointのサイトID
        path: str
            ファイルまでのパス(ex. /General/Path/to/file)
        """
        # リクエスト先設定
        header = {"Authorization": f"Bearer {read_token()}"}
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:{path}"

        # APIの実行
        response = requests.get(url, headers=header)

        # レスポンスのチェック
        if response.status_code != 200:
            raise ApiError(response)

        return json.loads(response._content.decode("utf-8"))

    def download(self, dest_path: str):
        """
        ファイルをダウンロードする

        """
        # リクエスト先設定
        header = {"Authorization": f"Bearer {read_token()}"}
        url = f"https://graph.microsoft.com/v1.0/sites/{self.parentReference['siteId']}/drive/items/{self.id}/content"

        # APIの実行
        response = requests.get(url, headers=header)

        # レスポンスのチェック
        if response.status_code != 200:
            raise ApiError(response)

        # ファイルの保存
        with open(f"{dest_path}/{self.name}", "wb") as f:
            f.write(response._content)
