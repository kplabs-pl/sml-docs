Setting password
================

A bit of background
-------------------
Occasionally you may need to use ``customer`` user with password authentication. Right after subscribing, that user has no password thus not allowing that kind of authentication. To use password, you need to set new password for ``customer`` user.

Setting up password
-------------------
#. Log-in to EGSE Host

   .. code-block:: shell-session

        my-machine$ ssh customer@egse-my-egse.egse.sml.lan
        customer@egse-my-egse:~$

#. Set up password

   .. code-block:: shell-session

        customer@egse-my-egse:~$ sudo passwd customer
        New password:
        Retype new password:
        passwd: password updated successfully

#. Now you can authenticate as ``customer`` user using password you've set up.
