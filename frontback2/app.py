from flask import Flask,render_template,request


app = Flask(__name__)

@app.route('/',methods=['GET'])
def homepage():
    return render_template('response.html',response="welcome to homepage")

@app.route('/user',methods=['GET'])
def user():
    return render_template('form.html',path='/user-data')

import pymysql as sql
my_connection = sql.connect(
    host= 'localhost',
    user= 'root',
    passwd= 'password#123',
    database= 'nrcm1'
)
my_cursor = my_connection.cursor()

@app.route('/user-data',methods=['POST'])
def user_data():
    u_id = request.form['u_id']
    u_name = request.form['u_name']
    u_age = request.form['u_age']
    u_salary = request.form['u_salary']

    query = '''
        insert into register(u_id,u_name,u_age,u_salary)
        values(%s,%s,%s,%s);
     '''

    values=(u_id,u_name,u_age,u_salary)
    my_cursor.execute(query,values)
    my_connection.commit()
    return render_template('response.html',response='DATA INSERTED,CHECK IN MYSQL') 

@app.route('/view',methods=['GET'])
def view():
    query= '''
     select * from register;
   '''
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    return render_template('response.html',response=data)

@app.route('/update',methods=['GET'])
def update():
    return render_template('update.html',path='/update-form')

@app.route('/update-form',methods=['POST'])
def update_form():
    u_id = request.form['u_id']
    u_age = request.form['u_age']
    query = '''
        update register
        set u_age= (%s)
        where u_id = (%s);
    '''
    values=(u_age,u_id)
    my_cursor.execute(query,values)
    my_connection.commit()
    return render_template('response.html',response=f'{u_id} age has been updated')

@app.route('/delete/<_id>',methods =['GET'])
def delete(_id):
    query = '''
        delete from register
        where u_id = %s
    '''
    values = (_id)
    my_cursor.execute(query,values)
    my_connection.commit()
    return render_template('response.html',response=f'user having u_id{_id} has been deleted')
