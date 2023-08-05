"""
Translation API

Usage :

```
import systranio

translation = systranio.Translation(API_KEY)
options = {'source': 'en' }
result = translation.text('traduction', 'fr', **options)
print(result)  # traduction
print(result.stats)  #  {"elapsed_time": 20, "nb_characters": 9, ...
```

"""
import json

from .api import BaseAPI

TEXT_ENDPOINT = '/translation/text/translate'
FILE_ENDPOINT = '/translation/file/translate'
API_VERSION_ENDPOINT = '/translation/apiVersion'
SUPPORTED_LANGUAGES_ENDPOINT = '/translation/supportedLanguages'
PROFILES_ENDPOINT = '/translation/profiles'


class TextTranslationResult(object):
    """
    Takes a text translation result (json) and makes it usable
    repr as the translation output
    """

    output = None
    detected_language = None
    detected_language_confidence = 0
    stats = {}

    def __init__(self, result: dict):
        """
        `output` is always there, but not the others
        So we try to politely set the values
        """
        self.output = result.get('output')
        self.detected_language = result.get('detectedLanguage')
        self.detected_language_confidence = result.get(
            'detectedLanguageConfidence')
        self.stats = result.get('stats')

    def __repr__(self) -> str:
        """
        The translated string
        """
        return self.output


class FileTranslationResult(object):
    """
    Takes a file translation result (a requests_toolbelt decoder.MultipartDecoder)
    and makes it usable repr as the translation output
    """

    output = None
    detected_language = None
    detected_language_confidence = 0
    stats = {}

    def __init__(self, result: tuple):
        """
        `output` is always there, but not the others
        So we try to politely set the values
        result is a tuple of multipart parts
        """
        for part in result:
            part_name = part.headers[b'part-name'].decode('utf-8')
            if part_name == 'stats':
                self.stats = json.loads(part.text)
            if part_name == 'output':
                self.output = part.text
            if part_name == 'detectedLanguage':
                language = json.loads(part.text)
                self.detected_language = language.get('detectedLanguage')
                self.detected_language_confidence = language.get(
                    'detectedLanguageConfidence')

    def __repr__(self) -> str:
        """
        The translated file
        """
        return self.output


class LanguagePairResult(object):
    """
    Takes a supported_languages result and makes it usable
    """

    source = None
    target = None
    profiles = {}

    def __init__(self, result: dict):
        """
        we try to politely set the values
        """
        self.source = result.get('source')
        self.target = result.get('target')
        self.profiles = result.get('profiles')

    def __str__(self) -> str:
        """
        A representation of the language pair : `source` → `target`
        """
        return '{} → {}'.format(self.source, self.target)


class ProfileResult(object):
    """
    Takes a profiles result and makes it usable
    """

    # pylint: disable=C0103
    id = None
    localization = {}
    name = None
    source = None
    target = None

    def __init__(self, result: dict):
        """
        we try to politely set the values
        """
        self.source = result.get('source')
        self.target = result.get('target')
        self.name = result.get('name')
        self.id = result.get('id')
        self.localization = result.get('localization')

    def __str__(self) -> str:
        """
        A string representation of the profile
        """
        return self.name


class Translation(BaseAPI):
    """
    Translation API model
    """

    optional_text_api_parameters = {
        'source': 'auto',
        'format': None,
        'profile': None,
        'with_source': False,
        'with_annotations': False,
        'with_dictionary': None,
        'with_corpus': None,
        'back_translation': False,
        'options': {},
        'encoding': 'utf-8'
    }

    optional_file_api_parameters = {
        'source': 'auto',
        'format': None,
        'profile': None,
        'with_source': False,
        'with_annotations': False,
        'with_dictionary': None,
        'with_corpus': None,
        'back_translation': False,
        'options': {},
        'encoding': 'utf-8',
        'async': False,
        'batch_id': None
    }

    def text(self, text, target: str, **kwargs) -> TextTranslationResult:
        """
        Translates a single `text` or a list of `text` into `target` language
        and returns a TextTranslationResult object or a list of TextTranslationResult
        @see `optional_text_api_parameters` and documentation for a list of valid parameters
        """
        parameters = self._update_parameters(self.optional_text_api_parameters,
                                             kwargs)
        self.payload.update(parameters)
        self.payload.update(input=text, target=target)
        response = self.post(TEXT_ENDPOINT)
        if isinstance(text, str):
            return TextTranslationResult(response['outputs'][0])
        results = []
        for result in response['outputs']:
            results.append(TextTranslationResult(result))
        return results

    def file(self, file, target: str, asynchronous=False,
             **kwargs) -> FileTranslationResult:
        """
        Translates a file into `target` language
        and returns a FileTranslationResult object or a request_id if async is True
        @see `optional_file_api_parameters` and documentation for a list of valid parameters
        """
        parameters = self._update_parameters(self.optional_file_api_parameters,
                                             kwargs)
        self.payload.update(parameters)
        self.payload.update(target=target, async=asynchronous)
        response = self.post(FILE_ENDPOINT, files={'input': file})
        if self.payload.get('async'):
            return response['requestId']
        return FileTranslationResult(response)

    def api_version(self) -> str:
        """
        Current version for translation apis
        """
        response = self.get(API_VERSION_ENDPOINT)
        return response['version']

    def supported_languages(self, source=None, target=None) -> list:
        """
        List of language pairs in which translation is supported.
        This list can be limited to a specific source language or target language.
        """
        self.payload.update(source=source, target=target)
        results = []
        response = self.get(SUPPORTED_LANGUAGES_ENDPOINT)
        for pair in response['languagePairs']:
            results.append(LanguagePairResult(pair))
        return results

    def profiles(self, source=None, target=None, profile_id=None) -> list:
        """
        List all available profiles for translation.
        """
        self.payload.update(source=source, target=target, id=profile_id)
        results = []
        response = self.get(PROFILES_ENDPOINT)
        for profile in response['profiles']:
            results.append(ProfileResult(profile))
        return results
