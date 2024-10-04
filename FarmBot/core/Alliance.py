# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class Alliance:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def join(self):
        try:
            response = self.http.post(
                url="/mining/alliances/set?alliance=pocketfi",
                domain="gm",
                valid_option_response_code=200,
                only_json_response=False,
            )
            # No response means success
            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to join alliance!</r>")
            return None

    def get(self, alliance):
        try:
            response = self.http.get(
                url=f"/mining/alliances/{alliance}",
                domain="gm",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(f"<r>⭕ {self.account_name} failed to get alliance!</r>")
                return None

            return response

        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get alliance!</r>")
            return None
