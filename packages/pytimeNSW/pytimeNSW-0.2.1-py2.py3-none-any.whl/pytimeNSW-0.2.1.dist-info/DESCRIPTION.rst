PyTimeNSW
=========

PyTimeNSW is a fork of `PyTime <https://github.com/shnode/PyTime>`__
with additional days added for NSW and Canberra public holidays.

Installation
------------

.. code:: python

    pip install pytimeNSW

To Do List
----------

1. Add wrapper function or decorator to automatically parse all strings
   into datetime.date ## Basic Usage

.. code:: python

    >>>from pytimeNSW import pytimeNSW
    >>>
    >>>queen = pytimeNSW.queen()           # Queen's Birthday
    >>>print(queen)
    datetime.date(2017, 6, 12)
    >>>
    >>>pytimeNSW.public(easter)             # Easter Public Holidays
    [datetime.date(2017, 3, 30),
     datetime.date(2017, 3, 31),
     datetime.date(2017, 4, 1),
     datetime.date(2017, 4, 2)]
    >>>
    >>> labour = pytimeNSW.labour(2019)      # 2019 Labour Day
    >>>print(labour)
    datetime.date(2019, 10, 7)

Other public holidays

.. code:: python

    >>>pytimeNSW.boxing()                      # Boxing Day
    datetime.date(2015, 12, 26)
    >>>
    >>>pytimeNSW.anzac()                    # Anzac Day
    datetime.date(2017, 4, 25)
    >>>
    >>>pytimeNSW.australia()                # Australia Day
    datetime.date(2017, 1, 26)
    >>>pytimeNSW.public_holidays(1995)                # List of public holidays in given year
    [datetime.date(1995, 4, 25),
     datetime.date(1995, 1, 26),
     datetime.date(1995, 4, 14),
     datetime.date(1995, 4, 15),
     datetime.date(1995, 4, 16),
     datetime.date(1995, 4, 17),
     datetime.date(1995, 1, 1),
     datetime.date(1995, 12, 25),
     datetime.date(1995, 12, 26),
     datetime.date(1995, 6, 12),
     datetime.date(1995, 10, 2)]
    >>>pytimeNSW.is_public('April 25 2015')                # Verifies if a date is a public holiday
    True

            pytimeNSW.is\_public\_can('September 25 2017') # Verifies if
            a date is a public holiday in Canberra True
            pytimeNSW.is\_weekend(datetime.date(2017,9,9) # Verifies if
            a date lands on the weekend True \`\`\`

License
-------

MIT


