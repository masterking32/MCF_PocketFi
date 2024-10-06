# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import sys
import os
import time

from .core.HttpRequest import HttpRequest
from .core.Base import Base
from .core.Alliance import Alliance
from .core.Task import Task
from .core.Wallet import Wallet
from utilities.utilities import getConfig
from random import randint

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)

import mcf_utils.utils as utils


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

    async def run(self):
        self.log.info(
            f"<cyan>{self.account_name}</cyan> | <g>🤖 Farming is starting...</g>"
        )
        try:
            self.http = HttpRequest(
                self.log,
                self.proxy,
                self.user_agent,
                self.web_app_query,
                self.account_name,
            )
            base = Base(self.log, self.http, self.account_name)
            alliance = Alliance(self.log, self.http, self.account_name)
            task = Task(self.log, self.http, self.account_name)
            wallet = Wallet(self.log, self.http, self.account_name)

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
            _alliance = user_mining.get("alliance", None)

            if _alliance is not None:
                alliance.get(_alliance)
            else:
                alliance.join()

            wallets = wallet.getList()
            wallet.getKnownTokens()
            wallet.getTotalBalance()
            wallet.getTotalBalanceBoosted()

            self.log.info(
                f"<cyan>{self.account_name}</cyan> | <g>👾 Balance: {user_mining.get('gotAmount', 0)} $SWITCH - Alliance: {_alliance if _alliance else 'No Alliance'}</g>"
            )

            if wallets is not None and len(wallets) > 0:
                wallet = wallets[0]
                if wallet is not None:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan> | <g>💳 In-App ETH Address: {utils.hide_text(wallet.get('address', '0xNotFound'))}</g>"
                    )
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan> | <g>💳 In-App TON Address: {utils.hide_text(wallet.get('tonUnbouncableAddress', 'UQ_NotFound'))}</g>"
                    )
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan> | <g>🪙 In-App Wallet Balance: ${wallet.get('totalBalanceUsd', 0)}</g>"
                    )

            if user_mining.get("miningAmount", 0) >= 0.25:
                claimResult = base.claim_mining()
                if claimResult is not None:
                    self.log.info(
                        f"<cyan>{self.account_name}</cyan> | <g>⛏️ Mining rewards claimed for {user_mining['miningAmount']}</g>"
                    )

            dailyResult = task.check_daily_reward()

            if dailyResult is not None:
                self.log.info(
                    f"<cyan>{self.account_name}</cyan> | <g>🎯 Daily rewards claimed! Streak: {int(user_mining.get('streak', 0)) + 1}</g>"
                )

            task.check_subscription(self.tgAccount)

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
            if getConfig("random_sleep", False):
                sleepFor = randint(5, 30)
                self.log.info(f"<y>⏳ sleeping for {sleepFor} seconds...</y>")
                time.sleep(sleepFor)
