Getting super-user privileges
=============================

A bit of background
-------------------
After logging in to EGSE Host you can't perform any super-user activities immediately. When you install new software or change configuration files, you need to get super-user privileges.

EGSE Host configuration grants ``sudo`` privileges to ``customer`` user.

Steps
-----
#. Login to EGSE Host

   .. code-block:: shell-session

      customer@egse-my-egse:~$ ssh customer@egse-my-egse

#. Use ``sudo -i`` to enter interactive super-user shell

   .. code-block:: shell-session

      customer@egse-my-egse:~$ sudo -i
      root@egse-my-egse:~#

   .. note:: Using ``sudo`` doesn't require entering password.
