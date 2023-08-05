from watchm8.actions.say import Event


def test_action_event():
    a = Event()
    a({}, None)
