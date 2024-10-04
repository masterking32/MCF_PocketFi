# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class Base:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def register_new_account(self):
        try:
            response = self.http.post(
                url="/mining/createUserMining",
                domain="gm",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to register new account!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to register new account!</r>")
            return None

    def get_user_mining(self):
        try:
            response = self.http.get(
                url="/mining/getUserMining",
                domain="gm",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get user mining!</r>"
                )
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get user mining!</r>")
            return None

    def claim_mining(self):
        try:
            response = self.http.post(
                url="/mining/claimMining",
                domain="gm",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to claim mining rewards!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to claim mining rewards!</r>")
            return None
