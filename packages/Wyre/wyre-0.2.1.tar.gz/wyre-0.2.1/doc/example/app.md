# Some sample app to walk you through Wyre

First you need to import the decorator `@inject`

```python
from wyre import inject
```

The you define the classes of your app. :
* `Translations` : a repository that returns a translated word given a language identifier.
* `Greetings` : a service that wraps the repository and returns a greeting word given a language identifier.
* `Friend` : a plain value type that models a someone and his name.
* `Meeting` : the app entry point. Requires a language identifier and instances of Greetings and Friend to work.

```python
class Translations:
    i18n = {'fr': 'Salut', 'en': 'Hello', 'it': 'Ciao'}

    def get_for(self, lang):
        return self.i18n[lang]


class Greetings:
    @inject
    def __init__(self, translations=Translations):
        self.translations_service = translations

    def hello(self, language):
        return self.translations_service.get_for(language)


class Friend:
    def get_name(self):
        return 'Bob'


class Meeting:
    @inject
    def __init__(self, lang, smiley=':-p', greetings=Greetings, friend=Friend):
        self.lang = lang
        self.greetings_service = greetings
        self.friend_service = friend
        self.smiley = smiley

    def say_hello(self):
        hello = self.greetings_service.hello(language=self.lang)
        friend = self.friend_service.get_name()
        return '%s %s ! %s' % (hello, friend, self.smiley)
```

Finally, we can create a new meeting instance with a language identifier and a smiley. Instances of dependencies will
be automatically injected through `__init__`.

```python
app = Meeting('en', smiley=':-)')

# prints 'Hello Bob ! :-)'
print(app.say_hello())
```
