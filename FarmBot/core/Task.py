# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
from utilities.utilities import getConfig


class Task:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def get_tasks(self):
        try:
            response = self.http.get(
                url="/mining/taskExecuting",
                domain="bot",
                valid_option_response_code=200,
            )

            if response is None:
                self.log.error(f"<r>⭕ {self.account_name} failed to get tasks!</r>")
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to get tasks!</r>")
            return None

    def check_daily_reward(self):
        try:
            tasks = self.get_tasks()
            for task in tasks["tasks"]["daily"]:
                if task["code"] == "dailyReward" and task["doneAmount"] == 0:
                    self.claim_daily_rewards()
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to check daily rewards!</r>")
            return None

    def claim_daily_rewards(self):
        try:
            response = self.http.post(
                url="/boost/activateDailyBoost",
                domain="bot",
                valid_option_response_code=200,
            )
            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to claim daily rewards!</r>"
                )
                return None
            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to claim daily rewards!</r>")
            return None

    async def check_subscription(self, tgAccount=None):
        try:
            tasks = self.get_tasks()
            for task in tasks["tasks"]["subscriptions"]:
                if task["code"] == "subscriptionTwitter":
                    if task["doneAmount"] == 0:
                        self.confirm_subscription("twitter")
                elif task["code"] == "subscription":
                    if task["doneAmount"] == 0 and tgAccount is not None:
                        if getConfig("join_pocketfi", False):
                            await tgAccount.joinChat("pocketfi")
                        self.confirm_subscription("telegram")
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to check subscription tasks!</r>")
            return None

    def confirm_subscription(self, platform):
        if platform is None:
            return None
        try:
            response = self.http.post(
                url="/confirmSubscription",
                domain="bot",
                data=json.dumps({"subscriptionType": platform}),
                valid_option_response_code=200,
                only_json_response=False,
            )
            if response is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to confirm subscription!</r>"
                )
                return None
            return response
        except Exception as e:
            self.log.error(f"<r>⭕ {e} failed to confirm subscription!</r>")
            return None
