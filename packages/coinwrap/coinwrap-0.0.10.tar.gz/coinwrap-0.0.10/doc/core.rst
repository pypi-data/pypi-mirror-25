=======
core.py
=======

A.1:
    While the class is not necessary for a program like this to function, in 
    the spirit of object-oriented design, everything is self-contained.

A.2:
    An uninstantiated session variable made to reference the ``requests`` lib
    ``Session`` class; however, it contains an underscore so that it doesn't 
    conflict with the ``session`` method.

A.4:
    Starts the session and updates the webpage headers to let the site know 
    who is crawling it and also to identify the JSON format that we are 
    attempting to scrape.

A.5:
    This method goes to the target site and attempts to collect the JSON 
    response and return it. This *magic method* uses double underscores 
    to ensure that the name will not overlap with the ``request`` method 
    from the request lib.

A.5:
    A user-available method that performs coinmarketcap's API ``ticker`` 
    method. If currency is available on coinmarketcap, then it adds that 
    string as an endpoint and also accepts a parameter for formatting 
    the output.

A.6:
    Returns the market stats according to the input.
