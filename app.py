import streamlit as st
import sqlite3
import hashlib
import random
import pandas as pd

st.set_page_config(page_title="QuizArena", layout="wide")

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("quizarena.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
coins INTEGER,
xp INTEGER,
level INTEGER
)
""")
conn.commit()

# ---------------- FUNCTIONS ---------------- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    try:
        c.execute(
            "INSERT INTO users VALUES(?,?,?,?,?)",
            (username, hash_password(password), 100, 0, 1)
        )
        conn.commit()
        return True
    except:
        return False

def login(username, password):
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    return c.fetchone()

# ---------------- QUESTION BANK ---------------- #
quiz_data = {

"Python":[
{"q":"Python keyword to define function?","options":["def","func","define","fun"],"answer":"def"},
{"q":"Which type stores True/False?","options":["int","str","bool","float"],"answer":"bool"},
{"q":"Which symbol is used for comments?","options":["//","#","/*","--"],"answer":"#"},
{"q":"Function to print output?","options":["print()","echo()","show()","write()"],"answer":"print()"},
{"q":"Python is?","options":["Compiled","Interpreted","Machine","Assembly"],"answer":"Interpreted"},
{"q":"File extension of Python?","options":[".py",".java",".c",".cpp"],"answer":".py"},
{"q":"Which keyword loop in Python?","options":["for","loop","iterate","repeat"],"answer":"for"},
{"q":"Which datatype is immutable?","options":["list","dict","tuple","set"],"answer":"tuple"},
{"q":"Python uses indentation for?","options":["Blocks","Variables","Memory","Compilation"],"answer":"Blocks"},
{"q":"Which symbol for string?","options":["' '","//","{}","<>"],"answer":"' '"}
],

"DSA":[
{"q":"Stack follows?","options":["FIFO","LIFO","Graph","Tree"],"answer":"LIFO"},
{"q":"Queue follows?","options":["FIFO","LIFO","Graph","Tree"],"answer":"FIFO"},
{"q":"Binary Search complexity?","options":["O(n)","O(log n)","O(n²)","O(1)"],"answer":"O(log n)"},
{"q":"Linked list uses?","options":["Nodes","Arrays","Tables","Files"],"answer":"Nodes"},
{"q":"Tree root is?","options":["Top node","Leaf","Edge","Bottom"],"answer":"Top node"},
{"q":"DFS stands for?","options":["Depth First Search","Data File System","Direct File Search","None"],"answer":"Depth First Search"},
{"q":"BFS uses?","options":["Queue","Stack","Tree","Array"],"answer":"Queue"},
{"q":"Sorting best case?","options":["O(n)","O(log n)","O(n²)","O(1)"],"answer":"O(n)"},
{"q":"Array index starts from?","options":["0","1","-1","2"],"answer":"0"},
{"q":"Graph has?","options":["Vertices & Edges","Nodes only","Tables","Fields"],"answer":"Vertices & Edges"}
],

"Java":[
{"q":"Java is?","options":["Platform Independent","OS","Database","Hardware"],"answer":"Platform Independent"},
{"q":"Java extension?","options":[".java",".py",".c",".txt"],"answer":".java"},
{"q":"JVM stands for?","options":["Java Virtual Machine","Java Variable Machine","Joint VM","None"],"answer":"Java Virtual Machine"},
{"q":"Main method?","options":["main()","start()","run()","init()"],"answer":"main()"},
{"q":"Inheritance keyword?","options":["extends","inherits","implement","super"],"answer":"extends"},
{"q":"Java is?","options":["Object Oriented","Procedural","Assembly","Machine"],"answer":"Object Oriented"},
{"q":"Compile produces?","options":["Bytecode","Machine code","HTML","CSS"],"answer":"Bytecode"},
{"q":"Java runs on?","options":["JVM","Compiler","OS","RAM"],"answer":"JVM"},
{"q":"Constructor name same as?","options":["Class","Method","Object","File"],"answer":"Class"},
{"q":"Keyword for interface?","options":["interface","class","struct","enum"],"answer":"interface"}
],

"DBMS":[
{"q":"DBMS stands for?","options":["Database Management System","Data Base Main System","Digital Base System","None"],"answer":"Database Management System"},
{"q":"SQL stands for?","options":["Structured Query Language","Simple Query Language","System Query Language","None"],"answer":"Structured Query Language"},
{"q":"Primary key is?","options":["Unique","Duplicate","Null","Multiple"],"answer":"Unique"},
{"q":"SQL command to fetch data?","options":["SELECT","INSERT","DELETE","UPDATE"],"answer":"SELECT"},
{"q":"Foreign key is used for?","options":["Relationship","Deletion","Sorting","Printing"],"answer":"Relationship"},
{"q":"DBMS stores data in?","options":["Tables","Graphs","Trees","Files only"],"answer":"Tables"},
{"q":"Normalization reduces?","options":["Redundancy","Speed","CPU","Memory"],"answer":"Redundancy"},
{"q":"ER stands for?","options":["Entity Relationship","Error Report","Entity Record","None"],"answer":"Entity Relationship"},
{"q":"Database language?","options":["SQL","HTML","C","Python"],"answer":"SQL"},
{"q":"Which is NoSQL?","options":["MongoDB","MySQL","Oracle","SQLite"],"answer":"MongoDB"}
],

"C":[
{"q":"C language developer?","options":["Dennis Ritchie","James Gosling","Guido","Bjarne"],"answer":"Dennis Ritchie"},
{"q":"Header for printf()?","options":["stdio.h","math.h","string.h","conio.h"],"answer":"stdio.h"},
{"q":"Statement ends with?","options":[";",".",",",":"],"answer":";"},
{"q":"C is?","options":["Middle Level","High Level","Low Level","Machine"],"answer":"Middle Level"},
{"q":"Loop with known iterations?","options":["for","while","do","if"],"answer":"for"},
{"q":"C compiled into?","options":["Machine code","Bytecode","HTML","Java"],"answer":"Machine code"},
{"q":"Main function returns?","options":["int","void","float","char"],"answer":"int"},
{"q":"Pointer stores?","options":["Address","Value","String","Array"],"answer":"Address"},
{"q":"Array index starts?","options":["0","1","-1","2"],"answer":"0"},
{"q":"Compiler converts?","options":["Source code","Data","Memory","Output"],"answer":"Source code"}
],

"Aptitude":[
{"q":"10 + 20 = ?","options":["20","30","40","50"],"answer":"30"},
{"q":"15 × 4 = ?","options":["40","50","60","70"],"answer":"60"},
{"q":"100 / 4 = ?","options":["20","25","30","40"],"answer":"25"},
{"q":"Square of 12?","options":["144","121","100","169"],"answer":"144"},
{"q":"50% of 200?","options":["100","150","200","50"],"answer":"100"},
{"q":"25 + 25 = ?","options":["50","40","60","30"],"answer":"50"},
{"q":"9 × 9 = ?","options":["81","72","99","90"],"answer":"81"},
{"q":"80 / 2 = ?","options":["40","30","50","60"],"answer":"40"},
{"q":"1/2 of 100?","options":["50","25","100","75"],"answer":"50"},
{"q":"Square root of 49?","options":["7","6","8","9"],"answer":"7"}
]
}

# ---------------- SESSION ---------------- #
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN / REGISTER ---------------- #
if st.session_state.user is None:

    st.title("🎮 QuizArena")
    st.subheader("Learn • Play • Earn • Compete")

    menu = st.sidebar.selectbox("Choose", ["Login", "Register"])

    if menu == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if register(username, password):
                st.success("Account Created Successfully")
            else:
                st.error("Username already exists")

    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ---------------- MAIN APP ---------------- #
else:

    username = st.session_state.user

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    coins, xp, level = user[2], user[3], user[4]

    menu = st.sidebar.radio("Menu",
        ["🎮 Quiz","🏆 Leaderboard","👤 Profile","🚪 Logout"]
    )

    # ---------------- QUIZ ---------------- #
    if menu == "🎮 Quiz":

        st.header("Quiz Arena")

        subject = st.selectbox(
            "Choose Subject",
            list(quiz_data.keys())
        )

        q = random.choice(quiz_data[subject])

        st.subheader(q["q"])

        choice = st.radio("Select Answer", q["options"])

        if st.button("Submit"):

            if choice == q["answer"]:
                coins += 20
                xp += 10
                level = xp // 50 + 1

                c.execute("""
                UPDATE users
                SET coins=?,xp=?,level=?
                WHERE username=?
                """,(coins,xp,level,username))

                conn.commit()

                st.success("Correct! +20 Coins +10 XP")

            else:
                st.error("Wrong Answer")

    # ---------------- LEADERBOARD ---------------- #
    elif menu == "🏆 Leaderboard":

        st.header("Leaderboard")

        df = pd.read_sql_query("""
        SELECT username, coins, xp, level
        FROM users
        ORDER BY coins DESC
        """, conn)

        st.dataframe(df, use_container_width=True)

    # ---------------- PROFILE ---------------- #
    elif menu == "👤 Profile":

        st.header("Profile")

        st.write("👤 Username:", username)
        st.write("🪙 Coins:", coins)
        st.write("⚡ XP:", xp)
        st.write("🎮 Level:", level)

    # ---------------- LOGOUT ---------------- #
    elif menu == "🚪 Logout":
        st.session_state.user = None
        st.rerun()