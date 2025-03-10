Accessing historical telemetry
==============================

Goal
----
In this tutorial you will:

* Power on DPU board to generate several minutes of telemetry data
* Access historical telemetry data from Smart Mission Lab system

Prerequisites
-------------
* Active subscription within Smart Mission Lab system
* Active VPN connection to Smart Mission Lab system
* Access to EGSE Host
* Board prepared to run Linux distribution

  * For Antelope use Linux distribution built in :doc:`/tutorials/antelope/zero_to_hero/index` tutorials

A bit of background
-------------------
When board's supervisor is running, Smart Mission Lab system continuously monitors telemetry readouts from board. Customer can access collected values using Grafana web application.

Generate telemetry data
-----------------------
1. Log in to EGSE Host using SSH

   .. code-block:: shell-session

       user@my-machine:~$ ssh customer@egse-my-egse.egse.vpn.sml.kplabs.space
       customer@egse-my-egse:~$

2. Power on board

   .. md-tab-set::
      .. md-tab-item:: Antelope

         .. code-block:: shell-session

            customer@egse-my-egse:~$ sml power on
            Powering on...Success

      .. md-tab-item:: Leopard

         .. code-block:: shell-session

            customer@egse-my-egse:~$ sml power on
            Powering on...Success

3. Wait 2 minutes
4. Power on DPU

   .. md-tab-set::
     .. md-tab-item:: Antelope

        .. code-block:: shell-session

           customer@egse-my-egse:~$ sml dpu power on
           Powering on...Success
           customer@egse-my-egse:~$ sml dpu reset off
           Bringing DPU out of reset...Success

     .. md-tab-item:: Leopard

         .. code-block:: shell-session

            customer@egse-my-egse:~$ sml pn1 power on
            Powering on...Success


Access historical telemetry
---------------------------

1. Open https://grafana.vpn.sml.kplabs.space in your web browser
2. Grafana will redirected you to Customer Dashboard for sign-in. Log-in using your credentials
3. After successful login, you will go back to Grafana home page automatically

   .. figure:: ./images/grafana_dashboards.png

         Dashboards available after logging in

4. Open dashboard with telemetry for your board (for Antelope use :menuselection:`Antelope Telemetry`, for Leopard use :menuselection:`Leopard Telemetry`)
5. Select board to display telemetry by selecting name of your EGSE Host in :menuselection:`hostname` dropdown at the top of the dashboard

   .. figure:: ./images/grafana_hostname_selector.png

       Select board to display by switching EGSE Host name

6. Select time range that contains this tutorial by selecting :menuselection:`Last 30 minutes`

   .. figure:: ./images/grafana_time_range.png

        Select time range to display

   .. note:: If you performed first part of this tutorial (powering on board) more than 30 minutes ago, you can select different time range. Use longer 'last ..' selection or enter absolute times to show data gathered during this tutorial.

7. Dashboard now displays telemetry data from your board.

   .. figure:: ./images/grafana_antelope_dashboard.png

         Example of Antelope Telemetry dashboard

Summary
-------
SML infrastructure constantly monitors and collects telemetry readouts from boards. At any point in time, you can use Grafana to review collected data.
