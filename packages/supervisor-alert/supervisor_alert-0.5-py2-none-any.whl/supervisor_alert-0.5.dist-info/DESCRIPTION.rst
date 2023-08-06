supervisor-alert
================

|Version| |pyversions| |Downloads| |License|

Are you using `Supervisor <http://supervisord.org>`__ to manage
processes on a server? With supervisor-alert you can receive messages
when the state of your processes change. Be the first to know when your
services die!

With the default configuration supervisor-alert sends messages over
Telegram. For this to work you need to install
`telegram-send <https://github.com/rahiel/telegram-send>`__ system-wide
first. You can also use any shell command to send the notifications.

Installation
============

Install supervisor-alert on your system:

.. code:: shell

    sudo pip install supervisor-alert

You must install it with Python 2 because Supervisor doesn't support
Python 3 yet. For Supervisor 4+ you may have Python 3 support, if
``python3 -c 'import supervisor'`` doesn't give an error, you should
install supervisor-alert with pip3/python3.

Then run:

.. code:: shell

    sudo supervisor-alert --configure

for the default configuration. This will send notifications over
Telegram. Read the next section to customize or if you dislike automatic
configurations.

Manual Configuration
====================

Create the file ``/etc/supervisor/conf.d/supervisor_alert.conf`` as
root:

.. code:: shell

    [eventlistener:supervisor_alert]
    command=supervisor-alert --telegram
    events=PROCESS_STATE_RUNNING,PROCESS_STATE_EXITED,PROCESS_STATE_FATAL
    autostart=true
    autorestart=true
    user=supervisor_alert

This will send the notifications over Telegram, to use something else,
for example `ntfy <https://github.com/dschep/ntfy>`__, pass in the
command:

.. code:: shell

    command=supervisor-alert -c 'ntfy send'

By default the config file at ``/etc/telegram-send.conf`` is used for
telegram-send, to use a different config, or to pass any other options:

.. code:: shell

    command=supervisor-alert -c 'telegram-send --config /home/user/bunny.conf'

Optionally you can show the hostname before each message with the
``--show-hostname`` option:

.. code:: shell

    command=supervisor-alert --telegram --show-hostname

The default configuration will run the event listener as the user
``supervisor_alert``. It is a good practice to isolate services by
running them as separate users (and avoiding running them as root). Add
the user with:

.. code:: shell

    sudo adduser supervisor_alert --system --no-create-home

Optionally, you can also subscribe to different supervisor events, `look
at the docs <http://supervisord.org/events.html#event-types>`__ to see
on which ones you'd like to be notified.

Finally, load the config and start the event listener:

.. code:: shell

    sudo supervisorctl reread
    sudo supervisorctl update

You should now receive your first alert, notifying you that
``supervisor_alert`` has started running.

.. |Version| image:: https://img.shields.io/pypi/v/supervisor-alert.svg
   :target: https://pypi.python.org/pypi/supervisor-alert
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/supervisor-alert.svg
   :target: https://pypi.python.org/pypi/supervisor-alert
.. |Downloads| image:: https://www.cpu.re/static/supervisor-alert/downloads.svg
   :target: https://www.cpu.re/static/supervisor-alert/downloads-by-python-version.txt
.. |License| image:: https://img.shields.io/pypi/l/supervisor-alert.svg
   :target: https://github.com/rahiel/supervisor-alert/blob/master/LICENSE.txt


