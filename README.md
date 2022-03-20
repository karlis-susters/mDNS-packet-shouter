# mDNS-packet-shouter
## Background
Is your Raspberry Pi ignoring you? Do you wish it would listen when you call it by raspberrypi.local instead of having to mess around trying to find its IP to connect to it? Then boy do I have the fix for you.

The .local domain name service is managed by mDNS, which uses IP multicast to query hosts on the network, if someone possesses the domain. For me the issue was the router frequently dropping (90% loss rate) these multicast mDNS packets, so either the Pi never received the query, or my computer never received the response. The fix here was just to make the Pi regularly send out arond 100 of its mDNS query responses, without being queried, so at least one would get to my PC.

To test if you suffer from the same loss rate, when you figure out the IP of your Pi, you can try pinging 224.0.0.251 (the Ip address used for mDNS multicast), and see if your Pi responds always, sometimes or never (sometimes indicates high packet loss, never could be caused by other problems)

## How to run

Run `mdns.py` to create and send the packets. But to use port 5353 as source (mDNS port), we need to disable the service occupying that port (for Pi -- avahi-daemon). This can be done manually, or automatically by running `mdns_manage_avahi.sh`, which should be done as sudo.

In my case I added `*/5 * * * * sudo /path_to_this/mdns_manage_avahi.sh` in my crontab file (run `crontab -e`), to make the script run every 5 minutes.
