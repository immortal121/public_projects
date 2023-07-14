import discord
import sqlite3
import re
import gspread
import asyncio
import time
import datetime

Bot = False

gc = gspread.service_account(filename='google.json')

worksheet = gc.open_by_key("1lNbcKgcG_4gJT2vV0tCEG6aPgBU3p1OCtlNIdY6AKB4")


current_sheet = worksheet.worksheet('Reportsheet')

# Connect to the database
conn = sqlite3.connect('betburger.db')

# Create a cursor
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS USER (id INTEGER PRIMARY KEY, username TEXT , Uid INTEGER,Active BOOLEAN DEFAULT True)')
cursor.execute("CREATE TABLE IF NOT EXISTS DISCORDMSG (id INTEGER PRIMARY KEY,MSG INTEGER,ChannelId INTEGER,MSGID INTEGER)")

cursor.execute("CREATE TABLE IF NOT EXISTS USERORDERS (id INTEGER PRIMARY KEY,Uid INTEGER,EventName TEXT,created_time TEXT)")
cursor.execute("DELETE FROM USERORDERS")
conn.commit()

def remove_link_chars(string):
    string = str(string)
    return string.replace("%","")

def get_match(statement):
    regex = r"^(\d+\.\d+)-(\d+)$"
    regex2 = r"^(\d+)-(\d+)$"
    match = re.search(regex, statement)
    match2 = re.search(regex2,statement)
    if match or match2:
        return True
    else:
        return False
  
async def msg_on_update(cursor,conn):
    sql = "SELECT * FROM messages where updated = True"
    cursor.execute(sql)
    update_rows = cursor.fetchall()
    if update_rows:
        for urow in update_rows:
            sql2 = f"SELECT * FROM DISCORDMSG WHERE MSG = {urow[0]}"
            cursor.execute(sql2)
            msg_rows = cursor.fetchall()
            if msg_rows:
                for msg_row in msg_rows:
                    channel = client.get_channel(msg_row[2]) # the message's channel
                    if channel is not None:
                        Msg = await channel.fetch_message(msg_row[3])
                        EventName = urow[1]
                        Link = urow[2]
                        Bookie = urow[5]
                        EventStart = urow[6]
                        Market = urow[7]
                        CurrentOdds = urow[8]
                        LastAcceptedOdds = urow[9]
                        Value = urow[3]
                        Link = remove_link_chars(Link)
                        if Link is not None:
                            msg = f"""\n\n**Event Name** : {EventName}\n\n**Booker Name** : {Bookie}\n\n**LINK :** {Link}\n\n **Time Of The Match **: {EventStart}\n\n**Market**: {Market}\n\n**Current Odds** : {CurrentOdds}\n\n**Value (Edge)** : {Value}\n\n**Last Acceptable Odds** : {LastAcceptedOdds}\n"""
                            dummy = await Msg.edit(content=msg)  
                            sql_new = f"UPDATE messages SET Updated = False WHERE id = {urow[0]}"
                            cursor.execute(sql_new)
                            conn.commit()          


async def msg_on_new(cursor,conn):
    sql = "SELECT * FROM messages where New = True"
    cursor.execute(sql)
    new_rows = cursor.fetchall()
    if new_rows:
        for new_row in new_rows:
            sql2 = "SELECT * FROM USER where Active = True"
            cursor.execute(sql2)
            msg_rows = cursor.fetchall()
            if msg_rows:
                for msg_row in msg_rows:
                    sql3 = f"SELECT * FROM USERORDERS WHERE Uid = {msg_row[2]} AND EventName = '{new_row[1]}'"
                    cursor.execute(sql3)
                    present_order = cursor.fetchall()
                    if present_order:
                        pass
                    else:
                        user_id = msg_row[2]
                        user =await client.fetch_user(user_id)
                        EventName = new_row[1]
                        Bookie = new_row[5]
                        EventStart = new_row[6]
                        Market = new_row[7]
                        CurrentOdds = new_row[8]
                        LastAcceptedOdds = new_row[9]
                        Value = new_row[3]
                        Link = new_row[2]
                        Link = remove_link_chars(Link)
                        if Link is not None:
                            msg = f"""\n**Event Name** : {EventName}\n\n**Booker Name** : {Bookie}\n\n**LINK :** {Link}\n\n **Time Of The Match **: {EventStart}\n\n**Market**: {Market}\n\n**Current Odds** : {CurrentOdds}\n\n**Value (Edge)** : {Value}\n\n**Last Acceptable Odds** : {LastAcceptedOdds}\n"""
                            send = await user.send(msg)
                            channelid = send.channel.id
                            msgid = send.id
    
                            sql_I = f"INSERT INTO DISCORDMSG (MSG,ChannelId, MSGID) VALUES ({new_row[0]},{channelid},{msgid})"
                            cursor.execute(sql_I)
                            conn.commit()
                            sql_new = f"UPDATE messages SET New = False WHERE id = {new_row[0]}"
                            cursor.execute(sql_new)
                            conn.commit()
async def delete_orders_day_ago(cursor,conn):
    try:
        current_time = datetime.datetime.now()
        one_day_ago = current_time - datetime.timedelta(days=1)
        cursor.execute(f"DELETE FROM USERORDERS WHERE created_time < '{one_day_ago}'")
        conn.commit()
    except:
        pass

async def msg_to_delete(cursor,conn):
    try:

        sql = "SELECT * FROM messages where onDelete = True"
        cursor.execute(sql)
        delete_rows = cursor.fetchall()
        if delete_rows:
            for drow in delete_rows:
                sql2 = f"SELECT * FROM DISCORDMSG WHERE MSG = {drow[0]}"
                cursor.execute(sql2)
                msg_rows = cursor.fetchall()
                for msg_row in msg_rows:
                    channel = client.get_channel(msg_row[2]) # the message's channel

                    if channel is not None:
                        Msg = await channel.fetch_message(msg_row[3])
                        EventName = drow[1]
                        Link = drow[2]
                        Bookie = drow[5]
                        EventStart = drow[6]
                        Market = drow[7]
                        CurrentOdds = drow[8]
                        LastAcceptedOdds = drow[9]
                        Value = drow[3]
                        Link = remove_link_chars(Link)
                        msg = f"""\n\n***EVENT WILL DISAPPEAR IN ONE MINUTE***\n**Event Name** : {EventName}\n\n**Booker Name** : {Bookie}\n\n**LINK :** {Link}\n\n **Time Of The Match **: {EventStart}\n\n**Market**: {Market}\n\n**Current Odds** : {CurrentOdds}\n\n**Value (Edge)** : {Value}\n\n**Last Acceptable Odds** : {LastAcceptedOdds}\n"""
                
                        dummy = await Msg.edit(content=msg)  
                        sql_new = f"UPDATE messages SET onDelete = False,Deleted = True WHERE id = {drow[0]}"
                        cursor.execute(sql_new)
                        conn.commit() 
                await asyncio.sleep(50)
                for msg_row in msg_rows:
                    channel = client.get_channel(msg_row[2]) # the message's channel

                    if channel is not None:
                        Msg = await channel.fetch_message(msg_row[3])
                        dummy = await Msg.delete() 
                        try:
                            sql_new = f"DELETE FROM messages WHERE id= {drow[0]}"
                            cursor.execute(sql_new)
                            conn.commit() 
                        except:
                            pass
                        print("deleted")
    except:
        pass
          
      

def get_two_numbers(statement):
    """Gets the two numbers from the match."""
    regex = r"(-?\d+)-(-?\d+)"
    regex2 = r"(\d+\.\d+)-(-?\d+)"
    match2 = re.search(regex2,statement)
    match = re.search(regex, statement)
    if match:
        first_number = float(match.group(1))
        second_number = float(match.group(2))
    if match2:
        first_number = float(match2.group(1))
        second_number = float(match2.group(2))

    return first_number, second_number

def list_to_string(list):
    """Converts a list to a string."""
    items = []
    for item in list:
        items.append(str(item))
    return items

client = discord.Client(intents = discord.Intents.default())

@client.event
async def on_ready():
    print("BETBURGER-Bot is Ready")

@client.event
async def on_message(message):
    global Bot
    if message.content == "@ENDBOTNOW":
        await message.author.send("SUCCESSFULLY BOT STOP")
        Bot = False
        time.sleep(5)

    if message.content == "@STARTBOTNOW":
           await message.author.send("SUCCESSFULLY BOT CONNECTED")
           Bot = True
           while Bot:
            await msg_on_update(cursor,conn)
            await msg_on_new(cursor,conn)
            await msg_to_delete(cursor,conn)
            await delete_orders_day_ago(cursor,conn)
            await asyncio.sleep(2)
          
    
    # channel = 0
    if (message.author != client.user) and Bot:
        sql = f"SELECT * FROM USER WHERE Uid = {message.author.id}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = len(rows)
        if rows == 0:
            sql = f"INSERT INTO USER (username, Uid) VALUES ('{message.author}',{message.author.id})"
            cursor.execute(sql)       
            conn.commit()
        
    
    if message.content == "STARTNOW":
        sql = f"UPDATE USER SET Active = True WHERE Uid = {message.author.id}"
        cursor.execute(sql)
        conn.commit()
        await message.author.send("SUCCESSFULLY CONNECTED")

    if message.content == 'STOPNOW':
        sql = f"UPDATE USER SET Active = False WHERE Uid = {message.author.id}"
        cursor.execute(sql)
        conn.commit()
        await message.author.send("SUCCESSFULLY DISCONNECTED")

    if message.author == client.user:
            return    
   
    if (message.content == "hello") or (message.content == "hi") and Bot:
        await message.author.send(f"Hello {message.author} ,From Now you get all bets")

    if get_match(message.content) and Bot:
        first_number, second_number = get_two_numbers(message.content)
        try:
            message_id = message.reference.message_id
        except:
            message_id = None

        if message_id is not None:
            sql = f"SELECT MSG FROM DISCORDMSG WHERE MSGID = {message_id}"
            cursor.execute(sql)
            msg = cursor.fetchone()
            if msg:
                sqll = f"SELECT * FROM messages WHERE id = {msg[0]}"
                cursor.execute(sqll)
                row = cursor.fetchone()

                if row:
                    UserName = message.author
                    Date = message.created_at
                    EventName = row[1]
                    Bookie = row[5]
                    EventStart = row[6]
                    Time_To_Event = ""
                    Market = row[7]
                    CurrentOdds = row[8]
                    LastAcceptedOdds = row[9]
                    PlacedOdds = first_number
                    Amt = second_number
                    items = list_to_string([UserName,Date,EventName,Bookie,EventStart,Time_To_Event,Market,CurrentOdds,LastAcceptedOdds,PlacedOdds,Amt])
                    try:
                        current_sheet.append_row(items)
                        await message.author.send("Your bet was saved!\nEventName :"+EventName)
                        sql_p = f"INSERT INTO USERORDERS (Uid,EventName,created_time) VALUES ({message.author.id},'{EventName}','{datatime.datatime.now()}')"
                        cursor.execute(sql_p)
                        conn.commit()
                    except:
                        pass
                else:
                    await message.author.send("Your bet didn't saved!, Some Exception Occured")
           

    



client.run("MTEyNTc1NDU5Nzk5OTM5NDg4OA.GpXLGJ.BjdMvxUNGCVXnKVlosA9qYAT2-5jR-uco9usYo")
