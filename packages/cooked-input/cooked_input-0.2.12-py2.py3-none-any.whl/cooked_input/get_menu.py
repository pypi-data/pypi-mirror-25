"""
get_menu - menu system for cooked_input

Len Wanger, 2017

Design:

- Lots of ideas from CursesMenu.

class Menu(object):
    title (str)
    set of menu items (list of MenuItems)

    def __init__(self, title, items=None, **options):
        # options:  add_exit_item (automatically put exit item last), repeat, show_function (for displaying the menu)

    def __repr__(self, function):

    def show(self):
    def add_item(self):
    def remove_item(self):

class DynamicMenu(Menu):
    # takes refresh_items function for generating list of items
    def __init__(self, title, item_function=None, item_function_args,  item_function_kwargs, **options):

class MenuItem(object):
    # abstract base class for MenuItems
    def __init__(self, args, kwargs, **options):
        # options:
        #   disabled: grayed out and not selectable
        #   visible: to make visible/invisiable (not shown)

    def __repr__(self)


class SelectionItem(MenuItem, **options):
    # returns a tag when selected
    def __init__(self, tag):

class FunctionItem(MenuItem, args, kwargs, **options):
    # menu item that calls a callable (function, lambda, or class method)
    # args and kwargs are passed as parameters to the callable
    def __init__(self, text, function, args, **options):

class SubMenuItem(MenuItem):
    def __init__(self, menu, parent, **options):

class SpacerItem(MenuItem):
    # This is not selectable, just for formatting (space or text)
    def __init__(self, text, **options):

class ExitItem(MenuItem):
    # Exits when called
    def __init__(self, text, **options):

class BackItem(MenuItem):
    # Reverts back to parent menu
    def __init__(self, text, **options):


class CITable(object):
    # abstract base class for tables?

<lots more table stuff to do!>
<is a menu a CITable (or subclass) with a menu_displayer display function?>

TODO:
    - Should exit be a SelectionItem or Boolean to add automatically (or both...)
    - How to integrate cleaning and validating?
    - How to set default row/item? None for no default
    - How to have multple choices in a table (crtl to pick multiple rows, shift to pick multiple contiguous rows)
    - Add indent with SpacerItem (so everything below is indented?
    - SpacerItem to BorderItem, with border type (blank for space), test, indent-level, etc. Makes a non-selectable item
        in the menu (up/down to skip it.)
    - Separate ExitItem, or exit_when_selected parameter on selection item?
    - Separate BackItem, or have action for return_to_parent? Could have NavigationItems that has actions for: exit,
        pop_to_parent, or pop_to_top_menu
    - need a get_return() function for the menu? Seems like bad design if needed.
    - General flow:  create menu items, create menu, call menu_show. Or just result = menu.show in a while loop?
    - How to handle actions for non-Function Items (have a action_handler function?) by default return the value?
        They could take a handler function that receives the value tag as a parameter.
    - How to remove/change items in the menu? Should items have a tag?
    - How to page long menus?
    - m.success string for showing success? Or handler just prints (can have flash_messages type of structure for msgs
        from the handler)
    - When sub-menu is called it should have caller/parent passed in plus context info. Then knows where to pop back to
        (so can support being called from many-to-one relationship).
    - Add navigation cmds like menu (dafvid on Github): 'p' - previous item or page, 'n' - next item/page, # for item #,
        'u' - update dynamic menu, 'h' - home/top menu, 'b' - back to parent menu, 'q' - quit, '?' - help
    - Add curses support so menu stays in place and can navigate with arrow keys, then hit select? Bold the current selection,
        default item starts on that item.
    - Work on table getter - display table in curses environment (arrows up/down, next and prev page, etc.) Allow filter
        to search for rows matching criteria (e.g. a Validator), allow render function to be passed in. Make a row_fetcher
        function (like DynamicItem) to get the data from a: list, pretty)_table, database query, Pandas dataframe, ... .
        Allow tab/sh-tab to traverse columns
    - different display functions (i.e. function for displaying the table - silent_table for no display of menu or table),
        can have pretty_table by default (or a curses equivalent) - have curses and non-curses options
    - Use curses for menu and tables, so can refresh in place, highlight current row/col, etc.
    - How to do requirements for curses in Windows?
    - Convenience functions for DynamicMenu (item_fetcher function), ListMenu (all SelectionItems and one handler
        function), FunctionMenu (all FunctionItems), PageMenu (multiple pages), etc.
    - Allow f-strings for prompt (and/or menu text), with kwargs passed in to display function (so can do config menu
        like things - f"edit profile for '{user}'" for "2. edit profile for 'lenw'"
    - Examples/scenarios:
        - menus:
            - example runner
            - simple menu (numbered item built from list)
            - action functions (with args/kwargs for context)
            - sub-menus
            - different borders
            - sub-menu with multiple parents
            - pick-once and quit
            - loop w/ pick until quit picked
            - dynamic menu - from: list, pretty-table, database, Pandas
            - different display functions (i.e. function for displaying the table - silent_table for no display of menu or table)
            - filter functions (i.e. only choices matching a role)
            - set user profile - list users, add profile, edit profile
            - use lambda for actions
        - tables:
            - list, pretty-tablem database, Pandas
            - different borders
            - format columns (width) and rows (length)
            - formats - bold, color, etc. for headers and borders
            - long table (multiple pages)
            - wide table (scroll to see columns)
            - wide table (filter columns shown)
            - search/filter by keyword
            - different display functions
            - filter rows/columns with filter function (e.g. don't show passwords, only certain roles can see certain data)
            - optional edit value - have edit_function to edit the cell value - e.g. change user name, when enter hit does
                database function to change it.
            - optional delete row - delete_function to delete the row (have cut-and-paste functions?)



"""