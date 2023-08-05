"""Main commands speech2text.

# $ speech2text -i input.mp3 -f html (default) -o output.html
# optional: content type, formatters?
"""

import click
import progressbar
import json
import yaml
import os.path

from .config import SUPPORTED_AUDIO_MODELS, SUPPORTED_CONTENT_TYPES
from . import recognize_speech
from .formatters import get_formatter


def parse_json(options_content):
    return json.loads(options_content)


def parse_yaml(options_content):
    return yaml.load(options_content)


OPTIONS_PARSERS_BY_EXTENSION = {
    'json': parse_json,
    'yaml': parse_yaml,
    'yml': parse_yaml
}

VALID_OPTIONS_EXTENSIONS = [k for k in OPTIONS_PARSERS_BY_EXTENSION]


def parse_options(options_file_path):
    name, extension = os.path.splitext(options_file_path)
    parser = OPTIONS_PARSERS_BY_EXTENSION[extension[1:].lower()]
    with open(options_file_path, 'r') as fp:
        options_content = fp.read()
        return parser(options_content)


def validate_options_name(ctx, param, value):
    if not value:
        return value
    if not any([value.lower().endswith('.' + ext) for ext in VALID_OPTIONS_EXTENSIONS]):
        raise click.BadParameter(
            'options must be: {}'.format(repr(VALID_OPTIONS_EXTENSIONS)))

    return value


@click.command()
@click.option('-i', '--input', type=click.Path(exists=True), required=True)
@click.option('-u', '--username', envvar='IBM_USERNAME', required=True)
@click.option('-p', '--password', prompt=True,
              hide_input=True, envvar='IBM_PASSWORD')
@click.option('-f', '--formatter',
              type=click.Choice(['html', 'markdown', 'json', 'original']),
              default='html')
@click.option('-c', '--content-type',
              type=click.Choice(SUPPORTED_CONTENT_TYPES), required=False)
@click.option('-m', '--audio-model',
              type=click.Choice(SUPPORTED_AUDIO_MODELS), required=False)
@click.option('-t', '--inactivity-timeout', type=int, required=False,
              help="Time in seconds to timeout audio if silent")
@click.option('-o', '--options', type=click.Path(exists=True),
              callback=validate_options_name, required=False)
@click.option('--progress/--no-progress', default=True)
@click.argument('output', type=click.Path(exists=False), required=True)
def speech_to_text(input, username, password, formatter,
                   content_type, audio_model, inactivity_timeout,
                   options, progress, output):

    APP = {
        'progress_bar': None
    }

    def progress_callback(data, progress, total_size):
        if not data and APP['progress_bar'] is None:
            return

        if APP['progress_bar'] is None:
            click.echo("Starting Upload.")
            APP['progress_bar'] = progressbar.ProgressBar(
                maxval=total_size,
                widgets=[progressbar.Bar('=', '[', ']'), ' ',
                         progressbar.Percentage()])
            APP['progress_bar'].start()
        APP['progress_bar'].update(progress)
        if not data:
            APP['progress_bar'].finish()
            click.echo("Upload finished. Waiting for Transcript")

    _callback = progress_callback if progress else None

    if options:
        options = parse_options(options)

    result = recognize_speech(username, password, audio_file_path=input,
                              forced_mime_type=content_type,
                              audio_model=audio_model,
                              inactivity_timeout=inactivity_timeout,
                              extra_options=options,
                              progress_callback=_callback)

    FormatterClass = get_formatter(formatter)
    formatted_output = FormatterClass().format(result)

    with open(output, 'w') as output_file:
        output_file.write(formatted_output)

    click.echo('Speech > Text finished.')
