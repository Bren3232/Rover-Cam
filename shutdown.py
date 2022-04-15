#!/usr/bin/env python3


# Copyright (C) 2022 Brendan Murphy - All Rights Reserved
# This file is part of the Rover Cam project.


from subprocess import run
import time

# print("in shutdown file - shutting down in 11 sec")
# time.sleep(1)

time.sleep(11)

run(['sudo', 'shutdown', 'now'])


