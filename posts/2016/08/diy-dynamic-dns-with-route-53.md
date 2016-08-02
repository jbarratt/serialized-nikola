<!-- 
.. title: DIY Dynamic DNS with Route 53
.. slug: diy-dynamic-dns-with-route-53
.. date: 2016-08-02 00:08:23 UTC
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

I haven't needed dynamic DNS service for a while, but I have a new use case that calls for it.
I looked around at the existing free options, and had a flash of that "if you're not paying for it, you're the product" feeling.

Suddenly, it hit me. I have DNS hosted somewhere that I can update via API. (AWS Route 53). This is easy!

The only dependency is that your computer be

1. Configured with AWS credentials in a named profile
2. Have [cli53](https://github.com/barnybug/cli53) installed
3. Have `curl`, `bash` and `dig` installed.
4. Already have a zone configured in Route53.

Tweak the below script to match your AWS profile and managed zone.

```
#!/bin/bash

# Requires cli53 (i.e. `brew install cli53` on mac)

# Update these values for yourself
export AWS_PROFILE='myprofile'
ZONE="mydomain.com"
HOSTNAME="dynamichost"
# this would configure dynamichost.mydomain.com with your current public IP

export PATH="/usr/local/bin:/usr/bin/:$PATH"
REMOTE_IP=$(curl -s ipecho.net/plain)
CURRENT_VALUE=$(dig +short $HOSTNAME.$ZONE)

if [[ $REMOTE_IP =~ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ ]] ; then
    if [[ $CURRENT_VALUE != $REMOTE_IP ]] ; then
        cli53 rrcreate --replace $ZONE "$HOSTNAME 60 A $REMOTE_IP"
    fi
fi
```

It uses `dig +short` first to check the current value of the setting, so it doesn't bother with changing the values in Route 53 unless a change is needed.

Even though it's been deprecated, I still use `crontab`, as it works and is a lot simpler than `launchd`.

To install this, copy the script somewhere on your machine, then run `crontab -e`.
A simple cron like this will run the script once every 2 minutes:

```
*/2 * * * * /Path/To/Your/script.sh
```

And you're done! You will have a 60 second TTL DNS entry which only gets updated when your actual public IP changes, at what will probably be $0 additional cost, if you're already hosting the zone in R53.
