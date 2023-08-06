from time import sleep
from datetime import datetime
import platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from .utils import Nonlocals
from ordered_set import OrderedSet
import re


class ElementNotFound(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return str(self.kwargs)


class MultipleElementsReturned(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return str(self.kwargs)



def get_element(self, css=None, text=None):
    lst = get_elements(self, css=css, text=text)
    if lst == []:
        raise ElementNotFound(css=css, text=text)
    if len(lst) > 1:
        raise MultipleElementsReturned(css=css, text=text)
    return lst[0]


def get_elements(self, css=None, text=None):
    """
    get_elements(d, css="a", text="hello")
    >>> List of <a> tags whose text exactly equals "hello"
    """
    if css is None and text is None:
        raise ValueError()

    # Use ordered sets so we don't muck up the ordering if the caller specifies
    # two or more arguments. This is a bit over-convoluted for having only two
    # ways to query (css and text) but the pattern makes it easy to plug in
    # more ways.
    #items = None
    nonlocals = Nonlocals(items=None)
    def update(new_items):
        if nonlocals.items == None:
            nonlocals.items = OrderedSet(new_items)
        else:
            nonlocals.items = nonlocals.items & OrderedSet(new_items)

    if text is not None:
        update([e for e in get_elements(self, css="*") if e.text == text])
    if css is not None:
        update(self.find_elements_by_css_selector(css))

    return nonlocals.items


def get_classes(self):
    return [c for c in re.split(r'\s+', self.get_attribute("class")) if c]


def monkeypatch_webdriver_objects():
    methods = (
        get_element,
        get_elements,
        get_classes
    )

    for m in methods:
        setattr(WebElement, m.__name__, m)
        setattr(WebDriver, m.__name__, m)

    @property
    def left(self):
        return self.location['x']

    @property
    def top(self):
        return self.location['y']

    @property
    def width(self):
        return self.size['width']

    @property
    def height(self):
        return self.size['height']

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def value(self):
        return self.get_attribute("value")

    WebElement.left = left
    WebElement.top = top
    WebElement.width = width
    WebElement.height = height
    WebElement.right = right
    WebElement.bottom = bottom
    WebElement.value = value

    def webelement__repr__(self):
        id = self.get_attribute("id")
        return "<WebElement: {tag_name}{id}{classes}>".format(
            tag_name=self.tag_name,
            id=("#" + id) if id else "",
            classes="".join(["." + c for c in self.get_classes()])
        )
    WebElement.__repr__ = webelement__repr__
            

def set_element_text(el, text, expected_text=None, defocus=False):
    def _set_text():
        # Turns out Ctrl+A (select all) and type over is better than calling
        # the `clear` method because if we call `clear` on a DateTimePicker's
        # input control, the control will reinstate the original text before we
        # get to write our own text.

        if platform.system() == 'Darwin':
            # Keys.COMMAND + 'a' has been broken on Chromedriver for five years.
            el.parent.execute_script("arguments[0].select()", el)
        else:
            retry_until_successful(lambda: el.send_keys(Keys.CONTROL + 'a'))

        retry_until_successful(lambda: el.send_keys(text))
        if defocus:
            # When Chrome decides to break sending the tab key into the text box and instead
            # makes that enter a tab character into the text box, document.activeElement.blur()
            # is another way to defocus the text box.
            # retry_until_successful(lambda: el.send_keys(Keys.TAB))
            retry_until_successful(lambda: el.parent.execute_script("document.activeElement.blur()"))

        if expected_text is not None:
            assert el.value.strip() == expected_text
    retry_until_successful(_set_text)


def retry_until_successful(func, num_retries=20, delay_ms=200):
    max_time_s = num_retries * delay_ms / 1000
    start_time = datetime.now()
    for i in range(0, num_retries):
        try:
            return func()
        except Exception as e:
            print(e)
            if (datetime.now() - start_time).total_seconds() >= max_time_s or i == num_retries - 1:
                raise
            sleep(delay_ms / 1000)


def retry_until_true(func, num_retries=20, delay_ms=200):
    retry_until_successful(lambda: _assert(func()), num_retries=num_retries, delay_ms=delay_ms)


def _assert(val, msg=None):
    assert val, msg
    return True


class Nonlocals(object):
    """ Helper class to implement nonlocal names in Python 2.x """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
