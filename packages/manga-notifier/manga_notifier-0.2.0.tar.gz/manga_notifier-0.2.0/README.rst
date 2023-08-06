manga-notifier
--------------

manga-notifier is a command-line tools to send osx notifications when a
new chapter of manga is released (www.mangastream.com)

Setup
-----

First you need to install
```terminal-notifier`` <https://github.com/alloy/terminal-notifier>`__.

Via `Homebrew <https://github.com/Homebrew/homebrew>`__:

::

    $ brew install terminal-notifier

Then:

::

    $ pip install manga-notifier

Usage
-----

First, add your favorite manga and the last chapter. (see
```Mangastream`` <http://www.mangastream.com>`__)

::

    $ manga-notifier add "One piece" 879

Then:

::

    $ manga-notifier

If there is a new chapter, you will receive a notification. Click on the
notification and it will open the chapter in a browser.

Other usage
~~~~~~~~~~~

You can add it to your .bashrc. In that case, each time you open a
terminal, it will check new release of your favorite manga.

Or you can add it in your crontab.
