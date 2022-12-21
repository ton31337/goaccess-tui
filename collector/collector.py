#!/usr/bin/python3

# Run this script as systemd timer periodically.

import time
import sqlite3
import subprocess
import json

log_file = "/var/log/nginx/stats/access.log"
sql_file = "sql/stats.sql"
db_file = "/tmp/goaccess.db"
log_format = '%h - %v %^ [%d:%t %^] %^ "%r" %s %b "%R" "%u"'
date_format = "%d/%b/%Y"
time_format = "%T"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

with open(sql_file, 'r') as file:
    sql_script = file.read()
    cursor.executescript(sql_script)

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
            "--no-query-string",
        ],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode('ascii', 'ignore')

    data_dict = json.loads(log_data)
    for vhost in data_dict["vhosts"]["data"]:
        sqlite_data = 'INSERT INTO stats (timestamp, vhost, visitors) VALUES ({}, "{}", {})'.format(
            time.time(), vhost["data"], vhost["visitors"]["count"]
        )
        cursor.execute(sqlite_data)
    # Delete old records, 10 days retention.
    cursor.execute("DELETE FROM stats WHERE STRFTIME('%s') - timestamp > 864000")

    conn.commit()
    conn.close()

    with open(log_file, "r+") as f:
        f.truncate()
except:
    print("Failed parsing {}".format(log_file))
    conn.close()
