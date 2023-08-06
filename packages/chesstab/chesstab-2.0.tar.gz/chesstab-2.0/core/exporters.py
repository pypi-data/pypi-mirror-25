# exporters.py
# Copyright 2013 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess game, repertoire, and partial position exporters.
"""
# All the *_grid_* functions to take account of bookmarks (not completed yet)

import os

from basesup.api.bytebit import Bitarray#bitarray import bitarray

from pgn.core.parser import (PGNDisplay, PGNRepertoireDisplay)

from . import chessrecord, filespec
from .cqlstatement import CQLStatement


def export_games_as_text(database, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGameText()
    rr.set_database(database)
    gamesout = open(filename, 'w', encoding='iso-8859-1')
    cursor = database.database_cursor(
        filespec.GAMES_FILE_DEF, filespec.GAMES_FILE_DEF)
    try:
        r = cursor.first()
        while r:
            rr.load_record(r)
            a = rr.get_srvalue()
            gamesout.write(rr.get_srvalue())
            gamesout.write('\n')
            r = cursor.next()
    finally:
        cursor.close()
        gamesout.close()


def export_games_as_pgn(database, filename):
    """Export all records in dbfile to textfile in export format."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGame()
    rr.set_database(database)
    games_for_date = []
    prev_date = None
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.GAMES_FILE_DEF, filespec.PGN_DATE_FIELD_DEF)
    try:
        r = cursor.first()
        while r:
            if r[0] != prev_date:
                for gfd in sorted(games_for_date):
                    gamesout.write(''.join(gfd[0][1]))
                    gamesout.write(''.join(gfd[0][-1]))
                    gamesout.write(gfd[2])
                    gamesout.write(gfd[1])
                prev_date = r[0]
                games_for_date = []
            g = database.get_primary_record(filespec.GAMES_FILE_DEF, r[1])
            try:
                rr.load_record(g)
            except StopIteration:
                break
            if rr.value.is_pgn_valid():
                games_for_date.append(rr.value.get_export_pgn_elements())
            r = cursor.next()
        for gfd in sorted(games_for_date):
            gamesout.write(''.join(gfd[0][1]))
            gamesout.write(''.join(gfd[0][-1]))
            gamesout.write(gfd[2])
            gamesout.write(gfd[1])
    finally:
        cursor.close()
        gamesout.close()


def export_games_as_rav_pgn(database, filename):
    """Export all records in dbfile to textfile in export format."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGame()
    rr.set_database(database)
    games_for_date = []
    prev_date = None
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.GAMES_FILE_DEF, filespec.PGN_DATE_FIELD_DEF)
    try:
        r = cursor.first()
        while r:
            if r[0] != prev_date:
                for gfd in sorted(games_for_date):
                    gamesout.write(''.join(gfd[0][1]))
                    gamesout.write(''.join(gfd[0][-1]))
                    gamesout.write(gfd[2])
                    gamesout.write(gfd[1])
                prev_date = r[0]
                games_for_date = []
            g = database.get_primary_record(filespec.GAMES_FILE_DEF, r[1])
            try:
                rr.load_record(g)
            except StopIteration:
                break
            if rr.value.is_pgn_valid():
                games_for_date.append(rr.value.get_export_pgn_rav_elements())
            r = cursor.next()
        for gfd in sorted(games_for_date):
            gamesout.write(''.join(gfd[0][1]))
            gamesout.write(''.join(gfd[0][-1]))
            gamesout.write(gfd[2])
            gamesout.write(gfd[1])
    finally:
        cursor.close()
        gamesout.close()


def archive_games_as_pgn(database, filename):
    """Export all records in dbfile to textfile in reduced export format."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGame()
    rr.set_database(database)
    games_for_date = []
    prev_date = None
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.GAMES_FILE_DEF, filespec.PGN_DATE_FIELD_DEF)
    try:
        r = cursor.first()
        while r:
            if r[0] != prev_date:
                for gfd in sorted(games_for_date):
                    gamesout.write(''.join(gfd[0][1]))
                    gamesout.write(''.join(gfd[0][-1]))
                    gamesout.write(''.join(gfd[1]))
                prev_date = r[0]
                games_for_date = []
            g = database.get_primary_record(filespec.GAMES_FILE_DEF, r[1])
            try:
                rr.load_record(g)
            except StopIteration:
                break
            if rr.value.is_pgn_valid():
                games_for_date.append(rr.value.get_archive_pgn_elements())
            r = cursor.next()
        for gfd in sorted(games_for_date):
            gamesout.write(''.join(gfd[0][1]))
            gamesout.write(''.join(gfd[0][-1]))
            gamesout.write(''.join(gfd[1]))
    finally:
        cursor.close()
        gamesout.close()


def export_repertoires_as_pgn(database, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordRepertoire()
    rr.set_database(database)
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.REPERTOIRE_FILE_DEF, filespec.REPERTOIRE_FILE_DEF)
    try:
        r = cursor.first()
        while r:
            rr.load_record(r)
            if rr.value.is_pgn_valid():
                gamesout.write(rr.value.get_export_repertoire_text())
            r = cursor.next()
    finally:
        cursor.close()
        gamesout.close()


def export_repertoires_as_rav_pgn(database, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordRepertoire()
    rr.set_database(database)
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.REPERTOIRE_FILE_DEF, filespec.REPERTOIRE_FILE_DEF)
    try:
        r = cursor.first()
        while r:
            rr.load_record(r)
            if rr.value.is_pgn_valid():
                gamesout.write(rr.value.get_export_repertoire_rav_text())
            r = cursor.next()
    finally:
        cursor.close()
        gamesout.close()


def export_repertoires_as_text(database, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGameText()
    rr.set_database(database)
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.REPERTOIRE_FILE_DEF, filespec.REPERTOIRE_FILE_DEF)
    try:
        r = cursor.first()
        while r:
            rr.load_record(r)
            gamesout.write(rr.get_srvalue())
            gamesout.write('\n')
            r = cursor.next()
    finally:
        cursor.close()
        gamesout.close()


def export_positions(database, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordPartial()
    rr.set_database(database)
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.PARTIAL_FILE_DEF, filespec.PARTIAL_FILE_DEF)
    try:
        r = cursor.first()
        while r:
            rr.load_record(r)
            gamesout.write(rr.get_srvalue())
            gamesout.write('\n')
            r = cursor.next()
    finally:
        cursor.close()
        gamesout.close()


def export_grid_games_as_pgn(grid, filename):
    """Export all records in dbfile to textfile in export format."""
    if filename is None:
        return
    if grid.bookmarks:
        database = grid.get_data_source().dbhome
        primary = database.is_primary(
            grid.get_data_source().dbset, grid.get_data_source().dbname)
        rr = chessrecord.ChessDBrecordGame()
        rr.set_database(database)
        games = []
        for b in grid.bookmarks:
            if primary:
                rr.load_record(
                    database.get_primary_record(filespec.GAMES_FILE_DEF, b[0]))
            else:
                rr.load_record(
                    database.get_primary_record(filespec.GAMES_FILE_DEF, b[1]))
            if rr.value.is_pgn_valid():
                games.append(rr.value.get_export_pgn_elements())
        gamesout = open(filename, 'w')
        try:
            for g in sorted(games):
                gamesout.write(''.join(g[0][1]))
                gamesout.write(''.join(g[0][-1]))
                gamesout.write(''.join(g[2]))
                gamesout.write(''.join(g[1]))
        finally:
            gamesout.close()
        return
    elif grid.partial:
        database = grid.get_data_source().dbhome
        cursor = database.database_cursor(
            grid.get_data_source().dbset, grid.get_data_source().dbset)
        try:
            r = cursor.last()
            if r is None:
                return
        finally:
            cursor.close()
        ba = Bitarray(r[0] + 1)
        ba.setall(False)
        primary = database.is_primary(
            grid.get_data_source().dbset, grid.get_data_source().dbname)
        cursor = grid.get_cursor()
        try:
            cursor.set_partial_key(grid.partial)
            r = cursor.last()
            if r is None:
                return
            while r:
                ba[r[1]] = True
                r = cursor.prev()
            export_partial_games_as_pgn(database, filename, ba)
            return
        finally:
            cursor.close()
    else:
        export_games_as_pgn(grid.get_data_source().dbhome, filename)
        return


def export_grid_games_as_rav_pgn(grid, filename):
    """Export all records in dbfile to textfile in export format."""
    if filename is None:
        return
    if grid.bookmarks:
        database = grid.get_data_source().dbhome
        primary = database.is_primary(
            grid.get_data_source().dbset, grid.get_data_source().dbname)
        rr = chessrecord.ChessDBrecordGame()
        rr.set_database(database)
        games = []
        for b in grid.bookmarks:
            if primary:
                rr.load_record(
                    database.get_primary_record(filespec.GAMES_FILE_DEF, b[0]))
            else:
                rr.load_record(
                    database.get_primary_record(filespec.GAMES_FILE_DEF, b[1]))
            if rr.value.is_pgn_valid():
                games.append(rr.value.get_export_pgn_rav_elements())
        gamesout = open(filename, 'w')
        try:
            for g in sorted(games):
                gamesout.write(''.join(g[0][1]))
                gamesout.write(''.join(g[0][-1]))
                gamesout.write(''.join(g[2]))
                gamesout.write(''.join(g[1]))
        finally:
            gamesout.close()
        return
    elif grid.partial:
        database = grid.get_data_source().dbhome
        cursor = database.database_cursor(
            grid.get_data_source().dbset, grid.get_data_source().dbset)
        try:
            r = cursor.last()
            if r is None:
                return
        finally:
            cursor.close()
        ba = Bitarray(r[0] + 1)
        ba.setall(False)
        primary = database.is_primary(
            grid.get_data_source().dbset, grid.get_data_source().dbname)
        cursor = grid.get_cursor()
        try:
            cursor.set_partial_key(grid.partial)
            r = cursor.last()
            if r is None:
                return
            while r:
                ba[r[1]] = True
                r = cursor.prev()
            export_partial_games_as_rav_pgn(database, filename, ba)
            return
        finally:
            cursor.close()
    else:
        export_games_as_rav_pgn(grid.get_data_source().dbhome, filename)
        return


def archive_grid_games_as_pgn(grid, filename):
    """Export all records in dbfile to textfile in reduced export format."""
    if filename is None:
        return
    if grid.bookmarks:
        database = grid.get_data_source().dbhome
        primary = database.is_primary(
            grid.get_data_source().dbset, grid.get_data_source().dbname)
        rr = chessrecord.ChessDBrecordGame()
        rr.set_database(database)
        games = []
        for b in grid.bookmarks:
            if primary:
                rr.load_record(
                    database.get_primary_record(filespec.GAMES_FILE_DEF, b[0]))
            else:
                rr.load_record(
                    database.get_primary_record(filespec.GAMES_FILE_DEF, b[1]))
            if rr.value.is_pgn_valid():
                games.append(rr.value.get_archive_pgn_elements())
        gamesout = open(filename, 'w')
        try:
            for g in sorted(games):
                gamesout.write(''.join(g[0][1]))
                gamesout.write(''.join(g[0][-1]))
                gamesout.write(''.join(g[1]))
        finally:
            gamesout.close()
        return
    elif grid.partial:
        database = grid.get_data_source().dbhome
        cursor = database.database_cursor(
            grid.get_data_source().dbset, grid.get_data_source().dbset)
        try:
            r = cursor.last()
            if r is None:
                return
        finally:
            cursor.close()
        ba = Bitarray(r[0] + 1)
        ba.setall(False)
        primary = database.is_primary(
            grid.get_data_source().dbset, grid.get_data_source().dbname)
        cursor = grid.get_cursor()
        try:
            cursor.set_partial_key(grid.partial)
            r = cursor.last()
            if r is None:
                return
            while r:
                ba[r[1]] = True
                r = cursor.prev()
            archive_partial_games_as_pgn(database, filename, ba)
            return
        finally:
            cursor.close()
    else:
        archive_games_as_pgn(grid.get_data_source().dbhome, filename)
        return


def export_grid_repertoires_as_pgn(grid, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    if grid.bookmarks:
        database = grid.get_data_source().dbhome
        rr = chessrecord.ChessDBrecordRepertoire()
        rr.set_database(database)
        gamesout = open(filename, 'w')
        try:
            for b in sorted(grid.bookmarks):
                rr.load_record(
                    database.get_primary_record(
                        filespec.REPERTOIRE_FILE_DEF, b[0]))
                if rr.value.is_pgn_valid():
                    gamesout.write(rr.value.get_export_repertoire_text())
            gamesout = open(filename, 'w')
        finally:
            gamesout.close()
        return
    else:
        export_repertoires_as_pgn(grid.get_data_source().dbhome, filename)
        return


def export_grid_repertoires_as_rav_pgn(grid, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    if grid.bookmarks:
        database = grid.get_data_source().dbhome
        rr = chessrecord.ChessDBrecordRepertoire()
        rr.set_database(database)
        gamesout = open(filename, 'w')
        try:
            for b in sorted(grid.bookmarks):
                rr.load_record(
                    database.get_primary_record(
                        filespec.REPERTOIRE_FILE_DEF, b[0]))
                if rr.value.is_pgn_valid():
                    gamesout.write(rr.value.get_export_repertoire_rav_text())
            gamesout = open(filename, 'w')
        finally:
            gamesout.close()
        return
    else:
        export_repertoires_as_rav_pgn(grid.get_data_source().dbhome, filename)
        return


def export_grid_positions(grid, filename):
    """Export all records in dbfile to textfile."""
    if filename is None:
        return
    if grid.bookmarks:
        database = grid.get_data_source().dbhome
        rr = chessrecord.ChessDBrecordPartial()
        rr.set_database(database)
        gamesout = open(filename, 'w')
        try:
            for b in sorted(grid.bookmarks):
                rr.load_record(
                    database.get_primary_record(
                        filespec.PARTIAL_FILE_DEF, b[0]))
                gamesout.write(rr.get_srvalue())
                gamesout.write('\n')
            gamesout = open(filename, 'w')
        finally:
            gamesout.close()
        return
    else:
        database = grid.get_data_source().dbhome
        rr = chessrecord.ChessDBrecordPartial()
        rr.set_database(database)
        gamesout = open(filename, 'w')
        cursor = database.database_cursor(
            filespec.PARTIAL_FILE_DEF, filespec.PARTIAL_FILE_DEF)
        try:
            r = cursor.first()
            while r:
                rr.load_record(r)
                gamesout.write(rr.get_srvalue())
                gamesout.write('\n')
                r = cursor.next()
        finally:
            cursor.close()
            gamesout.close()
        return


def export_partial_games_as_pgn(database, filename, partialset):
    """Export all records in dbfile to textfile in export format."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGame()
    rr.set_database(database)
    games_for_date = []
    prev_date = None
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.GAMES_FILE_DEF, filespec.PGN_DATE_FIELD_DEF)
    try:
        r = cursor.first()
        while r:
            if r[0] != prev_date:
                for gfd in sorted(games_for_date):
                    gamesout.write(''.join(gfd[0][1]))
                    gamesout.write(''.join(gfd[0][-1]))
                    gamesout.write(gfd[2])
                    gamesout.write(gfd[1])
                prev_date = r[0]
                games_for_date = []
            if partialset[r[1]]:
                g = database.get_primary_record(filespec.GAMES_FILE_DEF, r[1])
                rr.load_record(g)
                if rr.value.is_pgn_valid():
                    games_for_date.append(rr.value.get_export_pgn_elements())
            r = cursor.next()
        for gfd in sorted(games_for_date):
            gamesout.write(''.join(gfd[0][1]))
            gamesout.write(''.join(gfd[0][-1]))
            gamesout.write(gfd[2])
            gamesout.write(gfd[1])
    finally:
        cursor.close()
        gamesout.close()


def export_partial_games_as_rav_pgn(database, filename, partialset):
    """Export all records in dbfile to textfile in export format."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGame()
    rr.set_database(database)
    games_for_date = []
    prev_date = None
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.GAMES_FILE_DEF, filespec.PGN_DATE_FIELD_DEF)
    try:
        r = cursor.first()
        while r:
            if r[0] != prev_date:
                for gfd in sorted(games_for_date):
                    gamesout.write(''.join(gfd[0][1]))
                    gamesout.write(''.join(gfd[0][-1]))
                    gamesout.write(gfd[2])
                    gamesout.write(gfd[1])
                prev_date = r[0]
                games_for_date = []
            if partialset[r[1]]:
                g = database.get_primary_record(filespec.GAMES_FILE_DEF, r[1])
                rr.load_record(g)
                if rr.value.is_pgn_valid():
                    games_for_date.append(
                        rr.value.get_export_pgn_rav_elements())
            r = cursor.next()
        for gfd in sorted(games_for_date):
            gamesout.write(''.join(gfd[0][1]))
            gamesout.write(''.join(gfd[0][-1]))
            gamesout.write(gfd[2])
            gamesout.write(gfd[1])
    finally:
        cursor.close()
        gamesout.close()


def archive_partial_games_as_pgn(database, filename, partialset):
    """Export all records in dbfile to textfile in reduced export format."""
    if filename is None:
        return
    rr = chessrecord.ChessDBrecordGame()
    rr.set_database(database)
    games_for_date = []
    prev_date = None
    gamesout = open(filename, 'w')
    cursor = database.database_cursor(
        filespec.GAMES_FILE_DEF, filespec.PGN_DATE_FIELD_DEF)
    try:
        r = cursor.first()
        while r:
            if r[0] != prev_date:
                for gfd in sorted(games_for_date):
                    gamesout.write(''.join(gfd[0][1]))
                    gamesout.write(''.join(gfd[0][-1]))
                    gamesout.write(''.join(gfd[1]))
                prev_date = r[0]
                games_for_date = []
            if partialset[r[1]]:
                g = database.get_primary_record(filespec.GAMES_FILE_DEF, r[1])
                rr.load_record(g)
                if rr.value.is_pgn_valid():
                    games_for_date.append(rr.value.get_archive_pgn_elements())
            r = cursor.next()
        for gfd in sorted(games_for_date):
            gamesout.write(''.join(gfd[0][1]))
            gamesout.write(''.join(gfd[0][-1]))
            gamesout.write(''.join(gfd[1]))
    finally:
        cursor.close()
        gamesout.close()


def archive_single_game_as_pgn(game, filename):
    """Export game to textfile in reduced export format."""
    if filename is None:
        return
    pgn = PGNDisplay()
    pgn.get_first_game(game)
    if not pgn.is_pgn_valid():
        return
    g = pgn.get_archive_pgn_elements()
    gamesout = open(filename, 'w')
    try:
        gamesout.write(''.join(g[0][1]))
        gamesout.write(''.join(g[0][-1]))
        gamesout.write(g[1])
    finally:
        gamesout.close()


def export_single_game_as_pgn(game, filename):
    """Export all records in dbfile to textfile in export format."""
    if filename is None:
        return
    pgn = PGNDisplay()
    pgn.get_first_game(game)
    if not pgn.is_pgn_valid():
        return
    g = pgn.get_export_pgn_elements()
    gamesout = open(filename, 'w')
    try:
        gamesout.write(''.join(g[0][1]))
        gamesout.write(''.join(g[0][-1]))
        gamesout.write(g[2])
        gamesout.write(g[1])
    finally:
        gamesout.close()


def export_single_game_as_rav_pgn(game, filename):
    """Export game to textfile in export format."""
    if filename is None:
        return
    pgn = PGNDisplay()
    pgn.get_first_game(game)
    if not pgn.is_pgn_valid():
        return
    g = pgn.get_export_pgn_rav_elements()
    gamesout = open(filename, 'w')
    try:
        gamesout.write(''.join(g[0][1]))
        gamesout.write(''.join(g[0][-1]))
        gamesout.write(g[2])
        gamesout.write(g[1])
    finally:
        gamesout.close()


def export_single_repertoire_as_pgn(repertoire, filename):
    """Export repertoire like PGN to textfile."""
    if filename is None:
        return
    pgn = PGNRepertoireDisplay()
    pgn.get_first_game(repertoire)
    if not pgn.is_pgn_valid():
        return
    gamesout = open(filename, 'w')
    try:
        gamesout.write(pgn.get_export_repertoire_text())
    finally:
        gamesout.close()


def export_single_repertoire_as_rav_pgn(repertoire, filename):
    """Export repertoire like RAV PGN to textfile."""
    if filename is None:
        return
    pgn = PGNRepertoireDisplay()
    pgn.get_first_game(repertoire)
    if not pgn.is_pgn_valid():
        return
    gamesout = open(filename, 'w')
    try:
        gamesout.write(pgn.get_export_repertoire_rav_text())
    finally:
        gamesout.close()


def export_single_position(partialposition, filename):
    """Export partial position to textfile."""
    if filename is None:
        return
    pgn = CQLStatement()
    pgn.process_cql_statement(partialposition)
    if not pgn.is_cql_statement():
        return
    gamesout = open(filename, 'w')
    try:
        gamesout.write(pgn.get_name_position_text())
    finally:
        gamesout.close()
