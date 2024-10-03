# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class Base:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

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

    def claim_daily_rewards(self):
        try:
            response = self.http.get(
                url="/mining/taskExecuting",
                domain="bot",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to claim daily rewards!</r>"
                )
                return None
            for task in response["tasks"]["daily"]:
                if task["code"] == "dailyReward":
                    # TODO
                    if task["currentDay"] == 0:
                        _response = self.http.post(
                            url="/boost/activateDailyBoost",
                            domain="bot",
                            valid_option_response_code=200,
                        )
                        if _response is None:
                            self.log.error(
                                f"<r>⭕ {self.account_name} failed to claim daily rewards!</r>"
                            )
                            return None
                        return _response
            return None
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to claim daily rewards!</r>")
            return None

    def join_alliance(self):
        try:
            response = self.http.post(
                url="/mining/alliances/set?alliance=pocketfi",
                domain="gm",
                valid_option_response_code=200,
            )
            # No response means success
            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to join alliance!</r>")
            return None

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
