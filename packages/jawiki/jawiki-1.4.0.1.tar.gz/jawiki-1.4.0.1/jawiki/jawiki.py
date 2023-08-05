
from wikipedia import *

set_lang('ja')

WikipediaPage.__org_repr__ = WikipediaPage.__repr__

def my_wikipedia_page_repr(self):
    return self.__org_repr__() + '\n' + stdout_encode(self.summary)

WikipediaPage.__repr__ = my_wikipedia_page_repr
