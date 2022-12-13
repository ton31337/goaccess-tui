#!/usr/bin/python3

# Run this script as systemd timer periodically.

import time
import sqlite3
import subprocess
import json

log_file = "/var/log/nginx/stats/access.log"
db_file = "/tmp/ngx-stats.db"
log_format = '%h - %v %^ [%d:%t %^] %^ "%r" %s %b "%R" "%u"'
date_format = "%d/%b/%Y"
time_format = "%T"

conn = sqlite3.connect(db_file)
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS stats
        (timestamp INT NOT NULL,
        vhost      TEXT    NOT NULL,
        visitors   INT     NOT NULL);
    """
)

try:
    log_data = subprocess.run(
        [
            "/usr/bin/goaccess",
            "-f",
            log_file,
            "--max-items",
            "1000000",
            "--log-format",
            log_format,
            "--date-format",
            date_format,
            "--time-format",
            time_format,
            "-o",
            "json",
        ],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    data_dict = json.loads(log_data)
    for vhost in data_dict["vhosts"]["data"]:
        sqlite_data = 'INSERT INTO stats (timestamp, vhost, visitors) VALUES ({}, "{}", {})'.format(
            time.time(), vhost["data"], vhost["visitors"]["count"]
        )
        conn.cursor().execute(sqlite_data)
    conn.commit()
    conn.close()

    with open(log_file, "r+") as f:
        f.truncate()
except IOError:
    print("Failed parsing {}".format(log_file))
