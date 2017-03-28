# Scripts to deal with immoscout24

1. Use a Mac + Google Chrome.
1. Install [Appscript](https://pypi.python.org/pypi/appscript/1.0.1): `sudo pip
   install appscript`.
1. Open a tab to immoscout and do a search.
1. Execute `./list_search_results.py`, save the results in a txt file called
   `results.taskpaper`.
1. Next time, `list_search_results.py` will only output new search results, none
   of the one mentioned in `results.taskpaper`.
