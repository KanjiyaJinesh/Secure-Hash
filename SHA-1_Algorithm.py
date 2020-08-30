from tkinter import *
import sys
from tkinter import messagebox
global count_next
global result1
global result2
global Inp
count_next=0

def ENCRYPT(input_array):                              # Encrypt function returns the messagebit array which is in
    length=input_array.__len__()                       # multiple of 512.
    messagebit=[]
    for i in range(length):
        a=input_array[i]
        anss=[]
        while a!=0:
            h=a % 2
            anss.append(h)
            a=int(a/2)
        for j in range(8-anss.__len__()):
            anss.append(0)
        anss.reverse()
        for j in range(8):
            messagebit.append(anss[j])
    messagebit.append(1)
    while messagebit.__len__() % 512 != 448:
        messagebit.append(0)
    length=length*8
    ml=[0]*64
    p=63
    while (length!=0):
        h=length % 2
        ml[p]=h
        length=int(length/2)
        p=p-1
    for j in range(64):
        messagebit.append(ml[j])
    return messagebit

def HASH(inp):                                      # This is the main function which returns the digest on clicking the 
    inp=[ord(c) for c in inp]                       # Generate Hash button.
    messagebit=ENCRYPT(inp)

    # Initializing A,B,C,D,E.
    A=[0,1,1,0,0,1,1,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,1];    # A=[67452301] <- this is in hexadecimal form
    B=[1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,0,1,0,0,1];    # B=[efcdab89]
    C=[1,0,0,1,1,0,0,0,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,0,1,1,1,1,1,1,1,0];    # C=[98badcfe]
    D=[0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,1,0,1,0,0,0,1,1,1,0,1,1,0];    # D=[10325476]
    E=[1,1,0,0,0,0,1,1,1,1,0,1,0,0,1,0,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0];    # E=[c3d2e1f0]

    size=messagebit.__len__()
    nn=0
    for n in range(0,size,512):
        w=[]

        for i in range(nn,nn+16):
            temp=[]
            for j in range((i*32),((i+1)*32)):
                temp.append(messagebit[j])
            w.append(temp)
        for i in range(16,80):
            temp=XOR_of_four(w[i-3],w[i-8],w[i-14],w[i-16])
            w.append(left_rotate(temp,1))
        
        a=A.copy()
        b=B.copy()
        c=C.copy()
        d=D.copy()
        e=E.copy()
        zeros=[0]*32
        for i in range(80):
            if (i>=0 and i<20):
                F=OR_of_three(AND(b,c) , AND(NOT(b),d) , zeros)
                k=[0,1,0,1,1,0,1,0,1,0,0,0,0,0,1,0,0,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1];    # k=[5A827999] <- this is in hexadecimal form
            elif (i>=20 and i<40):
                F = XOR_of_four(b,c,d,[0]*32)
                k=[0,1,1,0,1,1,1,0,1,1,0,1,1,0,0,1,1,1,1,0,1,0,1,1,1,0,1,0,0,0,0,1];    # k=[6ED9EBA1]
            elif (i>=40 and i<60):
                F = OR_of_three( AND(b,c) , AND(b,d) , AND(c,d))
                k=[1,0,0,0,1,1,1,1,0,0,0,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,0,1,1,1,0,0];    # k=[8F1BBCDC]
            else:
                F = XOR_of_four(b,c,d,zeros)
                k=[1,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,1,1,1,0,1,0,1,1,0];    # k=[CA62C1D6]

            temp=ADD_of_five(left_rotate(a,5),F,e,k,w[i])
            e=d.copy()
            d=c.copy()
            c=left_rotate(b,30)
            b=a.copy()
            a=temp.copy()

        A=ADD_of_two(A,a)
        B=ADD_of_two(B,b)
        C=ADD_of_two(C,c)
        D=ADD_of_two(D,d)
        E=ADD_of_two(E,e)

        nn=nn+16
    
    dig=get_digest(A + B + C + D + E)
    return dig

def left_rotate(A,n):                               # This function raotates the 'A' in left direction by n digits.
    temp=[]
    for i in range(n,32):
        temp.append(A[i])
    for i in range(0,n):
        temp.append(A[i])
    return temp.copy()

def XOR_of_four(A,B,C,D):                           # This function does the XOR of 'A','B','C' and 'D'
    temp=[]
    
    for i in range(32):
        temp.append( (A[i]+B[i]+C[i]+D[i]) % 2)
    return temp.copy()

def AND(A,B):                                       # This function does AND operation between 'A' and 'B'
    temp=[]
    for i in range(32):
        if (A[i]==1 and B[i]==1):
            temp.append(1)
        else:
            temp.append(0)
    return temp.copy()

def OR_of_three(A,B,C):                             # This function does OR operation of 'A','B' and 'C'
    temp=[]
    for i in range(32):
        if(A[i]==0 and B[i]==0 and C[i]==0):
            temp.append(0)
        else:
            temp.append(1)
    return temp.copy()

def NOT(A):                                         # This function does NOT operation of 'A'
    temp=[]
    for i in range(32):
        temp.append((A[i]+1) % 2)
    return temp.copy()

def ADD_of_two(A,B):                                # This operation raturns the addition of two variable 'A' and 'B'
    temp=[]
    carry=0
    for i in range(32):
        sum=carry + A[31-i] + B[31-i]
        if (sum % 2==0):
            temp.append(0)
            carry=int(sum/2)
        else:
            temp.append(1)
            carry=int((sum-1)/2)
    temp.reverse()
    return temp.copy()

def ADD_of_five(A,B,C,D,E):                        # This operation raturns the addition of five variable 'A','B','C','D' and 'E'
    temp=[]
    carry=0
    for i in range(32):
        sum=carry + A[31-i] + B[31-i] + C[31-i] + D[31-i] + E[31-i]
        if (sum % 2==0):
            temp.append(0)
            carry=int(sum/2)
        else:
            temp.append(1)
            carry=int((sum-1)/2)
    temp.reverse()
    return temp.copy()

def get_digest(A):                                 # This function returns the hexadecimal string of 'A'
    s=''
    for i in range(0,160,4):
        an=A[i]*8 + A[i+1]*4 + A[i+2]*2 + A[i+3]
        if (an<=9):
            an=str(an)
        elif (an==10):
            an='a'
        elif (an==11):
            an='b'
        elif (an==12):
            an='c'
        elif (an==13):
            an='d'
        elif (an==14):
            an='e'
        else:
            an='f'
        s=s+an
    return s

def chekinput():                                  # This function checks if the input is right form or not 
    global count_next
    global Inp
    v=0
    x=Inp.get()
    if len(x)==0:
        messagebox.showerror("Error","Please enter input.")
        v=1
        #count_next=1
    else:
        for i in range(len(x)):
            if x[i]==" ":
                messagebox.showinfo("Information","Space is not allowed. Here I am assuming the input in password form.")
                v=1
                #count_next=1
                Inp.delete(0,END)
                break
    return v



def onclick():                                    #  definition for onclick function
    global count_next
    global result1
    global result2
    global Inp
    c=chekinput()
    if (count_next==0 and c==0):
        password=HASH(Inp.get())
        count_next=1
        result1=Label(window,text="The digest is  :",font=("arial",13,"bold"),width=12)
        result1.place(x=70,y=210)
        result2=Label(window,text=password,font=("arial",12))
        result2.place(x=80,y=250)

def exit1():
    window.destroy()

def reset():
    global result1
    global result2
    global count_next
    global Inp
    count_next=0
    Inp.delete(0,END)
    result1.destroy()
    result2.destroy()

if __name__=="__main__" :                          #  this will generate the GUI for hash generation
    
    window = Tk()
    window.geometry("500x500")
    window.title("Hash Generator")
    #window.configure(bg="white")
    L1 = Label(window, text="SHA-1 Generator",relief="solid",font=("arial",19,"bold"),width=20)
    L1.place(x=90,y=53)
    L2 = Label(window, text="Enter Input  :",font=("arial",13,"bold"),width=10)
    L2.place(x=70,y=120)

    btn1=Button(window,text="generate hash",width=18,bg='green',fg='white',command=onclick)
    btn1.place(x=220,y=160)
    btn2=Button(window,text="Reset",width=12,bg='blue',fg='white',command=reset)
    btn2.place(x=135,y=380)
    btn2=Button(window,text="exit",width=12,bg='red',fg='white',command=exit1)
    btn2.place(x=265,y=380)

    Inp=Entry(window,width=30)
    Inp.place(x=220,y=120)

    window.mainloop()
