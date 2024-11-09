from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import sqlite3

ERROR_MESSAGE = "해당 id의 paste가 존재하지 않습니다."

app = FastAPI()
conn = sqlite3.connect('answer.db', check_same_thread=False)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Paste (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 content TEXT);''')
conn.commit()

class Paste(BaseModel):
    content: str

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/paste/{paste_id}')
def get_paste(paste_id: int):
    res = cur.execute('''SELECT id, content
                      FROM Paste
                      WHERE id = ?''', (paste_id,))
    data = res.fetchone()

    if data is None:
        raise HTTPException(status_code = 404, detail = ERROR_MESSAGE)
    
    paste = Paste(content=data[1])
    return {'paste_id': data[0],
            'paste': paste}

@app.get('/paste/')
def get_pastes():
    res = cur.execute('''SELECT id, content
                      FROM Paste''')
    data = res.fetchall()

    return [{'paste_id': row[0], 'content': row[1]} for row in data]

@app.post('/paste/')
def post_paste(paste: Paste):
    cur.execute('''INSERT INTO Paste (content)
                         VALUES (?)''', (paste.content,))
    conn.commit()
    paste_id = cur.lastrowid
    return {'paste_id': paste_id,
            'paste': paste}

@app.put('/paste/{paste_id}')
def put_paste(paste_id: int, paste: Paste):
    res = cur.execute('''SELECT id
                      FROM Paste
                      WHERE id = ?''', (paste_id,))
    if res.fetchone() is None:
        raise HTTPException(status_code = 404, detail = ERROR_MESSAGE)

    cur.execute('''UPDATE Paste
                SET content = ?
                WHERE id = ?''', (paste.content, paste_id))
    conn.commit()
    
    return {'paste_id': paste_id,
            'paste': paste}

@app.delete('/paste/{paste_id}')
def delete_paste(paste_id:int):
    res = cur.execute('''SELECT id
                      FROM Paste
                      WHERE id = ?''', (paste_id,))
    if res.fetchone() is None:
        raise HTTPException(status_code = 404, detail = ERROR_MESSAGE)
    
    cur.execute('''DELETE
                FROM Paste
                WHERE id = ?''', (paste_id,))
    conn.commit()
    
    return Response(status_code=204)
