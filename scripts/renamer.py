import glob
import os
import sqlite3 as sq
from collections import defaultdict
from contextlib import closing

if __name__ == "__main__":
    with closing(sq.connect("card_list.sqlite")) as conn:

        conn.execute(
        """
        UPDATE card_list
        SET "references" = NULL
        WHERE card_name = 'The Legendary Gambler'
        """).fetchall()

        conn.commit()
