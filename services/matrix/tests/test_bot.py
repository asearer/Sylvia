import pytest
from unittest.mock import patch, MagicMock
import types
from services.matrix.src.bot import MatrixOrchestrationBot

class DummyRoom:
    display_name = 'TestBotRoom'

@patch('services.matrix.src.bot.trigger_ml_job')
def test_bot_handles_train_cmd(mock_trigger):
    bot = MatrixOrchestrationBot('hs','user','pw','room')
    event = MagicMock()
    event.body = '!train'
    bot._on_event = types.MethodType(MatrixOrchestrationBot._on_event, bot)
    import asyncio
    asyncio.run(bot._on_event(DummyRoom(), event))
    mock_trigger.assert_called_once()

def test_bot_ignores_other_cmd():
    bot = MatrixOrchestrationBot('hs','user','pw','room')
    event = MagicMock()
    event.body = '!somethingelse'
    bot._on_event = types.MethodType(MatrixOrchestrationBot._on_event, bot)
    import asyncio
    asyncio.run(bot._on_event(DummyRoom(), event))
    # No exception or workflow triggered
