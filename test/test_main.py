import unittest
from unittest.mock import AsyncMock, patch

import main
import channels
from roles import HIVE_MXTRESS


class MainTest(unittest.IsolatedAsyncioTestCase):

    @patch("main.has_role")
    @patch("main.mantra_handler")
    async def test_repeat(self, mantra_handler, has_role):
        # setup
        context = AsyncMock()
        context.channel.name = channels.REPETITIONS

        has_role.return_value = True

        mantra_handler.update_mantra = AsyncMock()

        # run
        await main.repeat(context, "beep", "boop")

        # assert
        has_role.assert_called_once_with(context.author, HIVE_MXTRESS)
        mantra_handler.update_mantra.assert_called_once_with(context.message, ("beep", "boop"))
