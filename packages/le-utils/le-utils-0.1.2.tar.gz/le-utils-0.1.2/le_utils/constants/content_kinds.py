import os
from gettext import gettext as _
from le_utils.constants import file_formats

""" Content Kind Constants """
# constants for ContentKind
TOPIC = "topic"
VIDEO = "video"
AUDIO = "audio"
EXERCISE = "exercise"
DOCUMENT = "document"
HTML5 = "html5"

choices = (
    (TOPIC, _("Topic")),
    (VIDEO, _("Video")),
    (AUDIO, _("Audio")),
    (EXERCISE, _("Exercise")),
    (DOCUMENT, _("Document")),
    (HTML5, _("HTML5 App")),
)

""" Format and Content Kind Mapping """
MAPPING = {
    file_formats.MP4: VIDEO,
    file_formats.MP3: AUDIO,
    file_formats.PDF: DOCUMENT,
    file_formats.PERSEUS: EXERCISE,
    file_formats.HTML5: HTML5,
}

def guess_content_kind(filename):
    """ guess_content_kind: determines what kind the content is
        Args:
            filename (str): name of file to determine kind
        Returns: string indicating node's kind
    """
    ext = os.path.splitext(path)[1][1:].lower()
    if ext in MAPPING:
        return MAPPING[ext]
    else:
        return TOPIC
