from flask import Flask,render_template,request
from flask_pymongo import PyMongo
from pymongo import MongoClient

app= Flask(__name__)


#app.config['MONGO_URI']='mongodb://localhost:27017/Hostel_leave'
client=MongoClient('mongodb://localhost:27017/')
#mongo= PyMongo(app)

db=client['Hostel']
collection=db['Leave_apply']
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='GET':
        documents = collection.find()
        for record in documents:
            print(record)
        return render_template('index.html')
    else:
        fname=(request.form.get('name'))
        reg_no=request.form.get('Reg')
        room=request.form.get('Room')
        From=request.form.get('From')
        To=request.form.get('TO')
        reason=request.form.get('Reason')

        data={
            'Name':fname,
            'Register Number':reg_no,
            'Room Number': room,
            'From':From,
            'To':To,
            'Reason':reason
        }
        #name,Reg,Room,From,To,Reason
        
        #data=request.form
        print(data)
        collection.insert_one(data)
        #mongo.db.record.insert(dict(Name=data['name'],Register_No=data['Reg'],Room_no=data['Room'],From=data['From'],To=data['TO'],Reason=data['Reason']))

        return 'Your leave applied successfully'


@app.route('/admin')
def admin():
    data=collection.find()
    return render_template('admin.html',data=data)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)