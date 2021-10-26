:mod:`hackthebox.htb` --- The HTB API Client
===================================================

Session Caching
----------------
If the :code:`cache` option is sent when initializing an API client, the library will follow this algorithm:

* Check if the given path exists
    * If it does, load the :code:`refresh_token` and :code:`access_token` from the file.
    * Check if the :code:`refresh_token` is expired
        * If it is, attempt to use the :code:`refresh_token` to gain a new token
        * If this fails, fall back to a login prompt
    * If it doesn't, fall back to a login prompt
* If it doesn't, fall back to a login prompt
* After any login prompts, and at program exit, the current token pair will be dumped out to the cache file.

If the option is not set, no cache is used at all.

.. automodule:: hackthebox.htb
