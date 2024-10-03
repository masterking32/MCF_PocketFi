# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import sys
import os
import time

from .core.HttpRequest import HttpRequest
from .core.Base import Base
from random import randint


MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)


class FarmBot:
    def __init__(
        self,
        log,
        bot_globals,
        account_name,
        web_app_query,
        proxy=None,
        user_agent=None,
        isPyrogram=False,
        tgAccount=None,
    ):
        self.log = log
        self.bot_globals = bot_globals
        self.account_name = account_name
        self.web_app_query = web_app_query
        self.proxy = proxy
        self.user_agent = user_agent
        self.isPyrogram = isPyrogram
        self.tgAccount = tgAccount
        self.http = None

    async def run(self):
        self.log.info(
            f"<cyan>{self.account_name}</cyan> | <g>🤖 Farming is starting...</g>"
        )

        # If self.tg is not None, it means you can use Pyrogram...
        # self.log.info(
        #     f"<blue>[Development Only] URL: <c>{self.web_app_query}</c></blue>"
        # )
        try:
            # Login and other codes here ...
            self.http = HttpRequest(
                self.log,
                self.proxy,
                self.user_agent,
                self.web_app_query,
                self.account_name,
            )
            base = Base(self.log, self.http, self.account_name)
            user_mining = base.get_user_mining()
            if user_mining is None:
                self.log.error(
                    f"<r>⭕ {self.account_name} failed to get user mining!</r>"
                )
                return
            if user_mining.get("userMining", None) is None:
                registerResult = base.register_new_account()
                if registerResult is not None:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan> | <g>🐣 Registered new account!</g>"
                    )
                    time.sleep(5)
                    user_mining = base.get_user_mining()
                    if user_mining is None:
                        self.log.error(
                            f"<r>⭕ {self.account_name} failed to get user mining!</r>"
                        )
                        return

            user_mining = user_mining.get("userMining", {})
            self.log.info(
                f"<cyan>{self.account_name}</cyan> | <g>👾 Balance: {user_mining.get('gotAmount', 0)} - Alliance: {user_mining.get('alliance', 'No alliance')}</g>"
            )
            if user_mining.get("alliance", None) is None:
                base.join_alliance()
            if user_mining.get("miningAmount", 0) >= 0.25:
                claimResult = base.claim_mining()
                if claimResult is not None:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan> | <g>⛏️ Mining rewards claimed for {user_mining['miningAmount']}</g>"
                    )
            dailyResult = base.claim_daily_rewards()
            if dailyResult is not None:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan> | <g>🎯 Daily rewards claimed</g>"
                )
            self.log.info(
                f"<cyan>{self.account_name}</cyan> | <g>🤖 Farming is done.</g>"
            )
        except Exception as e:
            self.log.error(
                f"<cyan>{self.account_name}</cyan> | <r>⭕ failed to run!</r>"
            )
            self.log.error(
                f"<cyan>{self.account_name}</cyan> | <r>⭕ Error (For devs): {e}</r>"
            )
            return
        finally:
            sleepFor = randint(5, 30)
            self.log.info(f"<y>⏳ sleeping for {sleepFor} seconds...</y>")
            time.sleep(sleepFor)
