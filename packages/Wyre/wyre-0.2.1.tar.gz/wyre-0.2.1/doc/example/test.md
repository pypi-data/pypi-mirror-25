# An example of unit test on your app

First, the imports.

```python
from unittest.mock import Mock
from doc.example import Greetings, Meeting
```

The the unit test - here using pytest.
The test consists in three distinct parts :
* `# given` : creates a mock and injects it in your `Meeting` app.
* `# when` : a single call to the `say_hello` function of your app.
* `# then` : an assertion on what result is expected from the previous call.

As expected, the behavior of `say_hello` matches what was defined on your mock !

```python
def test_say_hello_with_a_mocked_greetings_dependency():
    # given
    mocked_greetings = Mock(spec=Greetings)
    mocked_greetings.hello.return_value = 'Coucou'
    meeting = Meeting('fr', smiley=':-D', greetings=mocked_greetings)
    print(meeting.greetings_service)

    # when
    result = meeting.say_hello()

    # then
    assert result == 'Coucou Bob ! :-D'
```
