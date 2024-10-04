# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json


class Wallet:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def getList(self):
        try:
            response = self.http.get(
                url="/tgUserWallets",
                domain="rubot",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get user wallets!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get user wallets!</r>")
            return None

    def getKnownTokens(self):
        try:
            response = self.http.post(
                url="/knownTokens",
                domain="rubot",
                data=json.dumps(
                    {"chainId": "TON", "sliceProps": {"limit": 20, "offset": 0}}
                ),
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get known tokens!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get known tokens!</r>")
            return None

    def getTotalBalanceBoosted(self):
        try:
            response = self.http.get(
                url="/totalBalance?boostNotification=1",
                domain="rubot",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get total balance (boosted)!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get total balance (boosted)!</r>")
            return None

    def getTotalBalance(self):
        try:
            response = self.http.get(
                url="/totalBalance?",
                domain="rubot",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get total balance!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get total balance!</r>")
            return None
