from flask import Flask, render_template, request
import sqlite3 as sql

conn = sql.connect('pendapatan.db')
print ("membuat database baru");
conn.execute('CREATE TABLE IF NOT EXISTS mingguan (id INTEGER NOT NULL PRIMARY KEY, biayaiklan VARCHAR, keuntungan VARCHAR, nik INTEGER NOT NULL, notelp INTEGER NOT NULL, namaortu VARCHAR )');
print ("Tabel berhasil dibuat");
conn.close()
app = Flask(__name__)

@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/')
def login():
    return render_template("Login.html")

@app.route('/enternew')
def new_student():
   return render_template('datamingguan.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         id = request.form['id']
         bi = request.form['bi']
         keu = request.form['keu']
         nik = request.form['nik']
         notelp = request.form['notelp']
         namaortu = request.form['namaortu']
                  
         with sql.connect("pendapatan.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO mingguan (id,biayaiklan,keuntungan,nik,notelp,namaortu) VALUES (?,?,?,?,?,?)",(id,bi,keu,nik,notelp,namaortu) )
            con.commit()
            msg = "Record berhasil ditambahkan"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("pendapatan.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from mingguan")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)
if __name__ == '__main__':
   app.run(debug = True)