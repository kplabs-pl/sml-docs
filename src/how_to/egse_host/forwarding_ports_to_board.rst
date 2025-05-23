Forwarding TCP/UDP ports to board
=================================

A bit of background
-------------------

Board isn't connected directly to Smart Mission Lab network which means that you can't access any network services (for example: Web server) on it from your workstation. EGSE Host supports forwarding TCP and UDP ports to Board allowing almost-direct to services exposed by Board. System uses `nftables <https://wiki.nftables.org/wiki-nftables/index.php/Main_Page>`_ to configure port forwarding.

Steps
-----
1. Log in to EGSE Host

   .. code-block:: shell-session

        my-machine$ ssh customer@egse-my-egse.egse.vpn.sml.kplabs.space
        customer@egse-my-egse:~$

2. Edit port forwarding configuration file

   .. code-block:: shell-session

        customer@egse-my-egse:~$ sudo nano /etc/nftables.conf

3. Modify ``tcp_redirects`` table (for forwarding TCP ports) or ``udp_redirects`` table (for forwarding UDP ports). Follow comments in the file on exact format of elements.

   .. md-tab-set::
      .. md-tab-item:: Antelope

         .. code-block::
            :emphasize-lines: 4-7, 14-17

            map tcp_redirects {
                type inet_service : inet_service
                elements = {
                    # One element = one port
                    # <port on egse-host>: <port on dpu>
                    122 : 22,
                    # Add your port redirects here, remember to have trailing comma on previous non-comment line
                }
            }

            map udp_redirects {
                type inet_service : inet_service
                elements = {
                    # One element = one port
                    # <port on egse-host>: <port on dpu>
                    # e.g. 123 : 456,
                    # Add your port redirects here, remember to have trailing comma on previous non-comment line
                }
            }



      .. md-tab-item:: Leopard

          .. code-block::
            :emphasize-lines: 4-8, 15-18

            map tcp_redirects {
                type inet_service : inet_service
                elements = {
                    # One element = one port
                    # <port on egse-host>: <node1/node2>:<port on dpu>
                    122 : node1:22,
                    222 : node2:22,
                    # Add your port redirects here, remember to have trailing comma on previous non-comment line
                }
            }

            map udp_redirects {
                type inet_service : inet_service
                elements = {
                    # One element = one port
                    # <port on egse-host>: <node1/node2>:<port on dpu>
                    # e.g. 123 : 456,
                    # Add your port redirects here, remember to have trailing comma on previous non-comment line
                }
            }

4. Restart ``nftables`` service

   .. code-block:: shell-session

          customer@egse-my-egse:~$ sudo systemctl restart nftables

Summary
-------
To expose service from DPU to your workstation, you need to configure port forwarding on EGSE Host. Base configuration files for nftables are already present. You can modify them to suit your needs.
