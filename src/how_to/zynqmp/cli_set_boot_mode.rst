Override boot mode using SML CLI
================================

A bit of background
-------------------
AMD Zynq UltraScale+ MPSoC devices boot by using firmware from storage selected by **boot mode** pins. When accessing hardware remotely (as is the case in Smart Mission Lab), it's possible to use SML CLI to override boot mode. Contrary to :doc:`/how_to/zynqmp/jtag_set_boot_mode` this method set physical pins on Zynq UltraScale+ device.

Prerequisites
-------------
None

Steps
-----
1. Log in to EGSE Host

   .. code-block:: shell-session

        my-machine$ ssh customer@egse-my-egse.egse.vpn.sml.kplabs.space
        customer@egse-my-egse:~$

2. Set boot mode using SML CLI

   .. md-tab-set::
      .. md-tab-item:: Antelope

        .. code-block:: shell-session

            customer@egse-my-egse:~$ sml dpu boot-mode set jtag
            Setting boot mode to 0b0000 (jtag)...Success

      .. md-tab-item:: Leopard (PN1)

         .. code-block:: shell-session

            customer@egse-my-egse:~$ sml pn1 boot-mode set jtag
            Setting boot mode to 0b0000 (jtag)...Success

      .. md-tab-item:: Leopard (PN2)

         .. code-block:: shell-session

            customer@egse-my-egse:~$ sml pn2 boot-mode set jtag
            Setting boot mode to 0b0000 (jtag)...Success

3. Inspect currently set boot mode

   .. md-tab-set::
      .. md-tab-item:: Antelope

        .. code-block:: shell-session

            customer@egse-my-egse:~$ sml dpu boot-mode get
            Getting boot mode...0b0000 (jtag)

      .. md-tab-item:: Leopard (PN1)

         .. code-block:: shell-session

            customer@egse-my-egse:~$ sml pn1 boot-mode get
            Getting boot mode...0b0000 (jtag)

      .. md-tab-item:: Leopard (PN2)

         .. code-block:: shell-session

            customer@egse-my-egse:~$ sml pn2 boot-mode get
            Getting boot mode...0b0000 (jtag)

.. note:: You can specify boot mode using friendly-name or binary value. See ``--help`` output for ``boot-mode`` command for details.

.. warning:: SML CLI allows you to set boot mode to value that might be unusable (for example USB boot)
