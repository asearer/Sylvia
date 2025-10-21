import pytest
from unittest.mock import patch, MagicMock
import types
from experiments.dashboards.metrics_dashboard import MatrixDashboard

class DummyRoom:
    display_name = 'TestRoom'

def test_event_callback_handles_metrics(capsys):
    dashboard = MatrixDashboard('hs','user','pw','room')
    event = MagicMock()
    event.body = '{"epoch":1,"accuracy":0.9,"loss":0.1}'
    dashboard._event_callback = types.MethodType(MatrixDashboard._event_callback, dashboard)
    # Run as normal function since it's async
    import asyncio
    asyncio.run(dashboard._event_callback(DummyRoom(), event))
    out = capsys.readouterr().out
    assert 'Type=' in out and 'TestRoom' in out

def test_event_callback_handles_parse_error(capsys):
    dashboard = MatrixDashboard('hs','user','pw','room')
    event = MagicMock()
    del event.body
    dashboard._event_callback = types.MethodType(MatrixDashboard._event_callback, dashboard)
    import asyncio
    asyncio.run(dashboard._event_callback(DummyRoom(), event))
    out = capsys.readouterr().out
    assert 'Error parsing event' in out
