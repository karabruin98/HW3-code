from flask import Flask,render_template,request,flash,session,redirect,url_for,g
import sqlite3
from  sqlite3 import Error
import json
import random
app = Flask(__name__)


#获取数据库连接
def Get_message_db():
    
    try:
        return g.message_db
    except:  
        g.message_db = sqlite3.connect("messages_db.sqlite")
        #创建数据库消息表
        cmd = 'CREATE TABLE IF NOT EXISTS message(id INTEGER PRIMARY KEY AUTOINCREMENT,name text, msg text )' # replace this with your SQL query
        #获取游标对象
        cursor = g.message_db.cursor()
        #执行sql
        cursor.execute(cmd)
        #返回连接对象
        return g.message_db
  
#自定义关闭连接方法
def close_conn(conn, cursor):
     if cursor:
         cursor.close()
     if conn:
         conn.close()


#插入消息方法
def Insert_message(request):
    #获取消息相关参数字段
    name= request.form.get("name",'')
    msg= request.form.get("msg",'')
    #获取连接对象
    con=Get_message_db()
    #获取游标对象
    cursor=con.cursor()
    sql="insert into message values(null,'{name}','{msg}')".format(name=name,msg=msg)
    cursor.execute(sql)
    #提交事务 
    con.commit()
    #关闭连接
    close_conn(con,cursor)
    return None
#随机信息方法
def random_messages(n):
    
    if n>=5:
        n=5
    #信息结果集
    result=[]
    
    sql="SELECT * FROM message ORDER BY RANDOM() LIMIT 1;"
    #循环随机获取数据信息
    for i in range(n):
        con=Get_message_db()
        cursor=con.cursor()
        cursor.execute(sql)
        temp=cursor.fetchone()
        result.append(temp)
    close_conn(con,cursor)
    return  result
    
    
@app.route('/',methods= ["GET"])
def index():
    return redirect(url_for("Insert"))   
@app.route('/Insert',methods=["POST","GET"])
#插入信息路由
def Insert():
    #get请求直接返回模板页面
    if request.method=='GET':
        
        return render_template('submit.html')
          
    elif request.method=='POST':
        Insert_message(request)
        return render_template('submit.html')
#查看信息路由
@app.route('/View',methods=["GET"])
def View():
    #获取3条随机信息
    msgs=random_messages(3)

    return render_template('view.html',msgs=msgs)
          





if __name__ == '__main__':
    app.run(debug=True, port = 5001)
    
