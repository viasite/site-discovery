## Recommended packages for site-info
- [viasite/drupal-scripts](https://github.com/viasite/drupal-scripts)
- [viasite/server-scripts](https://github.com/viasite/server-scripts)

## Install
```
pip install site_discovery
```

# get-sites
Get sites from localhost and execute site-info for each site.

## Configuration
Config file should placed into `/etc/site-info.yml`. See [site-info.example.yml](site-info.example.yml).
``` yaml
tests:
- name: root_path # name of test, using as json name and xlsx column name
  comment: Site root # using as comment for cell in xlsx
  command: pwd # shell command for get test result
  type: string # result type (integer|string|time)
  groups: main # string or array of groups
```

I'm using group `main` for must-have tests.


## Usage
### Default sites list, output to tab separated list
```
get-sites
```

### Generate all tests results into xlsx with delay for avoid server overload
```
get-sites --format xlsx --xlsx-path /tmp/sites-info.xlsx --group all --delay 10
```

## Options
- `--format=[console|json|xlsx|line]` - output format
- `--quiet` - don't output progress
- `--color` - colorize line output
- `--root-path-excluded=ROOT_PATHS_EXCLUDED` - exclude some paths, default: [/usr/share/nginx/html, /var/www/html, /var/www/example.com]
- `--excluded-file=EXCLUDED_FILE` - don't scan site with file in site root, default: `.excluded`
- `--cached` - Only attach site-info, don't generate
- `--cache-time=TIME` - Cache time, when `--cached` not set
- `--delay=DELAY` - Delay between site-info calls, seconds, default: 0
- `--lock-file-path=LOCK_FILE_PATH` - Path to lockfile, default: `/tmp/sites-info.lock`
- `--lock-file-max-age=LOCK_FILE_AGE` - Max age of lockfile (since last modification), seconds, default: 86400
- `--results-dir=RESULTS_DIR` - Path to directory with site-info results, default: `/var/log/site-info`
- `--force` - Ignore lockfile
- `--group=GROUPS` - Groups of site-info tests, default: main. --group all assumes execution of all tests.
- `--limit=LIMIT` - Limit of sites
- `--sites-json=SITES_JSON` - Get sites results from json
- `--xlsx-path=XLSX_PATH` - xlsx destination path


# site-info
Get info for single site.

# server-info
Get info for server.
