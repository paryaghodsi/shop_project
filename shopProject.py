import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import json


#--------------functions--------------------

def gradeCheck(user):
    with open("setting.json") as f:
        global grade
        info = json.load(f)
        v=list(info.values())
        k=list(info.keys())
        if user in k:
            x=k.index(user)
            grade=(v[x])
        return int(grade)
                       

def moreInfo():
    def prodExist():
        pname=txtpname.get()
        lblMsg.configure(text='', fg='orange') 
        listBox.delete(0, tk.END)  
        if len(pname)==0:
                    lblMsg.configure(text='empty fields error!',fg='red')
        elif pname.isdigit():
                    lblMsg.configure(text='Invalid input!!',fg='red')
        else: 
                sql=f"SELECT * FROM ratings WHERE pname LIKE ('%{pname}%')"
                result=cnt.execute(sql)
                rows=result.fetchall()
                if rows:
                        for row in rows:
                                item=f'''{row[2]}=>RATE:{row[3]},ISSUE:{row[4]}'''
                                listBox.insert('end',item) 
                                btnshowInfo.configure(state='active')
                                txtpname.delete(0, tk.END)
                                lblpname.configure(state='disabled')  
                                lblMsg.configure(text="Here are some comments about the product,\n hope you find them helpful!")
                else:
                        lblMsg.configure(text="No product or feedback available.",fg='red')
                        cnt.commit()     

    winmoreInfo=tk.Toplevel(win)
    winmoreInfo.title('more information')
    winmoreInfo.geometry('300x300')
    lblpname=tk.Label(winmoreInfo,text='enter the product name: ')
    lblpname.pack()
    txtpname=tk.Entry(winmoreInfo)
    txtpname.pack()
    lblMsg=tk.Label(winmoreInfo, text='')
    lblMsg.pack()
    btnshowInfo=tk.Button(winmoreInfo,text='show ratings',command=prodExist)
    btnshowInfo.pack()
    listBox=tk.Listbox(winmoreInfo,width=40)
    listBox.pack()
    




           
def isEmpty(user,pas):
    if user=='' or pas=='':
        return True
    else:
        return False
def checkInfo(user,pas=False):
    if pas:
        sql=f'''SELECT * FROM users WHERE username="{user}" AND password="{pas}" '''
    else:
        sql = f'''SELECT * FROM users WHERE username="{user}" '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    if len(rows)<1:
        return False
    else:
        return True
    




def login():
    global session
    user=txtUser.get()
    pas=txtPas.get()
   
    if isEmpty(user,pas):
        lblMsg.configure(text='empty fields error!!!',fg='red')
        return
    
    if checkInfo(user,pas):
        lblMsg.configure(text='Welcome To your Account!',fg='green')
        session=user  
        txtUser.delete(0,'end')
        txtPas.delete(0,'end')
        txtUser.configure(state='disabled')
        txtPas.configure(state='disabled')
        btnLogin.configure(state='disabled')
        btnDel.configure(state='active')
        btnShop.configure(state='active')
        btnMycart.configure(state='active')
        grade=gradeCheck(user)
        listbox.insert('end',' your grade:',grade )

        if grade>3:
          btnsearch.configure(state='active',fg='brown')  


        if grade>5:
            btnrate.configure(state='active',fg='gold')
            lblMsg.configure(text='you are a special user!',fg='gold')
            btnsearch.configure(state='active',fg='brown') 
            btnMoreinfo.configure(state='active',fg='gold') 
            

        
    else:
        lblMsg.configure(text='Wrong Username Or Password', fg='red')

        
   
def signup():
    def signupValidate(user,pas,cpas):
        if user=='' or pas=='' or cpas=='':
            return False,'Empty Fields Error!'
        if pas!=cpas:
            return False,'password and confirmation mismatch!'
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', pas):
            return False,'password Minimum eight chars,at least one letter and one number'
        if checkInfo(user):
            return False,'Username Already Exist!!'
        return  True,''

    def save2users(user,pas):
        try:
            sql=f'INSERT INTO users (username,password,grade) VALUES ("{user}","{pas}",0)'
            cnt.execute(sql)
            cnt.commit()
            return True
        except:
            return False
    def submit():
        user=txtUser.get()
        pas=txtPas.get()
        cpas=txtCpas.get()
        result,errorMSG=signupValidate(user,pas,cpas)
        if not result:
            lblMsg.configure(text=errorMSG,fg='red')
            return
        result=save2users(user,pas)
        if not result:
            lblMsg.configure(text='something went wrong during database connection!!',fg='red')
            return
        lblMsg.configure(text='submit done successfully!',fg='green')
        txtUser.delete(0,'end')
        txtPas.delete(0, 'end')
        txtCpas.delete(0, 'end')
    winSignup=tk.Toplevel(win)
    winSignup.title('Signup Panel')
    winSignup.geometry('300x300')
    lblUser = tk.Label(winSignup, text='Username:')
    lblUser.pack()
    txtUser = tk.Entry(winSignup)
    txtUser.pack()
    lblPas = tk.Label(winSignup, text='Password:')
    lblPas.pack()
    txtPas = tk.Entry(winSignup,show='*')
    txtPas.pack()
    lblCpas = tk.Label(winSignup, text='Password confirmation:')
    lblCpas.pack()
    txtCpas = tk.Entry(winSignup,show='*')
    txtCpas.pack()
    lblMsg = tk.Label(winSignup, text='')
    lblMsg.pack()
    btnSubmit = tk.Button(winSignup, text='Submit',command=submit)
    btnSubmit.pack()
    winSignup.mainloop()


def delAccount():
    global session
    result=messagebox.askyesno(title='Confirm',message='Are You Sure?')
    if not result:
        lblMsg.configure(text='Operation Canceled By User!',fg='red')
        return
    result=delUser(session)
    if not result:
        lblMsg.configure(text='something went wrong during database connection!!', fg='red')
        return
    lblMsg.configure(text='account deleted successfully!',fg='green')
    btnDel.configure(state='disabled')
    btnLogin.configure(state='active')
    txtUser.configure(state='normal')
    txtPas.configure(state='normal')
    session=''
def delUser(user):
    try:
        sql=f'DELETE FROM users WHERE username="{user}"'
        cnt.execute(sql)
        cnt.commit()
        return True
    except:
        return False

def getProducts():
    sql="SELECT * FROM products"
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows
def fetch(sql):
    result = cnt.execute(sql)
    rows = result.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False
def idExist(pId):
    sql=f"SELECT * FROM products WHERE id={int(pId)}"
    return fetch(sql)

def enoughProducts(pid,num):
    sql=f'''SELECT * FROM products WHERE id={int(pid)} AND quantity>={int(num)} '''
    return fetch(sql)
def getId(user):
    sql=f'''SELECT id FROM users WHERE username="{user}" '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows[0][0]

def shopPanel(): 

    def save2cart(pId,pNumber):
        try:
            global session
            id=getId(session)
            sql=f'''INSERT INTO cart (uid,pid,number) VALUES ({id},{int(pId)},{int(pNumber)})'''
            cnt.execute(sql)
            cnt.commit()
            return True
        except:
            return False

    def updateQNT(pId,pNumber):
        try:
            pNumber=int(pNumber)
            pId=int(pId)
            sql=f'''UPDATE products SET quantity=quantity-{pNumber} WHERE id={pId}'''
            cnt.execute(sql)
            cnt.commit()
            return True,''
        except Exception as e:
            return False,e      
    def discount():
        user=txtUser.get()
        grade=gradeCheck(user)
        if grade>5:
            discountPercentage=(grade)
            lblmsg2.configure(text=f'You have {discountPercentage}% off!')
        else:
            lblmsg2.configure(text='sorry,your grade does not get any discount,maybe next time:(',fg='pink')    

    def buy(): 
        pId=txtid.get()
        pNumber=txtqnt.get()
        if pId=='' or pNumber=='':
            lblmsg2.configure(text='Fill the blanks!',fg='red')
            return
        if (not pId.isdigit()) or (not(pNumber.isdigit())):
            lblmsg2.configure(text='Invalid input!', fg='red')
            return
        if not idExist(pId):
            lblmsg2.configure(text='Wrong Product Id!', fg='red')
            return
        if not enoughProducts(pId,pNumber):
            lblmsg2.configure(text='Not enough Products!', fg='red')
            return
        result,msg=updateQNT(pId,pNumber)
        if not result:
            lblmsg2.configure(text=f'ERROR while connecting database=>\n{msg}', fg='red')
            return
        result=save2cart(pId,pNumber)
        if not result:
            lblmsg2.configure(text='ERROR while connecting database', fg='red')
            return
        lblmsg2.configure(text='products saved to your cart!',fg='green')
        txtid.delete(0,'end')
        txtqnt.delete(0,'end')
        lstBox.delete(0,'end')
        products = getProducts()
        for product in products:
            item = f'''Id={product[0]} , Name={product[1]} , Price={product[2]} , QNT={product[3]}'''
            lstBox.insert('end', item)
        if result:
            sql=f'''UPDATE users SET grade=grade+1 WHERE username="{session}"  '''
            cnt.execute(sql)
            cnt.commit()


    
    winShop=tk.Toplevel(win)
    winShop.title('Shop Panel')
    winShop.geometry('500x400')
    lstBox=tk.Listbox(winShop,width=80)
    lstBox.pack()
    lblid=tk.Label(winShop,text='Id:')
    lblid.pack()
    txtid=tk.Entry(winShop)
    txtid.pack()
    lblqnt = tk.Label(winShop, text='numbers:')
    lblqnt.pack()
    txtqnt = tk.Entry(winShop)
    txtqnt.pack()
    lblmsg2=tk.Label(winShop,text='')
    lblmsg2.pack()
    btndiscount=tk.Button(winShop,text='show my discount!',command=discount)
    btndiscount.pack()
    btnBuy=tk.Button(winShop,text='Buy!',command=buy)
    btnBuy.pack()
    products=getProducts()

    for product in products:
        item=f'''Id={product[0]} , Name={product[1]} , Price={product[2]} , QNT={product[3]}'''
        lstBox.insert('end',item)
    winShop.mainloop()

def showCart():
    def getMycart():
        global session
        id=getId(session)
        sql=f'''
                SELECT products.pname,products.price,cart.number
                FROM products INNER JOIN cart
                ON products.id=cart.pid
                WHERE cart.uid={id}
            '''
        result=cnt.execute(sql)
        rows=result.fetchall()
        return rows

    def Totalprice():
        tPrice=0
        for product in cart:
            price=(int(product[1]) )
            qnt=(int(product[2]))
            tPrice += (price*qnt)
        lblMsg2.configure(text=f'total price = {tPrice} $', fg='green')

    def Discount():
        global session
        user=session
        grade=gradeCheck(user)
        lblMsg4.configure(text=f'discount = {grade} %', fg='green')



    def pdiscount():
        global session
        user=session
        grade=gradeCheck(user)
        tPrice=0
        for product in cart:
            price=(int(product[1]))
            qnt=(int(product[2]))
            tPrice += price*qnt
            Dprice = ((tPrice)-(tPrice * grade/100))
            lblMsg.configure(text=f'price with discount = {Dprice} $', fg='green')
        

    winCart=tk.Toplevel(win)
    winCart.title('Cart Panel')
    winCart.geometry('700x700')
    lstbox2=tk.Listbox(winCart,width=60,height=15)
    lstbox2.pack()


    btnTotal=tk.Button(winCart,text='show total price',command=Totalprice)
    btnTotal.pack()
    
    lblMsg2=tk.Label(winCart,text="")
    lblMsg2.pack()

    btnDiscount=tk.Button(winCart,text='show discount',command=Discount)
    btnDiscount.pack()
    
    lblMsg4=tk.Label(winCart,text="")
    lblMsg4.pack()

    btnDprice=tk.Button(winCart,text='show price with discount',command=pdiscount)
    btnDprice.pack()

    lblMsg=tk.Label(winCart,text="")
    lblMsg.pack()

    
    global session
    user=session
    gradeCheck(user)
    if grade<3:
     btnDprice.configure(state='disable')
     btnDiscount.configure(state='disable')
    cart=getMycart()
    for product in cart:
        text=f'Name:{product[0]}  Number:{product[2]}  Total price={int(product[1])*int(product[2])} $  '
        lstbox2.insert(0,text)
    
    winCart.mainloop()
#----------------------SEARCH-------------------------------------------------------------------
def search():

    def save2cart(pId,pNumber):
        try:
            global session
            id=getId(session)
            sql=f'''INSERT INTO cart (uid,pid,number) VALUES ({id},{int(pId)},{int(pNumber)})'''
            cnt.execute(sql)
            cnt.commit()
            return True
        except:
            return False

    def updateQNT(pId,pNumber):
        try:
            pNumber=int(pNumber)
            pId=int(pId)
            sql=f'''UPDATE products SET quantity=quantity-{pNumber} WHERE id={pId}'''
            cnt.execute(sql)
            cnt.commit()
            return True,''
        except Exception as e:
            return False,e      

    def buy(): 
        pId=txtid.get()
        pNumber=txtqnt.get()
        if pId=='' or pNumber=='':
            lblmsg3.configure(text='Fill the blanks!',fg='red')
            return
        if (not pId.isdigit()) or (not(pNumber.isdigit())):
            lblmsg3.configure(text='Invalid input!', fg='red')
            return
        if not idExist(pId):
            lblmsg3.configure(text='Wrong Product Id!', fg='red')
            return
        if not enoughProducts(pId,pNumber):
            lblmsg3.configure(text='Not enough Products!', fg='red')
            return
        result,msg=updateQNT(pId,pNumber)
        if not result:
            lblmsg3.configure(text=f'ERROR while connecting database=>\n{msg}', fg='red')
            return
        result=save2cart(pId,pNumber)
        if not result:
            lblmsg3.configure(text='ERROR while connecting database', fg='red')
            return
        lblmsg3.configure(text='products saved to your cart!',fg='green')
        txtid.delete(0,'end')
        txtqnt.delete(0,'end')
        listbox.delete(0,'end')
        if result:
            sql=f'''UPDATE users SET grade=grade+1 WHERE username="{session}"  '''
            cnt.execute(sql)
            cnt.commit()


    def searchPN():
        prodname=txtprod.get()
        if len(prodname)==0:
           lblmsg3.configure(text='empty fields error!',fg='red')
        if prodname.isdigit():
           lblmsg3.configure(text='Invalid input!!',fg='red')
        else: 
            sql=f"SELECT * FROM products WHERE pname LIKE ('%{prodname}%')"
            result=cnt.execute(sql)
            rows=result.fetchall()
        
        if rows:
                for row in rows:
                    item=f'''Id={row[0]} , Name={row[1]} , Price={row[2]} , QNT={row[3]}'''
                    listbox.insert('end',item) 

                btnBuy.configure(state='active')
                txtprod.delete(0, tk.END)
                lblid.configure(state='active')
                txtid.configure(state='normal')
                lblqnt.configure(state='active')
                txtqnt.configure(state='normal')          
        else:
             lblmsg3.configure(text='No products found!',fg='red')
        cnt.commit()     
    winsearch=tk.Toplevel(win)
    winsearch.title('search')
    winsearch.geometry('400x400')
    lblprod=tk.Label(winsearch,text='product name:')
    lblprod.pack()
    txtprod=tk.Entry(winsearch)
    txtprod.pack()
    lblmsg3=tk.Label(winsearch,text='')
    lblmsg3.pack()
    btnsearch=tk.Button(winsearch,text='search product',state='active',command=searchPN)
    btnsearch.pack()
    listbox=tk.Listbox(winsearch,width=40,height=10)
    listbox.pack()
    lblid=tk.Label(winsearch,text='Id:',state='disabled')
    lblid.pack()
    txtid=tk.Entry(winsearch,state='disabled')
    txtid.pack()
    lblqnt = tk.Label(winsearch, text='numbers:',state='disabled')
    lblqnt.pack()
    txtqnt= tk.Entry(winsearch,state='disabled')
    txtqnt.pack()
    btnBuy=tk.Button(winsearch,text='buy',state='disabled',command=buy)
    btnBuy.pack()
    
#-------------------RATE------------------------------------ 
def rate():

    def pIssues():
        issue=txtprob.get()
        prname=txtpname.get()
        pscore = int(txtpscore.get())  
        global session
        id=getId(session)
        sql = f'''INSERT INTO ratings (id,username, pname,prate, pIssues) 
                  VALUES ("{id}","{session}", "{prname}", "{pscore}", "{issue}")'''
        cnt.execute(sql)
        cnt.commit()
        lblMsg3.configure(text='sorry for the experience you had,Your feedback has been successfully submitted!',fg='orange')
        lblprob.configure(state='disabled')
        lblpname.configure(state='disabled')
        lblpscore.configure(state='disabled')
        txtprob.configure(state='disabled')
        btnprob.configure(state='disabled')
        btnsave.configure(state='disabled')
        txtprob.delete(0, tk.END)
        txtpname.delete(0, tk.END)
        txtpscore.delete(0, tk.END)

    def prodExist():
        prname=txtpname.get()
        sql=f'''SELECT * FROM products WHERE pname LIKE "%{prname}%" '''
        result=cnt.execute(sql)
        rows=result.fetchall()
        return (rows)

    def save():
        prname=txtpname.get()
        pscore=txtpscore.get()

        if prname=='' or pscore=='':
           lblMsg3.configure(text='empty fields error!!!',fg='red')  
           return
        if int(pscore)>10 or int(pscore)<1:
           lblMsg3.configure(text='please choose a number between 1 to 10!',fg='red')
           return
        rows=prodExist()
        if len(rows)==0:   
            lblMsg3.configure(text='Wrong Product!', fg='red')
            return 
        if int(pscore)<5:
            lblMsg3.configure(text='What is the reason for your dissatisfaction with the product?',fg='red')
            lblprob.configure(state='active')
            txtprob.configure(state='normal')
            btnprob.configure(state='active')
        else:
            global session
            id=getId(session)
            sql = f'''INSERT INTO ratings(id, username, pname, prate, pIssues) 
                VALUES ("{id}","{session}", "{prname}", "{pscore}", " ")'''
            cnt.execute(sql)
            cnt.commit()
            lblMsg3.configure(text='Your feedback has been successfully submitted!', fg='yellow')
            lblpname.configure(state='disabled')
            lblpscore.configure(state='disabled')
            btnsave.configure(state='disabled')
            txtpname.delete(0, tk.END)
            txtpscore.delete(0, tk.END)
              
    winrate=tk.Toplevel(win)
    winrate.title('rate')
    winrate.geometry('600x300')
    lblMsg=tk.Label(winrate,text='now you can rate our products to help us to know more about your opinion!')
    lblMsg.pack()

    lblpname=tk.Label(winrate,text='product name:')
    lblpname.pack()
    txtpname=tk.Entry(winrate)
    txtpname.pack()

    lblpscore=tk.Label(winrate,text='chose a number from 1 to 10: ')
    lblpscore.pack()
    txtpscore=tk.Entry(winrate)
    txtpscore.pack()

    btnsave=tk.Button(winrate,text='save!',command=save)
    btnsave.pack()
    lblMsg3=tk.Label(winrate)
    lblMsg3.pack()

    lblprob=tk.Label(winrate,text='your issue: ',state='disabled')
    lblprob.pack()
    txtprob=tk.Entry(winrate,state='disabled')
    txtprob.pack()
    btnprob=tk.Button(winrate,text='done',state='disabled',command=pIssues)
    btnprob.pack()
    winrate.mainloop()   

#-------------- database codes ---------------
cnt=sqlite3.connect('shop.db')
# sql='''CREATE TABLE users (
#         id INTEGER PRIMARY KEY,
#         username VARCHAR(30) NOT NULL,
#         password VARCHAR(30) NOT NULL,
#         grade INTEGER NOT NULL
#         )'''
# cnt.execute(sql)

# sql='''INSERT INTO users (username,password,grade)
#         VALUES('g','1',8)'''
# cnt.execute(sql)
# cnt.commit()


# sql='''CREATE TABLE products (
#         id INTEGER PRIMARY KEY,
#         pname VARCHAR(50) NOT NULL,
#         price REAL NOT NULL,
#         quantity INTEGER NOT NULL,
#         date VARCHAR
#         )'''
# cnt.execute(sql)


# sql='''INSERT INTO products (pname,price,quantity)
#         VALUES('PHONE SAMSUNG MODEL:A51s','340',180)'''
# cnt.execute(sql)
# cnt.commit()


# sql='''CREATE TABLE cart (
#         id INTEGER PRIMARY KEY,
#         uid INTEGER NOT NULL,
#         pid INTEGER NOT NULL,
#         number INTEGER NOT NULL
#         )'''
# cnt.execute(sql)


# sql='''CREATE TABLE ratings(
#        id INTEGER,
#        username VARCHAR(50),
#        pname VARCHAR(50),
#        prate INTEGER,
#        pIssues VARCHAR(50)
#         )'''
# cnt.execute(sql)



dct={}
sql='''SELECT * FROM users'''
result=cnt.execute(sql)
columns=result.fetchall()
for column in columns:
   dct[column[1]]=column[3]
cnt.commit()    
with open("setting.json","w") as f:
    json.dump(dct,f)

#---------------- main -----------------------
session=''
win=tk.Tk()
win.title('Shop Project')
win.geometry('400x400')
lblUser=tk.Label(win,text='Username:')
lblUser.pack()
txtUser=tk.Entry(win)
txtUser.pack()
lblPas=tk.Label(win,text='Password:')
lblPas.pack()
txtPas=tk.Entry(win,show='*')
txtPas.pack()
lblMsg=tk.Label(win,text='')
lblMsg.pack()
btnLogin=tk.Button(win,text='Login',command=login)
btnLogin.pack()
btnSignup=tk.Button(win,text='Signup',command=signup)
btnSignup.pack()
btnDel=tk.Button(win,text='Delete Account!',state='disabled',command=delAccount)
btnDel.pack()
btnShop=tk.Button(win,text='Shop Panel',state='disabled',command=shopPanel)
btnShop.pack()
btnMycart=tk.Button(win,text='My Cart',state='disabled',command=showCart)
btnMycart.pack()
btnsearch=tk.Button(win,text='search product',state='disabled',command=search)
btnsearch.pack()
btnrate=tk.Button(win,text='rate',state='disabled',command=rate)
btnrate.pack()
btnMoreinfo=tk.Button(win,text='more info!',fg="gold",state='disabled',command=moreInfo)
btnMoreinfo.pack()
listbox=tk.Listbox(win,width=10,height=3,fg='gold')
listbox.pack(side=tk.LEFT, padx=10, pady=10)


win.mainloop()