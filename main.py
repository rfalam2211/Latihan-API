#import package
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel #parent class untuk buat schema di request body
import pandas as pd
from datetime import datetime
#membuat objek FastAPI
app = FastAPI()

# variable password
password = 'KERJAgaji666'


# membuat endpoint-> ketentuan untuk client membuat request
# function (get, put, post, delete)
# url (/...)


# endpoint untuk menampilkan pesan "Selamat Datang"
@app.get('/')
def getWelcome():
    return {
        "msg": "Selamat Datang King!"
    }

#endpoint untuk menampilkan semua isi dataset
@app.get("/profile")
def getData():
    #mengambil data dari csv
    df = pd.read_csv('teams.csv')

    #mengembalikan respons isi dataset
    return df.to_dict(orient='records')

#routing/path parameter--> url dinamis--> menyesuaikan dengan data yang ada di server
# endpoint untuk menampilkan data sesuai dengan lokasi
# data dari school ->/data/school

@app.get("/data/{school_names}")
def getData(school_name: str):

    #mengambil data dari csv
    df = pd.read_csv('teams.csv')

    # filter data berdasarkan parameter
    result = df[df.school_name == school_name]

    #validate hasuk data
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail='Data gaada nih brok')

    #mengembalikan respons isi dataset
    return result.to_dict(orient='records')

# endpoint untuk menghapus data berdasarkan school name
@app.delete('/data/{id}')
def deleteData(id: int, api_key: str = Header(None)):

    #proses authentication
    if api_key == None and api_key != password:
        # kalau tidak ada api_key/password salah muncul pesan -> Hayo siapa kamu
         raise HTTPException(status_code=401, detail='Hayo siapa kamu')


    #mengambil data dari csv
    df = pd.read_csv('teams.csv')

    #cek data apakah ada
    result = df[df.id == id]

    if len(result) == 0:
        #jika tidak ada
        #menampilkan pesar error --> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Datanya gaada bro")
    
    #proses hapus data
    #condition

    result = df[df.id != id ]


    result.to_csv('teams.csv', index=False)

    #mengembalikan respons isi dataset
    return {
        'msg' : 'Data sudah dihapus'
    }

class Profile(BaseModel):
    division: str
    conference: str
    school_name: str
    roster_url: str
    id: int

# endpoint untuk menambah data baru 
@app.post('/data')
def createData(profile: Profile):
    #melakukan proses pengambilan data dari csv
    df = pd.read_csv('teams.csv')

    #proses menambahkan data
    #concat
    newData = pd.DataFrame({
        'division': [profile.division],
        'conference' : [profile.conference],
        'school_name' : [profile.school_name],
        'roster_url' : [profile.roster_url],
        'id': [profile.id]
    })
  

    #concat
    df = pd.concat([df, newData])

    #update dataset
    df.to_csv('teams.csv', index=False)

    return {
        'msg':"Data sudah ditambah"
    }

