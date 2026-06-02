import asyncio
import importlib
import os
import unittest
from unittest.mock import patch


class FakeResponse:
    def __init__(self, events):
        self._events = events

    async def defer(self, thinking=True):
        self._events.append(("defer", thinking))


class FakeFollowup:
    def __init__(self, events):
        self._events = events

    async def send(self, message):
        self._events.append(("send", message))


class FakeInteraction:
    def __init__(self):
        self.events = []
        self.response = FakeResponse(self.events)
        self.followup = FakeFollowup(self.events)


class MenuCommandTest(unittest.TestCase):
    def test_menu_defers_before_fetching_menu(self):
        os.environ.setdefault("DISCORD_TOKEN", "test-token")
        os.environ.setdefault("DISCORD_GUILD_ID", "123")
        main = importlib.import_module("main")
        interaction = FakeInteraction()

        def fake_get_menu(date):
            interaction.events.append(("fetch", date))
            return [["Soup", "1 kcal", "0 g", "0 g", "0 g"]]

        async def run_test():
            with patch.object(main, "get_menu", fake_get_menu):
                await main.menu.callback(interaction, "2026-06-02")

        asyncio.run(run_test())

        self.assertEqual(interaction.events[0], ("defer", True))
        self.assertEqual(interaction.events[1], ("fetch", "2026-06-02"))
        self.assertEqual(interaction.events[2][0], "send")


if __name__ == "__main__":
    unittest.main()
