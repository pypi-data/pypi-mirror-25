### Feed2toot

Feed2toot automatically parses rss feeds, identifies new posts and posts them on the [Mastodon](https://mastodon.social) social network.
For the full documentation, [read it online](https://feed2toot.readthedocs.org/en/latest/).

If you would like, you can [support the development of this project on Liberapay](https://liberapay.com/carlchenet/).
Alternatively you can donate cryptocurrencies:

- BTC: 1AW12Zw93rx4NzWn5evcG7RNNEM2RSLmAC
- XMR: 43GGv8KzVhxehv832FWPTF7FSVuWjuBarFd17QP163uxMaFyoqwmDf1aiRtS5jWgCiRsi73yqedNJJ6V1La2joznKHGAhDi

### Quick Install

* Install Feed2toot from PyPI

        # pip3 install feed2toot

* Install Feed2toot from sources
  *(see the installation guide for full details)
  [Installation Guide](http://feed2toot.readthedocs.org/en/latest/install.html)*


        # tar zxvf feed2toot-0.7.tar.gz
        # cd feed2toot
        # python3 setup.py install
        # # or
        # python3 setup.py install --install-scripts=/usr/bin

### Create the authorization for the Feed2toot app

* Just launch the following command::

        $ register_feed2toot_app

### Use Feed2toot

* Create or modify feed2toot.ini file in order to configure feed2toot:

        [mastodon]
        instance_url=https://mastodon.social
        user_credentials=feed2toot_usercred.txt
        client_credentials=feed2toot_clientcred.txt
        ; Default visibility is public, but you can override it:
        ; toot_visibility=unlisted

        [cache]
        cachefile=cache.db

        [rss]
        uri=https://www.journalduhacker.net/rss
        toot={title} {link}

        [hashtaglist]
        several_words_hashtags_list=hashtags.txt

* Launch Feed2toot

        $ feed2toot -c /path/to/feed2toot.ini

### Authors

* Carl Chenet <chaica@ohmytux.com>
* Antoine Beaupré <anarcat@debian.org>
* First developed by Todd Eddy

### License

This software comes under the terms of the GPLv3+. Previously under MIT license. See the LICENSE file for the complete text of the license.
