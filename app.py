from flask import Flask,render_template,request,redirect
import pymysql
conn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        db='pyapp',
                        user='root',
                        passwd='java1004')
# print(conn)
app = Flask(__name__)


# msg_add.html 폼
@app.route('/add_msg', methods=['GET', 'POST'])
def add_msg():
    if request.method == 'GET':
        return render_template('add_msg.html')
    elif request.method == 'POST':
        msg_text = request.form['msg_text']
        # db 입력
        cursor = conn.cursor()
        cursor.execute('INSERT INTO msg(msg_text) VALUES(%s)',[msg_text])
        conn.commit()   
        return redirect('/')

# msg 목록
@app.route('/', methods=['GET'])
def msg_list():
   cursor = conn.cursor()
   cursor.execute('SELECT msg_id, msg_text FROM msg')
   msglist = cursor.fetchall() # cursor.fetchone()
   print(msglist)
   return render_template('msg_list.html',msglist = msglist) 

# msg 삭제
@app.route('/del_msg', methods=['GET'])
def del_msg():
    msg_id = request.args.get('msg_id')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM msg WHERE msg_id=%s', [msg_id])
    conn.commit()
    return redirect('/')
# msg 수정
@app.route('/modify_msg', methods=['GET','POST'])
def modify_msg():
    if request.method == 'GET': #수정폼
        msg_id = request.args.get('msg_id')

        cursor = conn.cursor()
        cursor.execute('select msg_id,msg_text from msg where msg_id=%s',[msg_id])
        msg = cursor.fetchone()

        print(msg)

        return render_template('modify_msg.html',msg = msg)
    elif request.method == 'POST': #수정액션
        msg_id = request.form['msg_id']
        msg_text = request.form['msg_text']

        #데이터베이스 입력
        cursor = conn.cursor()
        cursor.execute('update msg set msg_text=%s where msg_id=%s',[msg_text,msg_id])
        conn.commit()

        return redirect('/')
    
app.run(host='127.0.0.1', port=80)