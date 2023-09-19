from flask import Flask,render_template,request,render_template_string,jsonify,redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

app= Flask(__name__)


#app.config['MONGO_URI']='mongodb://localhost:27017/Hostel_leave'
client=MongoClient('mongodb://localhost:27017/')
#mongo= PyMongo(app)

db=client['Hostel']
collection=db['Leave_apply']
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='GET':
      return render_template('index.html')
    else:
        fname=(request.form.get('name'))
        reg_no=int(request.form.get('Reg'))
        room=request.form.get('Room')
        From=request.form.get('From')
        To=request.form.get('TO')
        reason=request.form.get('Reason')
        submitted='submitted'

        data={
            'Name':fname,
            'Register Number':reg_no,
            'Room Number': room,
            'From':From,
            'To':To,
            'Reason':reason,
            'status':submitted
        }
        #name,Reg,Room,From,To,Reason
        
        #data=request.form
        print(data)
        collection.insert_one(data)
        #mongo.db.record.insert(dict(Name=data['name'],Register_No=data['Reg'],Room_no=data['Room'],From=data['From'],To=data['TO'],Reason=data['Reason']))

        return 'Your leave applied successfully'


@app.route('/admin')
def admin():
    data=list(collection.find())
    return render_template('admin.html',data=data)
@app.route('/adminlist')
def adminlist():
    cursor=collection.find({},{"Name": 1,"Register Number":1,"Room Number":1,"From":1,"To":1,"Reason":1})

    print(cursor)
    data = [document for document in cursor]
    #print(data)
    #return json.loads(json_util.dumps(data))
    #return jsonify(data)
    page_sanitized = json.loads(json_util.dumps(data))
    return page_sanitized


@app.route('/checkStatus',methods=['POST','GET'])
def checkStatus():
    if request.method=='POST':
        id=int(request.form.get('id'))
        print(id)
        fdata=collection.find_one({"Register Number":id},{"_id":0})
        print(fdata)
        return render_template('search.html',data=fdata)
    else:   
        return render_template('check.html')

@app.route('/approve')
def approve():
    a=int(request.args.get('register_number'))
    cdata=collection.update_one({"Register Number":a}, {"$set": {"status":'Approved'}})
   
    return render_template_string('leave approved successfully')

@app.route('/reject')
def reject():
    a=int(request.args.get('register_number'))
    cdata=collection.update_one({"Register Number":a}, {"$set": {"status":'Rejected'}})
   
    return render_template_string('Leave Rejected successfully')

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)