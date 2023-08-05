# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2017
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------

import sqlite3
import os

import json
import sys
import time
from pixiedust_optimus.utils.constants import PIXIEDUST_REPO_URL
from pkg_resources import get_distribution
from re import search
from requests import post
from os import environ as env
from pixiedust_optimus.utils.printEx import *

from . import pdLogging
logger = pdLogging.getPixiedustLogger()
getLogger = pdLogging.getLogger

myLogger = getLogger(__name__)

__all__ = ['Storage']

SQLITE_DB_NAME = 'pixiedust-optimus.db'
SQLITE_DB_NAME_PATH = os.environ.get("PIXIEDUST_HOME", os.path.expanduser('~')) + "/" + SQLITE_DB_NAME

if not os.path.exists(os.path.dirname(SQLITE_DB_NAME_PATH)):
    os.makedirs(os.path.dirname(SQLITE_DB_NAME_PATH))

#global connection
_conn = None

def _initStorage():
    def copyRename(oldName, newName):
        if os.path.isfile(oldName) and not os.path.isfile(newName):
            from shutil import copyfile
            copyfile(oldName, newName)
            os.rename(oldName, oldName + ".migrated")
            print("")

    #if db already exist with old name, rename it now
    copyRename('spark.db', SQLITE_DB_NAME)
    copyRename(SQLITE_DB_NAME, SQLITE_DB_NAME_PATH)

    global _conn
    if not _conn:
        def _row_dict_factory(cursor,row):
            res={}
            for i,col in enumerate(cursor.description):
                res[col[0]]=row[i]
            return res
        _conn = sqlite3.connect(SQLITE_DB_NAME_PATH)
        _conn.row_factory=_row_dict_factory 
        print("")

    _trackDeployment()

"""
Encapsule access to data from the pixiedust database
including storage lifecycle e.g. schema definition and creation, cleanup, etc...
"""
class Storage(object):
    def __init__(self):
        pass

    def _initTable(self, tableName, schemaDef):
        cursor = _conn.execute("""
            SELECT * FROM sqlite_master WHERE name ='{0}' and type='table';
        """.format(tableName))
        if cursor.fetchone() is None:
            _conn.execute('''CREATE TABLE {0} ({1});'''.format(tableName, schemaDef))
            print("Table {0} created successfully".format(tableName))
        '''
        else:
            print("Deleting table")
            _conn.execute("""DROP TABLE {0}""".format(tableName))
        '''
        cursor.close()

DEPLOYMENT_TRACKER_TBL_NAME = "VERSION_TRACKER"

class __DeploymentTrackerStorage(Storage):
    def __init__(self):
        self._initTable(DEPLOYMENT_TRACKER_TBL_NAME,"VERSION TEXT NOT NULL")

def _trackDeployment():
    deploymenTrackerStorage = __DeploymentTrackerStorage()
    row = deploymenTrackerStorage.fetchOne("SELECT * FROM {0}".format(DEPLOYMENT_TRACKER_TBL_NAME));
    if row is None:
        _trackDeploymentIfVersionChange(deploymenTrackerStorage, None)
    else:
        _trackDeploymentIfVersionChange(deploymenTrackerStorage, row["VERSION"])

def _trackDeploymentIfVersionChange(deploymenTrackerStorage, existingVersion):
    # Get version and repository URL from 'setup.py'
    version = None
    repo_url = None
    try:
        app = get_distribution("pixiedust-optimus")
        version = app.version
        repo_url = PIXIEDUST_REPO_URL
        notebook_tenant_id = os.environ.get("NOTEBOOK_TENANT_ID")
        notebook_kernel = os.environ.get("NOTEBOOK_KERNEL")
        # save last tracked version in the db
        printWithLogo("Pixiedust-Optimus version {0}".format(version))
    except:
        myLogger.error("Error registering with deployment tracker:\n" + str(sys.exc_info()[0]) + "\n" + str(sys.exc_info()[1]))