from enum import Enum

MAX_BLOG_ARTICLE_TITLE_LENGTH = 69

RICH_TEXT_BLOCK_FEATURES = [
    "bold",
    "italic",
    "ol",
    "ul",
    "hr",
    "link",
    "document-link",
    "image",
    "embed",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "code",
    "superscript",
    "subscript",
    "strikethrough",
    "blockquote",
]

MAX_BLOG_ARTICLE_INTRO_LENGTH = 250

INTRO_ELLIPSIS = " [...]"


class ArticleBodyBlockNames(Enum):
    do_not_call_in_templates = True

    MARKDOWN = "markdown"
    HEADER = "header"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    IMAGE = "image"
