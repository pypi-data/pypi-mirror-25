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
from datetime import datetime

from .api import BaseAPI

TEXT_ENDPOINT = '/translation/text/translate'

FILE_ENDPOINT = '/translation/file/translate'
FILE_STATUS_ENDPOINT = '/translation/file/status'
FILE_CANCEL_ENDPOINT = '/translation/file/cancel'
FILE_RESULT_ENDPOINT = '/translation/file/result'

API_VERSION_ENDPOINT = '/translation/apiVersion'
SUPPORTED_LANGUAGES_ENDPOINT = '/translation/supportedLanguages'
SUPPORTED_FORMATS_ENDPOINT = '/translation/supportedFormats'
PROFILES_ENDPOINT = '/translation/profiles'


class TextResult(object):
    """
    Takes a text translation result (json) and makes it usable
    repr as the translation output
    """

    output = None
    detected_language = None
    detected_language_confidence = 0.0
    stats = {}

    def __init__(self, result: dict):
        """
        `output` is always there, but not the others
        So we try to politely set the values
        """
        self.output = result.get('output')
        self.detected_language = result.get('detectedLanguage')
        self.detected_language_confidence = float(
            result.get('detectedLanguageConfidence', 0))
        self.stats = result.get('stats')

    def __repr__(self) -> str:
        """
        The translated string
        """
        return self.output


class FileResult(object):
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


class FileStatusResult(object):
    """
    Takes a file status call result (json)
    use success property to easily check translation status
    """

    batch_id = None
    cancelled = False
    created_at = 0
    expire_at = 0
    finished_at = 0
    finished_steps = 0
    total_steps = 0
    status = ''  # ['registered', 'import', 'started', 'pending', 'export', 'finished', 'error']
    description = ''

    def __init__(self, result: dict):
        """
        `status` is always there, but not the others
        So we try to politely set the values
        """
        self.status = result.get('status')
        self.batch_id = result.get('batchId')
        self.cancelled = True if result.get('cancelled') == 'true' else False
        # timestamps are from js @see https://stackoverflow.com/a/10286261
        self.created_at = datetime.fromtimestamp(
            result.get('createdAt') /
            1000) if result.get('createdAt') else None
        self.expire_at = datetime.fromtimestamp(
            result.get('expireAt') / 1000) if result.get('expireAt') else None
        self.finished_at = datetime.fromtimestamp(
            result.get('finishedAt') /
            1000) if result.get('finishedAt') else None
        self.finished_steps = result.get('finishedSteps')
        self.total_steps = result.get('totalSteps')
        self.description = result.get('description')

    @property
    def success(self) -> bool:
        """
        True if successful, False if failed or canceled, None if in progress
        """
        if self.status == 'error' or self.cancelled:
            return False
        if self.status == 'finished':
            return True
        return None

    def __str__(self) -> str:
        """
        return status
        """
        return self.status


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


class SupportedFormatResult(object):
    """
    Takes a format result and makes it usable
    """

    input = ''
    output = ''
    name = ''

    def __init__(self, result: dict):
        """
        we try to politely set the values
        """
        self.input = result.get('mimetypes').get('input')
        self.output = result.get('mimetypes').get('output')
        self.name = result.get('name')

    def __str__(self) -> str:
        """
        A representation of the supported format : `name` (`input` -> `output`)
        """
        return '{name} : {input} → {output}'.format(**self.__dict__)


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

    def text(self, text, target: str, **kwargs) -> TextResult:
        """
        Translates a single `text` or a list of `text` into `target` language
        and returns a TextResult object or a list of TextResult
        @see `optional_text_api_parameters` and documentation for a list of valid parameters
        """
        parameters = self._update_parameters(self.optional_text_api_parameters,
                                             kwargs)
        self.payload.update(parameters)
        self.payload.update(input=text, target=target)
        response = self.post(TEXT_ENDPOINT)
        if isinstance(text, str):
            return TextResult(response['outputs'][0])
        results = []
        for result in response['outputs']:
            results.append(TextResult(result))
        return results

    def file(self, file, target: str, **kwargs) -> FileResult:
        """
        Translates a file into `target` language and returns a FileResult object
        @see `optional_file_api_parameters` and documentation for a list of valid parameters
        """
        parameters = self._update_parameters(self.optional_file_api_parameters,
                                             kwargs)
        self.payload.update(parameters)
        self.payload.update(target=target)
        with open(file, 'rb') as input_file:
            response = self.post(FILE_ENDPOINT, files={'input': input_file})
        return FileResult(response)

    def file_async(self, file, target: str, **kwargs) -> str:
        """
        Translates asynchronously a file into `target` language and returns a request_id
        @see `optional_file_api_parameters` and documentation for a list of valid parameters
        """
        parameters = self._update_parameters(self.optional_file_api_parameters,
                                             kwargs)
        self.payload.update(parameters)
        self.payload['target'] = target
        self.payload['async'] = True
        with open(file, 'rb') as input_file:
            response = self.post(FILE_ENDPOINT, files={'input': input_file})
        return response['requestId']

    def status(self, request_id: str) -> FileStatusResult:
        """
        Get the status of an asynchronous translation request
        """
        self.payload.update(request_id=request_id)
        response = self.get(FILE_STATUS_ENDPOINT)
        return FileStatusResult(response)

    def cancel(self, request_id: str) -> bool:
        """
        Cancel an asynchronous translation request
        """
        self.payload.update(request_id=request_id)
        self.post(FILE_CANCEL_ENDPOINT)
        return True

    def result(self, request_id: str) -> str:
        """
        Get the result of an asynchronous translation request
        """
        self.payload.update(request_id=request_id)
        response = self.get(FILE_RESULT_ENDPOINT)
        return response

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

    def supported_formats(self) -> list:
        """
        List of supported formats with their outputs for the translation.
        """
        results = []
        response = self.get(SUPPORTED_FORMATS_ENDPOINT)
        for supported_format in response['formats']:
            results.append(SupportedFormatResult(supported_format))
        return results
