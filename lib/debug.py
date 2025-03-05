#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag
import ipdb
from models.company import Company


company = Company.find_by_id(1)
ipdb.set_trace()