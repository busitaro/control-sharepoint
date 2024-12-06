import json
import requests

from graph_auth import read_token
from graph_auth import ApiError


class Site:
    def __init__(self, hostname: str, path: str):
        """
        コンストラクタ

        Params
        -------
        hostname: str
            ホスト名 (ex: ~.sharepoint.com)
        path: str
            サイトへのパス (ex: /sites/site_name)
        """
        for k, v in self.get_site(hostname, path).items():
            setattr(self, k, v)

    def get_site(self, hostname: str, path: str):
        """
        サイト情報を取得する

        Params
        -------
        hostname: str
            ホスト名 (ex: ~.sharepoint.com)
        path: str
            サイトへのパス (ex: /sites/site_name)
        """
        # リクエスト先設定
        header = {"Authorization": f"Bearer {read_token()}"}
        url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/{path}"

        # APIの実行
        response = requests.get(url, headers=header)

        # レスポンスのチェック
        if response.status_code != 200:
            raise ApiError(response)

        return json.loads(response._content.decode("utf-8"))
