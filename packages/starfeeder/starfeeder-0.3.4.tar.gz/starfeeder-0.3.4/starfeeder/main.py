#!/usr/bin/env python
# starfeeder/main.py

"""
    Copyright (C) 2015-2017 Rudolf Cardinal (rudolf@pobox.com).

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


REFERENCES cited in code:
[1] E-mail to Rudolf Cardinal from Søren Ellegaard, 9 Dec 2014.
[2] E-mail to Rudolf Cardinal from Søren Ellegaard, 10 Dec 2014.
[3] "RFID Reader.docx" in [1]; main reference for the RFID tag reader.
[4] "ba_ad105_e_2.pdf" in [1]; main reference for the balance.
[5] "RFID and LOAD CELL DEVICES - SE_20141209.pptx" in [1].
[6] E-mail to Rudolf Cardinal from Matthew Weinie, 8 Dec 2015.

"""

import argparse
import faulthandler
import logging
import sys
import traceback
from typing import List

from cardinal_pythonlib.sqlalchemy.alembic_func import (
    get_current_and_head_revision,
    upgrade_database,
)
from cardinal_pythonlib.logs import (
    configure_logger_for_colour,
    copy_root_log_to_file,
)
from cardinal_pythonlib.signalfunc import trap_ctrl_c_ctrl_break
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.QtWidgets import QApplication
from sqlalchemy import create_engine
from whisker.qt import (
    GarbageCollector,
    LogWindow,
    run_gui,
)
import whisker.version

from starfeeder.constants import (
    ALEMBIC_BASE_DIR,
    ALEMBIC_CONFIG_FILENAME,
    DATABASE_ENV_VAR_NOT_SPECIFIED,
    DB_URL_ENV_VAR,
    LOG_FORMAT,
    LOG_DATEFMT,
    WINDOW_TITLE,
    WRONG_DATABASE_VERSION_STUB,
)
from starfeeder.gui import (
    BaseWindow,
    NoDatabaseSpecifiedWindow,
    WrongDatabaseVersionWindow,
)
from starfeeder.settings import (
    get_database_url,
    set_database_url,
    set_database_echo,
)
from starfeeder.version import VERSION

log = logging.getLogger(__name__)


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    trap_ctrl_c_ctrl_break()
    # NOTE that manually closing the Windows command prompt running the
    # command-line version of Starfeeder will lead to an instant kill.

    # -------------------------------------------------------------------------
    # Arguments
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Starfeeder v{}. Whisker bird monitor, reading from RFID "
        "tag readers and weighing balances.".format(VERSION))
    # ... allow_abbrev=False requires Python 3.5
    parser.add_argument("--logfile", default=None,
                        help="Filename to append log to")
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help="Be verbose (use twice for extra verbosity)")
    parser.add_argument('--debug_gc', action="store_true",
                        help="Debug garbage collection")
    parser.add_argument('--guilog', action="store_true",
                        help="Show Python log in a GUI window")
    parser.add_argument('--upgrade-database', action="store_true",
                        help="Upgrade database (determined from SQLAlchemy"
                        " URL, read from {} environment variable) to current"
                        " version".format(DB_URL_ENV_VAR))
    parser.add_argument('--gui', '-g', action="store_true",
                        help="GUI mode only")
    parser.add_argument(
        "--dburl", default=None,
        help="Database URL (if not specified, task will look in {} "
        "environment variable).".format(DB_URL_ENV_VAR))
    parser.add_argument('--dbecho', action="store_true",
                        help="Echo SQL to log.")
    # parser.add_argument('--debug-qt-signals', action="store_true",
    #                     help="Debug QT signals.")

    # We could allow extra Qt arguments:
    # args, unparsed_args = parser.parse_known_args()
    # Or not:
    args = parser.parse_args()
    unparsed_args = []  # type: List[str]

    qt_args = sys.argv[:1] + unparsed_args

    # -------------------------------------------------------------------------
    # Modify settings if we're in a PyInstaller bundle
    # -------------------------------------------------------------------------
    in_bundle = getattr(sys, 'frozen', False)
    if in_bundle:
        args.gui = True
    if not args.gui:
        args.guilog = False

    # -------------------------------------------------------------------------
    # If non-Python code causes a segfault, get some sort of trace
    # -------------------------------------------------------------------------
    faulthandler.enable()

    # -------------------------------------------------------------------------
    # Create QApplication before we create any windows (or Qt will crash)
    # -------------------------------------------------------------------------
    qt_app = QApplication(qt_args)

    # Attempt to fix rare bugs by constraining the Python garbage collector
    # to the GUI thread only

    # noinspection PyUnusedLocal
    my_garbage_collector = GarbageCollector(qt_app, interval_ms=100,
                                            debug=args.debug_gc)
    # ... with interval of 10000, get
    #     pymysql.err.OperationalError (1040, 'Too many connections')
    # ... 500 seems OK
    # ... not sure why there was a problem, though, as all sessions are created
    #     using "with session_thread_scope", and when that finishes, it calls
    #     session.close(), and that's meant to release all resources:
    #     http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#closing
    # ... since I'm not sure, let's use 100 to be conservative

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    loglevel = logging.DEBUG if args.verbose >= 1 else logging.INFO
    logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATEFMT,
                        level=loglevel)
    rootlogger = logging.getLogger()
    rootlogger.setLevel(loglevel)
    configure_logger_for_colour(rootlogger)  # configure root logger
    logging.getLogger('whisker').setLevel(logging.DEBUG if args.verbose >= 2
                                          else logging.INFO)
    if args.logfile:
        copy_root_log_to_file(args.logfile)
    if args.guilog:
        log_window = LogWindow(level=loglevel,
                               window_title=WINDOW_TITLE + " Python log",
                               logger=rootlogger)
        log_window.show()

    # If any exceptions happen up to this point, we're a bit stuffed.
    # But from now on, we can trap anything and see it in the GUI log, if
    # enabled, even if we have no console.

    # noinspection PyBroadException
    try:

        # ---------------------------------------------------------------------
        # Info
        # ---------------------------------------------------------------------
        log.info("Starfeeder v{}: RFID/balance controller for Whisker, "
                 "by Rudolf Cardinal (rudolf@pobox.com)".format(VERSION))
        log.debug("args: {}".format(args))
        log.debug("qt_args: {}".format(qt_args))
        log.debug("PyQt5 version: {}".format(PYQT_VERSION_STR))
        log.debug("Qt version: {}".format(QT_VERSION_STR))
        log.debug("Whisker client version: {}".format(whisker.version.VERSION))
        if in_bundle:
            log.debug("Running inside a PyInstaller bundle")
        if args.gui:
            log.debug("Running in GUI-only mode")
        # if args.debug_qt_signals:
        #     enable_signal_debugging_simply()

        # ---------------------------------------------------------------------
        # Database
        # ---------------------------------------------------------------------
        # Get URL, or complain
        if args.dburl:
            set_database_url(args.dburl)
        if args.dbecho:
            set_database_echo(args.dbecho)
        try:
            database_url = get_database_url()
        except ValueError:
            if args.gui:
                win = NoDatabaseSpecifiedWindow()
                if args.guilog:
                    # noinspection PyUnboundLocalVariable
                    win.exit_kill_log.connect(log_window.exit)
                return run_gui(qt_app, win)
            raise ValueError(DATABASE_ENV_VAR_NOT_SPECIFIED)
        engine = create_engine(database_url)
        log.debug("Using database URL: {}".format(engine))  # obscures password

        # Has the user requested a command-line database upgrade?
        if args.upgrade_database:
            sys.exit(upgrade_database(ALEMBIC_CONFIG_FILENAME,
                                      ALEMBIC_BASE_DIR))
        # Is the database at the correct version?
        (current_revision, head_revision) = get_current_and_head_revision(
            database_url,
            ALEMBIC_CONFIG_FILENAME,
            ALEMBIC_BASE_DIR
        )
        if current_revision != head_revision:
            if args.gui:
                win = WrongDatabaseVersionWindow(current_revision,
                                                 head_revision)
                if args.guilog:
                    # noinspection PyUnboundLocalVariable
                    win.exit_kill_log.connect(log_window.exit)
                return run_gui(qt_app, win)
            raise ValueError(WRONG_DATABASE_VERSION_STUB.format(
                head_revision=head_revision,
                current_revision=current_revision))

        # ---------------------------------------------------------------------
        # Run app
        # ---------------------------------------------------------------------
        win = BaseWindow()
        if args.guilog:
            # noinspection PyUnboundLocalVariable
            win.exit_kill_log.connect(log_window.exit)
        return run_gui(qt_app, win)

    except:
        if args.guilog:
            log.critical(traceback.format_exc())
            log_window.set_may_close(True)
            return qt_app.exec_()
        else:
            raise


# =============================================================================
# Command-line entry point
# =============================================================================

if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        sys.exit(main())
    except Exception as e:  # master top-level exception catcher
        log.critical("Exception caught at top level: {}".format(str(e)))
        log.critical(traceback.format_exc())
        # Don't use print_exc(); that might not get sent to the log.
        sys.exit(1)
