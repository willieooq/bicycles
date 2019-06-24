import psycopg2

#conncect to the db

con = psycopg2.connect(
            host = 'ec2-54-83-192-245.compute-1.amazonaws.com',
            database = 'df3vg11r7cab9s',
            user = 'ouwlmxtvewdibl',
            password ='05f09b74d57c0cf93c2594966a1e03e06c7ba3605d56b46d8ecce6f61da50131',
            port = '5432')

#cursor
cur = con.cursor()

#cur.execute("insert into weather (city,date) values ('tapei','2014-11-29' )",)
#cur.execute("insert into bicycles (userid) values (UserId )")
cur.execute("insert into bicycles (userid) values ('0' )")
cur.execute("select city, date from weather")

#rows = cur.fetchall()

#commit the transcation
con.commit()

#close the cur 
cur.close()

#close the connection
con.close()
