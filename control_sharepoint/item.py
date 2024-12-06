import json
import requests
from os.path import basename

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
            ファイルorディレクトリまでのパス
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
            ファイルorディレクトリまでのパス(ex. /General/Path/to/file)
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

    def upload(self, file_path: str):
        """
        ファイルをアップロードする

        Params
        -------
        file_path: str
            アップロードするファイルのパス
        dist_path: str
            アップロード先ディレクトリのパス(ex. /General/Path/to/dist)
        """
        # リクエスト先設定
        header = {"Authorization": f"Bearer {read_token()}"}
        url = f"https://graph.microsoft.com/v1.0/sites/{self.parentReference['siteId']}/drive/items/{self.id}:/{basename(file_path)}:/content"

        # APIの実行
        with open(file_path, "rb") as f:
            response = requests.put(url, headers=header, data=f)

        # レスポンスのチェック
        if response.status_code not in [200, 201]:
            print(response.status_code)
            raise ApiError(response)

        return json.loads(response._content.decode("utf-8"))
