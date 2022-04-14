import pymysql
#database connection
connection = pymysql.connect(host="db", user="root", passwd="root@123", database="TicketsList")
cursor = connection.cursor()
#inserting data to db
def add_text(ticket_data):
    cursor.execute("INSERT INTO TICKETS_DATA(TICKET_ID,TICKET_DATE) VALUES (%s, DEFAULT)",(ticket_data))
    connection.commit()
    return 1

def get_data():
    cursor.execute("SELECT TICKET_ID, DATE(TICKET_DATE) FROM TICKETS_DATA ORDER BY TICKET_DATE DESC")
    rows = cursor.fetchall()    

