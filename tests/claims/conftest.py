def pytest_configure(config):
    config.addinivalue_line("markers", "live: calls the Claude Code CLI model; runs only with RC_LIVE=1")
