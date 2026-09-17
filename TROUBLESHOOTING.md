# Troubleshooting

## `WEBMIN_CONFIG not set`

If you run `index.cgi` directly from a shell, Webmin libraries may report:

```text
WEBMIN_CONFIG not set
```

Use `perl -c index.cgi` for syntax checking. Test actual rendering through Webmin.

## `Access denied : User ... is not allowed to use the ... module`

The Webmin account lacks module permission. Fix the Webmin ACL rather than changing the CGI.

## Webmin Security Warning / unknown referer

Do not disable referer protection just for testing. Open the module from Webmin navigation or use a trusted in-Webmin path.

## Literal `$variable` text appears in the page

Perl does not interpolate variables in a single-quoted heredoc:

```perl
print <<'HTML';
```

Use an interpolating block such as:

```perl
print qq{
...
};
```

for HTML containing Perl variables.

## `Can't find string terminator "HTML"`

A `print <<'HTML';` block is missing its closing line:

```text
HTML
```

The terminator must appear by itself at the start of a line.

## `Can't find string terminator "}"`

A `print qq{` block is missing its closing:

```perl
};
```

## Docker shows `N/A`

Check that Webmin's execution context can run `docker` and that the relevant user/process has permission to access Docker.

## SMART shows `N/A`

Verify `smartmontools` is installed and test:

```bash
smartctl -H /dev/sda
```

## Weather shows `N/A`

Verify outbound HTTPS access and JSON support:

```bash
curl --version
perl -MJSON::PP -e 'print "JSON::PP OK\n"'
```

## Network diagnostics are slow

The template performs short ping tests during page rendering. If you expand network checks, keep timeouts short or move collection into a scheduled background job so dashboard rendering remains responsive.
