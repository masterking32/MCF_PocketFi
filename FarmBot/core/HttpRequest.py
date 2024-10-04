# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
import time
import requests


class HttpRequest:
    def __init__(
        self,
        log,
        proxy=None,
        user_agent=None,
        tgWebData=None,
        account_name=None,
    ):
        self.log = log
        self.proxy = proxy
        self.user_agent = user_agent
        self.game_url = {
            "gm": "https://gm.pocketfi.org",
            "bot": "https://bot.pocketfi.org",
            "rubot": "https://rubot.pocketfi.org",
        }
        self.tgWebData = tgWebData
        self.account_name = account_name

        if not self.user_agent or self.user_agent == "":
            self.user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.3"

        if "windows" in self.user_agent.lower():
            self.log.warning(
                "🟡 <y>Windows User Agent detected, For safety please use mobile user-agent</y>"
            )

    def get(
        self,
        url,
        domain="game",
        headers=None,
        send_option_request=True,
        valid_response_code=200,
        valid_option_response_code=204,
        return_headers=False,
        retries=3,
        display_errors=True,
    ):
        try:
            url = self._fix_url(url, domain)
            default_headers = (
                self._get_default_headers() if "pocketfi.orgs" in url else {}
            )

            if headers is None:
                headers = {}

            if self.tgWebData is not None:
                headers["telegramrawdata"] = self.tgWebData

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            if send_option_request:
                self.options(url, None, "GET", headers, valid_option_response_code)

            response = requests.get(
                url=url,
                headers=default_headers,
                proxies=self._get_proxy(),
            )

            if response.status_code != valid_response_code:
                if display_errors:
                    self.log.error(
                        f"🔴 <red> GET Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                    )
                return (None, None) if return_headers else None

            return (
                (response.json(), response.headers)
                if return_headers
                else response.json()
            )
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send request, retrying...</y>")
                time.sleep(0.5)
                if domain == "bot":
                    domain = "rubot"
                elif domain == "rubot":
                    domain = "bot"
                return self.get(
                    url,
                    domain,
                    headers,
                    send_option_request,
                    valid_response_code,
                    valid_option_response_code,
                    auth_header,
                    return_headers,
                    retries - 1,
                    display_errors,
                )
            if display_errors:
                self.log.error(f"🔴 <red> GET Request Error: <y>{url}</y> {e}</red>")
            return (None, None) if return_headers else None

    def post(
        self,
        url,
        domain="game",
        data=None,
        headers=None,
        send_option_request=True,
        valid_response_code=200,
        valid_option_response_code=204,
        return_headers=False,
        retries=3,
        only_json_response=True,
    ):
        try:
            url = self._fix_url(url, domain)
            default_headers = (
                self._get_default_headers() if "pocketfi.orgs" in url else {}
            )

            if headers is None:
                headers = {}

            if self.tgWebData is not None:
                headers["telegramrawdata"] = self.tgWebData

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            if send_option_request:
                self.options(url, None, "POST", headers, valid_option_response_code)
            response = None

            if data:
                response = requests.post(
                    url=url,
                    headers=default_headers,
                    data=data,
                    proxies=self._get_proxy(),
                )
            else:
                response = requests.post(
                    url=url,
                    headers=default_headers,
                    proxies=self._get_proxy(),
                )

            if response.status_code != valid_response_code:
                print(response.text)
                print(response.json())
                print(data)
                self.log.error(
                    f"🔴 <red> POST Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return (None, None) if return_headers else None

            if (
                "application/json" not in response.headers.get("Content-Type", "")
                and only_json_response is False
            ):
                return (
                    (response.text, response.headers)
                    if return_headers
                    else response.text
                )

            return (
                (response.json(), response.headers)
                if return_headers
                else response.json()
            )
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send request, retrying...</y>")
                time.sleep(0.5)
                if domain == "bot":
                    domain = "rubot"
                elif domain == "rubot":
                    domain = "bot"
                return self.post(
                    url,
                    domain,
                    data,
                    headers,
                    send_option_request,
                    valid_response_code,
                    valid_option_response_code,
                    return_headers,
                    retries - 1,
                )

            self.log.error(f"🔴 <red> POST Request Error: <y>{url}</y> {e}</red>")
            return (None, None) if return_headers else None

    def options(
        self,
        url,
        domain=None,
        method="POST",
        headers=None,
        valid_response_code=204,
        retries=3,
    ):
        try:
            url = self._fix_url(url, domain)
            default_headers = (
                self._get_get_option_headers(headers, method)
                if "pocketfi.org" in url
                else {}
            )

            if headers is None:
                headers = {}

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            response = requests.options(
                url=url,
                headers=default_headers,
                proxies=self._get_proxy(),
            )

            if response.status_code != valid_response_code:
                self.log.error(
                    f"🔴 <red> OPTIONS Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return None

            return True
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send option request, retrying...</y>")
                time.sleep(0.5)
                if domain == "bot":
                    domain = "rubot"
                elif domain == "rubot":
                    domain = "bot"
                return self.options(
                    url,
                    domain,
                    method,
                    headers,
                    valid_response_code,
                    retries - 1,
                )
            self.log.error(f"🔴 <red> OPTIONS Request Error: <y>{url}</y> {e}</red>")
            return None

    def _get_proxy(self):
        if self.proxy:
            return {"http": self.proxy, "https": self.proxy}

        return None

    def _fix_url(self, url, domain=None):
        if url.startswith("http") or domain is None:
            return url

        game_url = self.game_url.get(domain)
        if not game_url:
            return url

        if url.startswith("/"):
            return f"{game_url}{url}"

        return f"{game_url}/{url}"

    def _get_default_headers(self):
        headers = {
            "accept": "application/json",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": self.user_agent,
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "Content-Type": "application/json",
            "X-Paf-T": "Abvx2NzMTM==",
        }

        if "android" in self.user_agent.lower():
            headers["Sec-CH-UA-Platform"] = '"Android"'
            headers["Sec-CH-UA-Mobile"] = "?1"
            headers["Sec-CH-UA"] = (
                '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"'
            )
            headers["X-Requested-With"] = "org.telegram.messenger"

        return headers

    def _get_get_option_headers(self, headers=None, method="GET"):
        default_headers = {
            "Accept": "*/*",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": self.user_agent,
            "pragma": "u=1, i",
            "cache-control": "no-cache",
            "access-control-request-method": method,
            "access-control-request-headers": "x-paf-t",
        }

        if not headers:
            return default_headers

        if "telegramrawdata" in headers:
            default_headers["access-control-request-headers"] = (
                default_headers["access-control-request-headers"] + ",telegramrawdata"
            )

        return default_headers
