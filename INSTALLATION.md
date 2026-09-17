# Installation

## 1. Install Webmin

Install Webmin using the official instructions for your Linux distribution. Confirm you can sign in before installing this module.

## 2. Install collector dependencies

On Debian/Ubuntu-based systems, a typical starting point is:

```bash
sudo apt update
sudo apt install smartmontools curl iproute2 iputils-ping
```

Docker, Tailscale, and UFW are optional and should only be installed if you intend to monitor them.

Verify JSON::PP:

```bash
perl -MJSON::PP -e 'print "JSON::PP OK\n"'
```

## 3. Install the module

Create the Webmin module directory:

```bash
sudo mkdir -p /usr/share/webmin/homelab-monitoring
```

Copy these files into it:

```text
index.cgi
module.info
config.pl.example
```

Then:

```bash
cd /usr/share/webmin/homelab-monitoring
sudo cp config.pl.example config.pl
sudo chmod 755 index.cgi
sudo chmod 644 module.info config.pl
```

## 4. Configure the module

Edit:

```bash
sudo nano /usr/share/webmin/homelab-monitoring/config.pl
```

See `CONFIGURATION.md` for every option.

## 5. Validate Perl syntax

```bash
sudo perl -c /usr/share/webmin/homelab-monitoring/index.cgi
```

Expected result:

```text
syntax OK
```

Note: running the CGI directly from a normal shell may fail with a Webmin environment message such as `WEBMIN_CONFIG not set`. That is expected; Webmin normally supplies its CGI environment.

## 6. Grant Webmin module access

Ensure the Webmin account you use is permitted to access the `homelab-monitoring` module. A Webmin `Access denied` message indicates an ACL issue rather than a Perl problem.

## 7. Open the dashboard

Launch **Homelab Monitoring** from the Webmin navigation menu. Avoid weakening Webmin referer/CSRF protection simply to make manually pasted CGI URLs work.
