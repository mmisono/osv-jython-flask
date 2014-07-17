#!/usr/bin/env python

import os
import os.path

from database import init_db
from blog import app, DATABASE, JDBC_URL, JDBC_DRIVER

if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db(JDBC_URL, JDBC_DRIVER)
    app.run(host="0.0.0.0", port=18080)
