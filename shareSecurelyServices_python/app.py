from flask import Flask, render_template,request,redirect,url_for,abort,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


from flask_bcrypt import Bcrypt


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


import sqlite3


app = Flask(__name__)
hashBcryptObject = Bcrypt(app)


from base64 import b64encode
from io import BytesIO


#connect appfiles to database files
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meg@bite001@localhost/sharesecureservices'


admin = Admin(app, name='Control Panel')


app.app_context().push()
#DB Instance
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'DB@Security112523'


#package which handles logging between flask and app 
init_manager_login = LoginManager()
init_manager_login.init_app(app)
init_manager_login.login_view = "login"


#reload user ids stored in the session
@init_manager_login.user_loader
def load_user(user_id):
    return registeredusers.query.get(int(user_id))


#creating tables
class registeredusers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    useremail = db.Column(db.String, nullable=False, unique=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    isadmin = db.Column(db.Boolean, default=False)
    userActive = db.Column(db.Boolean, default=False)
    

class groups(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)   
    groupname = db.Column(db.String, nullable=False, unique=True)
    groupdesc = db.Column(db.String, nullable=False)
    useremail = db.Column(db.String, nullable=False)
    isowner = db.Column(db.Boolean, default=False)

class groupentries(db.Model, UserMixin):
    __table_args__ = (
        db.UniqueConstraint('groupname', 'useremail', name='unique_groupentries'),
    )
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String, nullable=False)
    useremail = db.Column(db.String, nullable=False)
    userActive = db.Column(db.Boolean, default=False)

class itementries(db.Model, UserMixin):
    __table_args__ = (
        db.UniqueConstraint('groupname', 'itemname', name='unique_itementries'),
    )
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String, nullable=False)
    itemname = db.Column(db.String, nullable=False)
    itemContent = db.Column(db.LargeBinary, nullable=False)
    useremail = db.Column(db.String, nullable=False)

class itemfeedbackentries(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String, nullable=False)
    itemname = db.Column(db.String, nullable=False)
    itemfeedback = db.Column(db.String, nullable=False)
    useremail = db.Column(db.String, nullable=False)



class Controller(ModelView):
    def is_accessible(self):
        if current_user.isadmin:
            return current_user.is_authenticated
        else:
            return abort(404)
            #return redirect(url_for('userHome'))
    def not_auth(self):
        return "Authentication Required"


admin.add_view(Controller(registeredusers, db.session))
admin.add_view(Controller(groups, db.session))
admin.add_view(Controller(groupentries, db.session))


# User Login Page
@app.route('/')
def loginPage():
    try:
        sqliteConnection = sqlite3.connect('instance/database.db')
        #D:\Workspace\PG\Python\Secure\Assignment3\instance\database.db
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")
        # Selecting record now

        viewGroupsQuery = """select distinct groupname from groups order by groupname"""
        #print(viewGroupsQuery)
        cursor.execute(viewGroupsQuery)
        grpdetails0=[]
        rs = cursor.fetchall()
        for i in rs:
            groupname = i[0]
            grpdetails0.append(groupname)

        #print("Record retrieved successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("the sqlite connection is closed")
    return render_template('UserLogin.html', availablegroups = grpdetails0)


# User register
@app.route('/registerNewUser', methods = ['Post','Get']) 
def registerNewUser():
    if request.method == 'POST':
        #print("Here 2")
        registerUserEmail = request.form['signup_email']
        #print(registerUserEmail)

        registerFirstName = request.form['signup_fname']
        #print(registerFirstName)
        registerLastName = request.form['signup_lname']
        #print(registerLastName)
        registerUserPass = request.form['signup_confirmpassword']
        #print(registerUserPass)
        hashedPass = hashBcryptObject.generate_password_hash(registerUserPass).decode('utf-8')
        #print(hashedPass)
        registerUserGroups = ','.join(request.form.getlist('signup_group'))
        #print(registerUserGroups)

        check_email_present = registeredusers.query.filter_by(
            useremail=registerUserEmail).first()

        boolValid = validateUserInputInUserRegistration(registerUserEmail, registerFirstName, registerLastName, registerUserPass, registerUserGroups)    

        if boolValid:
            if check_email_present:
                return redirect(url_for('registerusercopy'))        

            objectRegisterNewUser = registeredusers(useremail=registerUserEmail, firstname=registerFirstName,lastname=registerLastName,password=hashedPass)
            #objectApprovedUser = approvedusers(useremail=registerUserEmail, firstname=registerFirstName,lastname=registerLastName,groups=registerUserGroups)
            db.session.add(objectRegisterNewUser)
            x = registerUserGroups.split(",")
            for i in x:
                db.session.add(groupentries(groupname=i, useremail=registerUserEmail))
            db.session.commit()
            return redirect(url_for('loginPage'))
        else:
            return redirect(url_for('loginPage'))
    else:
        return redirect(url_for('loginPage'))


def validateUserInputInUserRegistration(registerUserEmail, registerFirstName, registerLastName, registerUserPass, registerUserGroups):
    if len(registerUserEmail) < 16 or len(registerUserEmail) > 31:
        return False
    if len(registerFirstName) < 5 or len(registerFirstName) > 31:
        return False
    if len(registerLastName) < 5 or len(registerLastName) > 31:
        return False
    if len(registerUserPass) < 5 or len(registerUserPass) > 31:
        return False
    return True

# User Login
@app.route('/loginUser', methods = ['Post','Get'])
def loginUser():
    if request.method == 'POST':
        #print("Here 3")
        loginUserEmail = request.form['login_email']
        #print(loginUserEmail)
        loginUserPass = request.form['login_password']
        #print(loginUserPass)
        #print(hashBcryptObject.generate_password_hash(loginUserPass).decode('UTF-8'))
        #check_this_user_present_approvedtable = approvedusers.query.filter_by(
            #useremail=loginUserEmail).first()        
        check_this_user_present_registeredTable = registeredusers.query.filter_by(
            useremail=loginUserEmail).first()
        if check_this_user_present_registeredTable:
            # user entry found
            if check_this_user_present_registeredTable.userActive:
                # active user
                if hashBcryptObject.check_password_hash(check_this_user_present_registeredTable.password,loginUserPass):
                    # correct password
                    login_user(check_this_user_present_registeredTable)
                    return redirect(url_for('userHome'))
                else:
                    #wrong password
                    #return redirect(url_for('wrongPassword'))
                    return redirect(url_for('nonActiveUser'))
            else:
                # non-active user
                return redirect(url_for('nonActiveUser'))
        else:
            # user entry not found
            #return redirect(url_for('noSuchUser'))
            return redirect(url_for('nonActiveUser'))
    else:
        return redirect(url_for('loginPage'))


# Logout functionality 
@app.route('/logout',methods = ['Post','Get'])
@login_required
def logoutUser():
    logout_user() 
    return redirect(url_for('loginPage'))


# Application Home page
@app.route('/userhome', methods = ['Post','Get'])
@login_required
def userHome():
    try:
        sqliteConnection = sqlite3.connect('instance/database.db')
        #D:\Workspace\PG\Python\Secure\Assignment3\instance\database.db
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")
        # Selecting record now

        viewOtherGroupsQuery = """select groupname from groups where groupname not in (Select distinct ge.groupname from groups g, groupentries ge where g.groupname=ge.groupname and ge.userActive = True and ge.useremail=?)"""
        #print(viewOtherGroupsQuery)
        cursor.execute(viewOtherGroupsQuery,[current_user.useremail])
        grpdetails0=[]
        rs0 = cursor.fetchall()
        for i in rs0:
            groupname = i[0]
            grpdetails0.append(groupname)

        request2MyGroupsQuery = """select groupname, useremail, userActive from groupentries where groupname in (select groupname from groups where useremail=?)  and useremail != ?"""
        #print(viewMyGroupsQuery)
        cursor.execute(request2MyGroupsQuery,[current_user.useremail,current_user.useremail])
        grpdetails1=[]
        rs1 = cursor.fetchall()
        
        for i in rs1:
            groupname = i[0]
            useremail = i[1]
            useractive = i[2]
            grpdetails1.append([groupname,useremail,useractive])

        viewMyGroupsQuery = """select a.groupname, a.groupdesc, CASE a.useremail WHEN ? THEN 'Yes' ELSE 'No' END ownership from groups a where a.groupname in (Select distinct ge.groupname from groups g, groupentries ge where g.groupname=ge.groupname and ge.userActive = True and ge.useremail=?)"""
        #print(viewMyGroupsQuery)
        cursor.execute(viewMyGroupsQuery,[current_user.useremail,current_user.useremail])
        grpdetails2=[]
        rs2 = cursor.fetchall()
        
        for i in rs2:
            #print(i)
            groupname = i[0]
            #print(groupname)
            groupdesc = i[1]
            #print(groupdesc)
            ownership = i[2]
            #print(ownership)
            grpdetails2.append([groupname,groupdesc,ownership])       

        #print("Record retrieved successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("the sqlite connection is closed")
    return render_template('ToolHome.html', loginemail=current_user.useremail, othergroups=grpdetails0, groupaccessrequests=grpdetails1, mygroups=grpdetails2)


#not used anywhere
@app.route('/adminUsersTable', methods = ['Post','Get'])
@login_required
def adminUsersTable():
    registeredusersare = registeredusers.query.all()
    return render_template('adminUsersTable.html', registeredusers=registeredusersare)

"""
# useremail not registered
@app.route('/nouser')
def noSuchUser():
    return render_template('NoUserFound.html')"""


# General login error method
@app.route('/errorlogin')
def nonActiveUser():
    return render_template('NonActiveUser.html')

"""
# Wrong Password
@app.route('/wrongPassword')
def wrongPassword():
    return render_template('wrongPassword.html')"""


# Duplicate Useremail
@app.route('/registerusercopy')
def registerusercopy():
    return render_template('UserAlreadyRegistered.html')


# Request to Join Existing Group
@app.route('/joinexistinggroup', methods = ['Post','Get'])
def joinExistingGroup():
    if request.method == 'POST':
        joins_groups = request.form['join_grpname']
        x = joins_groups.split(",")
        for i in x:
            db.session.add(groupentries(groupname=i, useremail=current_user.useremail))
        db.session.commit()
        return redirect(url_for('userHome'))
    else:
        return redirect(url_for('loginPage'))


# Create / Delete Group
@app.route('/createdeletegroup', methods = ['Post','Get']) 
def createDeleteGroup():
    if request.method == 'POST':
        #print("howdy")
        createdeletegroupname = request.form['create_grpname']
        #print(createdeletegroupname)
        createdeletegroupdesc = request.form['create_grpdesc']
        #print(createdeletegroupdesc)
        createdeletegroupactionperform = request.form['radcrtdelgrp']
        #print(createdeletegroupactionperform)

        if createdeletegroupactionperform == "Create":

            objectCreateNewgroup1 = groups(groupname=createdeletegroupname, groupdesc=createdeletegroupdesc, useremail=current_user.useremail, isowner=True)
            objectCreateNewgroup2 = groupentries(groupname=createdeletegroupname, useremail=current_user.useremail, userActive=True)
            db.session.add(objectCreateNewgroup1)
            db.session.add(objectCreateNewgroup2)
            db.session.commit()
        else:
            try:
                sqliteConnection = sqlite3.connect('instance/database.db')
                #D:\Workspace\PG\Python\Secure\Assignment3\instance\database.db
                cursor = sqliteConnection.cursor()
                #print("Connected to SQLite")
                queryToCheckAdmin = """Select count(*) from groups g, registeredusers users where users.useremail= g.useremail and (users.isadmin=True or (g.isowner=True and g.useremail=? and g.groupname=?)"""
                #print(queryToCheckAdmin)
                cursor.execute(queryToCheckAdmin,[current_user.useremail,createdeletegroupname])
                rs = cursor.fetchall()
                for i in rs:
                    cnt = int(i[0])
                    break
                #print(cnt)
                if cnt>0:
                    # Deleting single record now
                    sql_delete_query1 = """DELETE from groups where  groupname='?'"""
                    #print(sql_delete_query1)
                    cursor.execute(sql_delete_query1,[createdeletegroupname])

                    sql_delete_query2 = """DELETE from groupentries where  groupname='?'"""
                    #print(sql_delete_query2)
                    cursor.execute(sql_delete_query2,[createdeletegroupname])

                    sql_delete_query3 = """DELETE from itementries where  groupname='?'"""
                    #print(sql_delete_query3)
                    cursor.execute(sql_delete_query3,[createdeletegroupname])

                    sql_delete_query4 = """DELETE from itemfeedbackentries where  groupname='?'"""
                    #print(sql_delete_query4)
                    cursor.execute(sql_delete_query4,[createdeletegroupname])

                    sqliteConnection.commit()
                    #print("Record deleted successfully ")
                cursor.close()

            except sqlite3.Error as error:
                print("Failed to delete record from sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    #print("the sqlite connection is closed")
        return redirect(url_for('userHome'))
    else:
        return redirect(url_for('loginPage'))

# User access management in groups by owners
@app.route('/grantgroupaccess', methods=['GET', 'POST'])
def grantgroupaccessdiv():
    if request.method == 'POST':
        try:
            sqliteConnection = sqlite3.connect('instance/database.db')
            cursor = sqliteConnection.cursor()
            if request.form['grantgroupaccess_action'] == "Accept":
                sql_delete_query1 = """update groupentries set userActive = 1 where groupname = ? and useremail = ?"""
                cursor.execute(sql_delete_query1,[request.form['grantgroupaccess_grpname'],request.form['grantgroupaccess_useremail']])
            elif request.form['grantgroupaccess_action'] == "Revoke":
                sql_delete_query1 = """update groupentries set userActive = 0 where groupname = ? and useremail = ?"""
                cursor.execute(sql_delete_query1,[request.form['grantgroupaccess_grpname'],request.form['grantgroupaccess_useremail']])
            elif request.form['grantgroupaccess_action'] == "Reject":
                sql_delete_query1 = """delete from groupentries where groupname = ? and useremail = ? and userActive = 0"""
                cursor.execute(sql_delete_query1,[request.form['grantgroupaccess_grpname'],request.form['grantgroupaccess_useremail']])

            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                #print("the sqlite connection is closed")
        return redirect(url_for('userHome'))

    else:
        return redirect(url_for('loginPage'))


# File upload on the selected group
@app.route('/fileuploadmodule', methods=['GET', 'POST'])
@login_required
def fileuploadmodule():
    if request.method == 'POST':
        currentGroupName = request.form['currentGroupName']
        objectFileUpload = request.files['file']
        objectFileUploadModal = itementries(itemname=objectFileUpload.filename, useremail=current_user.useremail, itemContent=objectFileUpload.read(), groupname=currentGroupName)
        db.session.add(objectFileUploadModal)
        db.session.commit() 

        sqliteConnection = sqlite3.connect('instance/database.db')
        cursor = sqliteConnection.cursor()
        viewItemsInGroupsQuery = """select itemname, itemContent, useremail, groupname from itementries where groupname = ? """
        cursor.execute(viewItemsInGroupsQuery,[currentGroupName])
        grpdetails0=[]
        rs0 = cursor.fetchall()
        for i in rs0:
            itemname = i[0]
            itemContent = b64encode(i[1]).decode("utf-8")
            itemowner = i[2]
            groupname = i[3]
            grpdetails0.append([itemname,itemContent,itemowner,groupname])
        cursor.close()
        return render_template('itemList.html', itemList=grpdetails0, selectedGroupName = currentGroupName, currentUserEmail = current_user.useremail)
    return redirect(url_for('userHome'))


# Takes you to group items page for the selected group
@app.route('/selectedgroup', methods=['GET', 'POST'])
def selectedGroup():
    groupnameis = request.form['selectedgroup_grpname']
    try:
        sqliteConnection = sqlite3.connect('instance/database.db')
        #D:\Workspace\PG\Python\Secure\Assignment3\instance\database.db
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")
        # Selecting record now

        viewItemsInGroupsQuery = """select itemname, itemContent, useremail, groupname from itementries where groupname = ? """
        #print(viewItemsInGroupsQuery)
        cursor.execute(viewItemsInGroupsQuery,[groupnameis])
        grpdetails0=[]
        rs0 = cursor.fetchall()
        for i in rs0:
            itemname = i[0]
            itemContent = b64encode(i[1]).decode("utf-8")
            itemowner = i[2]
            groupname = i[3]
            grpdetails0.append([itemname,itemContent,itemowner,groupname])
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("the sqlite connection is closed")
    #print("agbdrbdrbdt:", grpdetails0)
    return render_template('itemList.html', itemList=grpdetails0, selectedGroupName = groupnameis, currentUserEmail = current_user.useremail)


# delete uploaded items in group
@app.route('/deleteGroupItem', methods = ['Post','Get']) 
def deleteGroupItem():
    if request.method == 'POST':
        deleteItem_itemGroupName = request.form['deleteItem_itemGroupName']
        deleteItem_itemName = request.form['deleteItem_itemName']

        try:
            sqliteConnection = sqlite3.connect('instance/database.db')
            cursor = sqliteConnection.cursor()
            queryToCheckAdmin = """Select count(*) from itementries where useremail=? and groupname=? and itemname=?"""
            #print(queryToCheckAdmin)
            cursor.execute(queryToCheckAdmin,[current_user.useremail,deleteItem_itemGroupName,deleteItem_itemName])
            rs = cursor.fetchall()
            for i in rs:
                cnt = int(i[0])
                break

            queryToCheckAdmin = """Select count(*) from itemfeedbackentries where groupname=? and itemname=?"""
            #print(queryToCheckAdmin)
            cursor.execute(queryToCheckAdmin,[deleteItem_itemGroupName,deleteItem_itemName])
            rs1 = cursor.fetchall()
            for i in rs1:
                cnt1 = int(i[0])
                break

            if cnt>0:
                sql_delete_query1 = """DELETE from itementries where groupname=? and itemname=?"""
                cursor.execute(sql_delete_query1,[deleteItem_itemGroupName,deleteItem_itemName])

                if cnt1>0:
                    sql_delete_query2 = """DELETE from itemfeedbackentries where groupname=? and itemname=?"""
                    cursor.execute(sql_delete_query2,[deleteItem_itemGroupName,deleteItem_itemName])

                sqliteConnection.commit()

            viewItemsInGroupsQuery = """select itemname, itemContent, useremail, groupname from itementries where groupname = ? """
            #print(viewItemsInGroupsQuery)
            cursor.execute(viewItemsInGroupsQuery,[deleteItem_itemGroupName])
            grpdetails0=[]
            rs0 = cursor.fetchall()
            for i in rs0:
                itemname = i[0]
                itemContent = b64encode(i[1]).decode("utf-8")
                itemowner = i[2]
                groupname = i[3]
                grpdetails0.append([itemname,itemContent,itemowner,groupname])
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            
        return render_template('itemList.html', itemList=grpdetails0, selectedGroupName = deleteItem_itemGroupName, currentUserEmail = current_user.useremail)
    else:
        return redirect(url_for('loginPage'))


# Takes to add feedback page of indv items
@app.route('/submitFeedbackGroupItem', methods=['GET', 'POST'])
def submitFeedbackGroupItem():
    submitFeedback_itemGroupName = request.form['submitFeedback_itemGroupName']
    submitFeedback_itemName = request.form['submitFeedback_itemName']
    try:
        sqliteConnection = sqlite3.connect('instance/database.db')
        cursor = sqliteConnection.cursor()
        viewItemsInGroupsQuery = """select itemContent from itementries where groupname = ? and itemname = ?"""
        #print(viewItemsInGroupsQuery)
        cursor.execute(viewItemsInGroupsQuery,[submitFeedback_itemGroupName,submitFeedback_itemName])
        grpdetails0=[]
        rs0 = cursor.fetchall()
        for i in rs0:
            groupname = submitFeedback_itemGroupName
            itemname = submitFeedback_itemName
            itemContent = b64encode(i[0]).decode("utf-8")            
            grpdetails0.append([groupname,itemname,itemContent])

        viewItemsFeedbacksQuery = """select id,useremail,itemfeedback from itemfeedbackentries where groupname = ? and itemname = ?"""
        cursor.execute(viewItemsFeedbacksQuery,[groupname,itemname])
        itemfeedbackslist=[]
        rs1 = cursor.fetchall()
        j=1
        for i in rs1:
            feedbackidnumber = j
            submittedby = i[1]
            itemfeedback = i[2]
            itemfeedbackslist.append([feedbackidnumber,submittedby,itemfeedback])
            j=j+1
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    return render_template('itemFeedbacks.html', itemList=grpdetails0, feedbackList=itemfeedbackslist)


# Submit feedback on Each Item of Group
@app.route('/submitNewFeedbackEachItem', methods=['GET', 'POST'])
def submitNewFeedbackEachItem():
    if request.method == 'POST':
        itemfeedbackentry_groupname = request.form['newFeedbackgrpNameVal']
        itemfeedbackentry_itemname = request.form['newFeedbackitemNameVal']
        itemfeedbackentry_itemfeedback = request.form['newFeedbackVal']

        objectCreateNewgroup1 = itemfeedbackentries(groupname=itemfeedbackentry_groupname, itemname=itemfeedbackentry_itemname, itemfeedback=itemfeedbackentry_itemfeedback, useremail=current_user.useremail)
        db.session.add(objectCreateNewgroup1)
        db.session.commit()

        try:
            sqliteConnection = sqlite3.connect('instance/database.db')
            cursor = sqliteConnection.cursor()
            viewItemsInGroupsQuery = """select itemContent from itementries where groupname = ? and itemname = ?"""
            cursor.execute(viewItemsInGroupsQuery,[itemfeedbackentry_groupname,itemfeedbackentry_itemname])
            grpdetails0=[]
            rs0 = cursor.fetchall()
            for i in rs0:
                groupname = itemfeedbackentry_groupname
                itemname = itemfeedbackentry_itemname
                itemContent = b64encode(i[0]).decode("utf-8")            
                grpdetails0.append([groupname,itemname,itemContent])

            viewItemsFeedbacksQuery = """select id,useremail,itemfeedback from itemfeedbackentries where groupname = ? and itemname = ?"""
            cursor.execute(viewItemsFeedbacksQuery,[groupname,itemname])
            itemfeedbackslist=[]
            rs1 = cursor.fetchall()
            j=1
            for i in rs1:
                feedbackidnumber = j
                submittedby = i[1]
                itemfeedback = i[2]
                itemfeedbackslist.append([feedbackidnumber,submittedby,itemfeedback])
                j=j+1
            
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete record from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
        return render_template('itemFeedbacks.html', itemList=grpdetails0, feedbackList=itemfeedbackslist)
    return redirect(url_for('userHome'))


#Download Individual Items from Group 
@app.route('/downloadEachItem', methods=['GET', 'POST'])
def downloadEachItem():
    if request.method == 'POST':
        downloadfile_groupname = request.form['downloadgrpNameVal']
        downloadfile_itemname = request.form['downloaditemNameVal']

        uploadedItem = itementries.query.filter_by(groupname=downloadfile_groupname,itemname=downloadfile_itemname).first()
        return send_file(BytesIO(uploadedItem.itemContent), download_name=downloadfile_itemname, as_attachment=True)
    return redirect(url_for('userHome'))


if __name__ == '__main__':
    app.run(debug=True, port=8081)


#List of References:

#https://csveda.com/flask-and-mysql-how-to-fill-table-data-in-a-dropdown/
#https://jquery.com/download/
#https://pythonbasics.org/flask-tutorial-routes/
#https://stackoverflow.com/questions/12502646/access-multiselect-form-field-in-flask
#https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
#https://stackoverflow.com/questions/16351826/link-to-flask-static-files-with-url-for
#https://stackoverflow.com/questions/19274226/how-to-track-the-current-user-in-flask-login
#https://stackoverflow.com/questions/21674303/flask-sqlalchemy-filters-and-operators
#https://stackoverflow.com/questions/25947251/deleting-rows-from-database-with-python-flask
#https://stackoverflow.com/questions/30011170/flask-application-how-to-link-a-javascript-file-to-website
#https://stackoverflow.com/questions/31083798/python-3-typeerror-str-object-cannot-be-interpreted-as-an-integer-when-work
#https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
#https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
#https://stackoverflow.com/questions/41588847/typeerror-cant-convert-bytes-object-to-str-implicitly-python
#https://stackoverflow.com/questions/42067268/jquery-toggle-div-when-clicking-on-h3
#https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
#https://stackoverflow.com/questions/547821/two-submit-buttons-in-one-form
#https://stackoverflow.com/questions/70319636/get-dropdown-selection-using-flask-and-html
#https://stackoverflow.com/questions/73508288/how-to-use-if-else-condition-in-html-table-td
#https://stackoverflow.com/questions/8712398/multiple-forms-or-multiple-submits-in-a-page
#https://teamtreehouse.com/community/using-databases-in-python-modeling-sqlite3-is-not-recognized-as-an-internal-or-external-command
#https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
#https://www.pythontutorial.net/getting-started/setup-visual-studio-code-for-python/
#https://www.youtube.com/watch?v=0Qxtt4veJIc&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&ab_channel=Codemy.com
#https://www.youtube.com/watch?v=1j3k-_DqobU
#https://www.youtube.com/watch?v=71EU8gnZqZQ
#https://www.youtube.com/watch?v=71EU8gnZqZQ&ab_channel=ArpanNeupane
#https://www.youtube.com/watch?v=bjcIAKuRiJw
#https://www.youtube.com/watch?v=GHvj1ivQ7ms&ab_channel=CodeVoid
#https://www.youtube.com/watch?v=hQl2wyJvK5k&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=10&ab_channel=Codemy.com
#https://www.youtube.com/watch?v=OrOKSFzsN9A&ab_channel=Pluralsight
#https://www.youtube.com/watch?v=pPSZpCVRbvQ
#https://www.youtube.com/watch?v=QIAgAnI6b3o&ab_channel=PracticalPythonSolutions-ByPaulMahon
#https://www.youtube.com/watch?v=RZfeixiJ4VA&ab_channel=plus2net


# Azure Link
#https://sharesecurelyservices.azurewebsites.net