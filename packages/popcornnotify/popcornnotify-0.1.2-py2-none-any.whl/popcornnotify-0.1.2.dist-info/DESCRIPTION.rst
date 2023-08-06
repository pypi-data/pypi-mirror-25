The Popcorn Notify Python Client
================================

This the  Python client library for `Popcorn Notify <https://www.PopcornNotify.com>`_.
Popcorn Notify is a simple non-blocking API to send emails or text messages 
from within your code.

---

::

    from popcornnotify import notify

    notify('contact@popcornnotify.com', 'A new user signed up!', subject="Server Message")

    notify('5555555555', 'Long script has finished running.')

    notify(['contact@popcornnotify.com','support@popcornnotify.com','5555555555'], 'The server is on fire.')


