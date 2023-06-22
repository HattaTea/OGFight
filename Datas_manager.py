# coding : utf-8

import sqlite3
import os


"""
    OGFight - Simulateur de combat pour Ogame FDV
    Copyright (C) 2023  HattaTea
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""



class Datas_manager:

    def __init__(self):
        if not os.path.exists("/datas.db"):
            self.create()
        
    def create(self):
        con = sqlite3.connect("datas.db")
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE  IF NOT EXISTS rapports(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            name TEXT,
            liste TEXT NOT NULL UNIQUE
            )
            """)
        con.commit()
        con.close()
        

    def add_rapport(self, liste):
        con = sqlite3.connect("datas.db")
        cur = con.cursor()
        datas = [liste]
        cur.executemany(
            """
            INSERT INTO rapports(date, name, liste) VALUES(?, ?, ?)
            """, datas)
        con.commit()
        con.close()

    def load(self):
        con = sqlite3.connect("datas.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM rapports")
        res = cur.fetchall()
        con.close()
        return res
