import logging
import re

import discord

from bot_utils import get_id
from channels import DRONE_HIVE_CHANNELS
from roles import DRONE, ENFORCER_DRONE, has_role
from speech_optimization import plain_status_code_pattern, informative_status_code_pattern

LOGGER = logging.getLogger('ai')

class Identity_Enforcer():

    def __init__(self, bot):
        self.bot = bot
        self.on_message = [self.enforce_identity]
        self.on_ready = [self.report_online]
        self.channels_whitelist = DRONE_HIVE_CHANNELS
        self.channels_blacklist = []
        self.roles_whitelist = [DRONE, ENFORCER_DRONE]
        self.roles_blacklist = []
        self.ENFORCER_AVATAR = "https://images.squarespace-cdn.com/content/v1/5cd68fb28dfc8ce502f14199/1586799510064-SOAGMV8AOH0VEMXDPDPE/ke17ZwdGBToddI8pDm48kDaNRrNi77yKIgWxrt8GYAFZw-zPPgdn4jUwVcJE1ZvWhcwhEtWJXoshNdA9f1qD7WT60LcluGrsDtzPCYop9hMAtVe_QtwQD93aIXqwqJR_bmnO89YJVTj9tmrodtnPlQ/Enforcer_Drone.png"
        self.DRONE_AVATAR = "https://images.squarespace-cdn.com/content/v1/5cd68fb28dfc8ce502f14199/1586799484353-XBXNJR1XBM84C9YJJ0RU/ke17ZwdGBToddI8pDm48kLxnK526YWAH1qleWz-y7AFZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVFUQAah1E2d0qOFNma4CJuw0VgyloEfPuSsyFRoaaKT76QvevUbj177dmcMs1F0H-0/Drone.png"
        self.informative_status_code_regex = re.compile(informative_status_code_pattern)
        self.plain_status_code_regex = re.compile(plain_status_code_pattern)

    async def send_webhook(self, message: discord.Message, webhook: discord.Webhook):
        if has_role(message.author, ENFORCER_DRONE):
            await webhook.send(message.content, username="⬢-Drone #"+get_id(message.author.display_name), avatar_url=self.ENFORCER_AVATAR)
        else:
            await webhook.send(message.content, username="⬡-Drone #"+get_id(message.author.display_name), avatar_url=self.DRONE_AVATAR)
    
    def check_is_status_code(self, message):
        return self.informative_status_code_regex.match(message.content) or self.plain_status_code_regex.match(message.content)

    async def enforce_identity(self, message: discord.Message):
        if not self.check_is_status_code(message):
            webhooks = await message.channel.webhooks()
            if len(webhooks) == 0:
                webhooks = [await message.channel.create_webhook(name="Identity Enforcement Webhook", reason="Webhook not found for channel.")]
            await message.delete()
            await self.send_webhook(message, webhooks[0])
        return False
    
    async def report_online(self):
        LOGGER.info("Identity enforcer online.")
