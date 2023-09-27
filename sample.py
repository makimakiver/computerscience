from tkinter import *  # python 3
from tkinter import font  as tkfont
from Register import *

from tkinter import messagebox
import tkinter as tk
import psycopg2
import random
from email.message import EmailMessage
import ssl
import smtplib
import otp
# creating class for the User object
class User:
    def __init__(self, username, email, password):
        self.__username = username
        self.__email = email
        self.__password = password

    def UUIDgenerator(self):
        userId = ""
        for i in range (6):
            random_number = random.randint(0,9)
            userId = userId + str(random_number)
        return userId
    
    def UUID(self):
        examine = []
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        myCursor = con.cursor()
        query = 'SELECT "id" FROM "ielts_user"' 
        myCursor.execute(query)
        result = myCursor.fetchall()
        for i in result:
            examine.append(str(i).strip("(),"))
        print(examine)
        id =self.UUIDgenerator()
        print(id)
        while examine.count(id)>0:
            id =self.UUIDgenerator()
            print(id)
        if examine.count(id) == 0: 
            return id
        
    def register(self):    
        print("hello")
        enteredEmail = self.__email
        enteredUsername = self.__username
        enteredPassword = self.__password
        userId = self.UUID()
        self.__userId = userId
        print("print userId from register file: ", userId)
        # Connect to the database
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        # Create a cursor object
        cursor = con.cursor()
        insert_query = "INSERT INTO ielts_user(email, username, password, id) VALUES (%s,%s,%s,%s)"
        vals = [enteredUsername, enteredEmail, enteredPassword, userId]
        cursor.execute(insert_query, vals)
        cursor.execute("commit")        
        con.close()
    def getId(self):
        print("print userId from getId method: ", self.__userId)
        return self.__userId
    
class Essay:
    def roundDown(self, num):
        num = float(num)
        first_option = round(num)
        second_first_option = abs((first_option + 0.5)-num)
        second_second_option = abs((first_option - 0.5)-num)
        if  second_first_option >= second_second_option:
            second_option = first_option - 0.5
        else:
            second_option = first_option + 0.5
        if second_option > first_option:
            return first_option
        else:
            return second_option 

    def overall_Calc(self, num1, num2, num3, num4):
        result = self.roundDown((num1+num2+num3+num4)/4)
        if len(str(result)) == 1:
            return (str(result) + ".0")
        else:
            return result
    def __init__(self, taskresponse, coherencecohesion, grammaraccuracy, lexicalresources, userId):
        self.__userId = userId
        self.__taskresponse = taskresponse
        self.__coherencecohesion = coherencecohesion
        self.__grammaraccuracy = grammaraccuracy
        self.__lexicalresources = lexicalresources
    def setOverall(self):
        self.__overall = self.overall_Calc(self.__coherencecohesion, self.__taskresponse, self.__lexicalresources, self.__grammaraccuracy)

    def UUIDgenerator(self):
        essayId = ""
        for i in range (6):
            random_number = random.randint(0,9)
            essayId = essayId + str(random_number)
        return essayId
    
    def UUID(self):
        examine = []
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        myCursor = con.cursor()
        query = 'SELECT "id" FROM "ielts_user"' 
        myCursor.execute(query)
        result = myCursor.fetchall()
        for i in result:
            examine.append(str(i).strip("(),"))
        print(examine)
        id =self.UUIDgenerator()
        print(id)
        while examine.count(id)>0:
            id =self.UUIDgenerator()
            print(id)
        if examine.count(id) == 0: 
            return id
        
    def essayWritten(self, userId, tr, cc, lr, ga):    
        print("hello")
        self.__userId = userId
        print("print userId from register file: ", userId)
        # Connect to the database
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        # Create a cursor object
        cursor = con.cursor()
        insert_query = "INSERT INTO essay(email, username, password, id) VALUES (%s,%s,%s,%s)"
        vals = [enteredUsername, enteredEmail, enteredPassword, userId]
        cursor.execute(insert_query, vals)
        cursor.execute("commit")        
        con.close()
    def getId(self):
        print("print userId from getId method: ", self.__userId)
        return self.__userId
    

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.discUserInfo = {}
        self.frames = {}
        for F in (Register, Login, Home, Result):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Register")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Register(tk.Frame):
    def callfunc(self, key, email, username, password):
        cost = otp.checker(key)
        if cost == True:
            global user
            user = User(email, username, password)
            user.register()
            userId = user.getId()
            self._Home_btn_clicked(email, username, password, userId)
        else:
            messagebox.showerror("", "your key is wrong")
    def callClass(self, enteredEmail, enteredUsername, enteredPassword, enteredConfirmation):
        print("test1 passed")
        # global enteredEmail
        print("entered Email: ", enteredEmail)
        print("entered Email: ", enteredUsername)
        print("entered Password: ", enteredPassword)
        # print(unique_checker("email", enteredEmail))
        # database might be needed to be changed from myPHP
        if enteredEmail == "" or enteredUsername == "" or enteredPassword == "" or enteredConfirmation == "":
            print("blank")
            messagebox.showerror("", "Blank not allowed")
        elif len(enteredPassword) <= 7:
            messagebox.showwarning("", "more letter, more secured")
        # elif self.unique_checker("username", enteredUsername) == False:
        #     messagebox.showerror("", "walk away")
        # elif self.unique_checker("email", enteredEmail) == False:
        #     messagebox.showerror("", "hey yo, you put same email address as other user. To be more respectful man!")
        # elif enteredPassword != enteredConfirmation:
        #     messagebox.showerror("", "repeat your password please")
        else:
            print("success")
            otp.generation(enteredEmail)
            try: 
                once_upon_a_time = tk.Entry(self)
                once_upon_a_time.pack()
                checkAccount = tk.Button(self, text="checking", command=lambda: self.callfunc(once_upon_a_time.get(), enteredEmail, enteredUsername, enteredPassword))
                checkAccount.pack()
            except:
                print("error")
                messagebox.showerror("","invalid password or the user do not exist")
            messagebox.showinfo("", "Now I have sent a one time pad key for your verification. Check it out.")
        
    def unique_checker(self, test, subject):
        examine = []    
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        myCursor = con.cursor()
        query = f'SELECT "{test}" FROM "ielts_user"'    
        # Execute the query
        myCursor.execute(query)
        result = myCursor.fetchall()
        for i in result:
            examine.append(str(i).strip("(),'"))
        print("There are ",examine.count(str(subject))," same ", test, " : ", subject)
        print(examine)
        for i in examine:
            if i == subject:
                print(False)
                return False
        print(True)
        return True
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label
        Entry = tk.Entry
        root = self

        title = Label(root, text="IELTs writing practice", font=("MSゴシック", "20", "bold"), fg="red")
        title.pack()

        emailLabel = Label(root, text="Email:")
        emailLabel.pack()
        email = Entry(root)
        email.pack()

        usernameLabel = Label(root, text="Username:")
        usernameLabel.pack()
        username = Entry(root)
        username.pack()

        passwordLabel = Label(root, text="Password:")
        passwordLabel.pack()
        password = Entry(root, show='*')
        password.pack()

        confirmationLabel = Label(root, text="Confirmation:")
        confirmationLabel.pack()
        confirmation = Entry(root, show='*')
        confirmation.pack()
        myButton = tk.Button(root, text="Create an account from here", command= lambda: self.callClass(email.get(), username.get(), password.get(), confirmation.get()))
        myButton.pack()
        switch_to_Login = tk.Button(root, text="jumping to the login page if you have an account", command= self._login_btn_clicked)
        switch_to_Login.pack()
        
    def _Home_btn_clicked(self, email, username, password, userId):
        ### after verifying the login data in database, it creates a dictionary with the user's data ( userId,name,lastName ...)
        self.controller.discUserInfo['email'] = email
        self.controller.discUserInfo['username'] = username
        self.controller.discUserInfo['password'] = password       
        self.controller.discUserInfo['userId'] = userId
        self.controller.show_frame("Home")
    def _login_btn_clicked(self):
        self.controller.show_frame("Login")


class Login(tk.Frame):
    def UUID(self):
        examine = []
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        myCursor = con.cursor()
        query = 'SELECT "id" FROM "ielts_user"' 
        myCursor.execute(query)
        result = myCursor.fetchall()
        for i in result:
            examine.append(str(i).strip("(),"))
        print(examine)
        id =self.UUIDgenerator()
        print(id)
        while examine.count(id)>0:
            id =self.UUIDgenerator()
            print(id)
        if examine.count(id) == 0: 
            return id
    def callfunc(self, key, email, username, password, userId ):
        print("value passed ? ", key)
        cost = otp.checker(key)
        if cost == True:           
            self._Home_btn_clicked(email, username, password, userId)
        else:
            messagebox.showerror("", "your key is wrong")
    def loginButton(self, enteredEmail, enteredPassword):    
        if enteredEmail == "" or enteredPassword == "" :
            messagebox.showerror("", "Blank not allowed")
            # if user do not put anything on either email or password entry it will tell you Blank is not allowed
        else:
            # if user put something it will fetch the user information based on provided information
            con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
            # connect to the Postgre 
            myCursor = con.cursor()
            # Create a cursor object
            query = f"SELECT * FROM ielts_user WHERE email=%s"
            # will fetch the data from the database where entry email exist
            myCursor.execute(query, (enteredEmail,))
            result = myCursor.fetchone()

            if str(result[3]) == str(enteredPassword):
                try:
                    root = self
                    otp.generation(enteredEmail)
                    once_upon_a_time = tk.Entry(root)
                    once_upon_a_time.pack()
                    checkAccount = tk.Button(root, text="checking", command=lambda: self.callfunc(once_upon_a_time.get(), result[1], result[2], result[3], result[0]))
                    checkAccount.pack()
                except:
                    print("error")
            else:
                messagebox.showerror("","invalid password or the user do not exist")
                

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = Label(self, text="IELTs writing practice", font=("MSゴシック", "20", "bold"), fg="red")
        title.pack()

        emailLabel = Label(self, text="Email:")
        emailLabel.pack()
        email = Entry(self)
        email.pack()

        passwordLabel = Label(self, text="Password:")
        passwordLabel.pack()
        password = Entry(self)
        password.pack()

        myButton = Button(self, text="Login", command= lambda: self.loginButton(email.get(), password.get()))
        myButton.pack()

        forgotLabel = Label(self, text="if you do not have any account")
        forgotLabel.pack()
        createAccount = Button(self, text="Create an account from here", command=self.switchpage)
        createAccount.pack()
    
    def _Home_btn_clicked(self, email, username, password, userId):
        ### after verifying the login data in database, it creates a dictionary with the user's data ( userId,name,lastName ...)
        self.controller.discUserInfo['email'] = email
        self.controller.discUserInfo['username'] = username
        self.controller.discUserInfo['password'] = password       
        self.controller.discUserInfo['userId'] = userId
        self.controller.show_frame("Home")
    
    def switchpage(self):
        self.controller.show_frame("Register")
        

class Home(tk.Frame):
    def UUIDgenerator(self):
        essayId = ""
        for i in range (6):
            random_number = random.randint(0,9)
            essayId = essayId + str(random_number)
        return essayId
    def UUID(self):
        examine = []
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        myCursor = con.cursor()
        query = 'SELECT "essay_id" FROM "essay"' 
        myCursor.execute(query)
        result = myCursor.fetchall()
        for i in result:
            examine.append(str(i).strip("(),"))
        print(examine)
        id =self.UUIDgenerator()
        print(id)
        while examine.count(id)>0:
            id =self.UUIDgenerator()
            print(id)
        if examine.count(id) == 0: 
            return id

    def switchToProgress(self):
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.ylabel('some numbers')
        plt.show()
        
    def getEssay(self, getQuestion, getAnswer):
        print(getQuestion, getAnswer)
    def submitEssay(self, getQuestion, getAnswer):
        print(getQuestion, getAnswer)
        con = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Eycj3209yuta", port=6000)
        # connect to the Postgre 
        myCursor = con.cursor()
        # Create a cursor object
        insert_query = "INSERT INTO essay(essay_id, question, essay, user_Id) VALUES (%s,%s,%s,%s)"
        # will fetch the data from the database where entry email exist
        vals = (int(self.UUID()), getQuestion, getAnswer, "{%s}" % str(self.controller.discUserInfo["userId"]))
        print(vals)
        # set UUID by using Class
        myCursor.execute(insert_query, vals)
        myCursor.execute("commit")
        con.close()
        self.switchpage()
       
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        root = self
        title = Label(root, text="IELTs writing practice", font=("MSゴシック", "20", "bold"), fg="red")
        title.pack()

        Label(root, text="Question: ").place(x=200, y=50)
        Question = StringVar()
        Q_entry = tk.Text(root, width=100, font="Times 9")
        Q_entry.place(x=270, y=50, height=30)

        Label(root, text="Your essay: ").place(x=200, y=90)
        Answer = StringVar()
        A_entry = tk.Text(root, width=100, font="Times 9")
        A_entry.place(x=270, y=90)
        Button(root, width=10, text="Progress", command=self.switchToProgress).place(x=50,y=50)
        Qus = Q_entry.get("1.0", END)
        Ans = A_entry.get("1.0", END)
        Button(root, text="submit your essay from here", command= lambda: self.submitEssay(Q_entry.get("1.0", END), A_entry.get("1.0", END))).place(x=500,y=500)
        Button(root, text="getessay: ", command= lambda: self.getEssay(Q_entry.get("1.0", END), A_entry.get("1.0", END))).pack()

    def getAlocationData(self):
        print(self.controller.discUserInfo["userId"])
    def switchpage(self):
        self.controller.show_frame("Result")
class Result(tk.Frame):       
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        root = self
        column = ('Name', 'Score')
        from tkinter import ttk 
        tree = ttk.Treeview(root, columns=column)
        # first row
        tree.column('#0',width=0, stretch='no')
        tree.column('Name', anchor='center', width=150)
        tree.column('Score', anchor='center', width=70)
        # first row's articles
        tree.heading('#0',text='')
        tree.heading('Name', text='Type', anchor='center')
        tree.heading('Score',text='Score', anchor='center')

        task_Response = 5.5
        grammar_Accuracy = 6.5
        lexical_Resources = 5.5
        coherence_Cohesion = 6.5
        overall = 6.0
        # adding record
        tree.insert(parent='', index='end', values=( 'Task-Response', task_Response))
        tree.insert(parent='', index='end', values=( '', ''))
        tree.insert(parent='', index='end', values=('Grammar-Accuracy', grammar_Accuracy))
        tree.insert(parent='', index='end', values=( '', ''))
        tree.insert(parent='', index='end', values=('Lexical-Resources', lexical_Resources))
        tree.insert(parent='', index='end', values=( '', ''))
        tree.insert(parent='', index='end', values=('Coherence-Cohesion', coherence_Cohesion))
        tree.insert(parent='', index='end', values=( '', ''))
        tree.insert(parent='', index='end', values=('Overall', overall))

        tree.pack(pady=10)

        ieltsAdvicesintro = Label(root, text="some advices: ")
        ieltsAdvicesintro.place(x=635, y=30)
        advice = ""
        ieltsAdvices = Message(root, text=advice, width=315)
        ieltsAdvices.place(x=620, y=70)

        gobackTohome = Label(root, text="do you want to try again?")
        gobackTohome.pack()
        homeButton = Button(root, text="Home", command=self.switchpage)
        homeButton.pack()
    def getAlocationData(self):
        print(self.controller.discUserInfo["userId"])
    def switchpage(self):
        self.controller.show_frame("Home")
if __name__ == "__main__":
    app = SampleApp()
    app.geometry('{}x{}'.format(800, 650))
    app.mainloop()