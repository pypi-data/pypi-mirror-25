import markdown as markdown_parser
import html as html_parser

from django.core.paginator import Paginator, EmptyPage

def parse_formatting(text: str, html: bool = False, markdown: bool = False) -> str:
    '''Parses formatted text.

    Arguments:

        text: The string to be parsed.

        html: If True, html in the original string will not be escaped.

        markdown: If True, the Markdown syntax will be applied.

    '''

    # Escapes HTML tags if HTML is disabled
    if not html:
        text = html_parser.escape(text)

    # Parses Markdown
    # Places the original text in <p> tags if Markdown is disabled in order
    # to maintain consistancy when the page is displayed.
    if markdown:
        text = markdown_parser.markdown(text)
    else:
        text = '<p>' + text + '</p>'

    return text

def surrounding_pages(paginator: Paginator, page: int, count: int = 3) -> dict:
    '''Calculates the page numbers before and after the current page in a
    paginated view.

    Arguments:

        paginator: The Paginator object.

        page: The current page.

        count: The number of pages in either direction.

    '''

    page = int(page)

    page_numbers = {
        'before': [],
        'after': [],
    }

    # Page numbers before the current page
    for _ in range(count):
        try:
            page_current = paginator.page(page - _)
            page_before = page_current.previous_page_number()
        except EmptyPage:
            break

        # Prepend to the list instead of append
        # Ensures that the page numbers are ordered from smallest to largest
        page_numbers['before'] = [page_before] + page_numbers['before']

    # Page numbers after the current page
    for _ in range(count):
        try:
            page_current = paginator.page(page + _)
            page_after = page_current.next_page_number()
        except EmptyPage:
            break

        page_numbers['after'].append(page_after)

    return page_numbers
