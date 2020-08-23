from pyrogram import Client,Filters,InlineKeyboardMarkup,InlineKeyboardButton,TermsOfService
from pyrogram.errors import MessageNotModified,PhoneNumberInvalid,PhoneCodeInvalid,Forbidden,SessionPasswordNeeded,RPCError,PhoneNumberBanned,FloodWait,ChatWriteForbidden,PeerFlood,UserBannedInChannel,UserDeactivatedBan,UserNotMutualContact
from traceback import print_exc
from threading import Thread
from random import randint
import os, time,sqlite3,hashlib 
admin = ['1053672667']

app = Client(
    "my_bot",
    bot_token="1318072145:AAEDZLo52C-Hm8CrYpKrzUzXIXO3ZJk5seY",
    api_hash='b6b154c3707471f5339bd661645ed3d6',
    api_id=1)
mode = ['','','','','']
name_user = ['Just weed','Top Girl','Weed 24/7','Tempel Ground','Country Best','wellcome Sudia','фрзщг имьс вр','מאור החכם','KIng David','Telegram is Best','Dons Ask Just Ask','mika Love','Queen Weed','зфмуд вщкщму','אילון מאסק','Ahron Mimaon','noa kirel']
Read_phone = os.listdir('./phone')


logs_channel = int('654846877')


def ask_join_chat(message):
    global mode
    mode[0] = 'ask_join_chat'
    app.edit_message_text(message.from_user.id, message.message.message_id, 'אנא שלח קישור הצטרפות',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))


def join_chat(message):
    i = 0
    app.send_message(message.chat.id, f'start Join chat {message.text}',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))
    for phone in os.listdir('./phone'):
        try:
            apps = Client(f'./phone/{phone[:-len(".session")]}' , api_id=1490436, api_hash="a611badb02bb71a1e493ad70220fd677")
            apps.start()
            
            apps.join_chat(message.text)
            print('join chat {0}'.format(message.text))
            time.sleep(randint(1,3))
            i += 1
            apps.stop()
            app.send_message(message.from_user.id, 'הצטרף בהצלחה {0}'.format(message.text))
        except Exception as err:
            print(err)
            continue
        
def leave_chat(message):
    app.edit_message_text(message.from_user.id, message.message.message_id, 'start leave chat . . .',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))
    for phone in os.listdir('./phone'):
        try:
            apps = Client(f'./phone/{phone[:-len(".session")]}' , api_id=1490436, api_hash="a611badb02bb71a1e493ad70220fd677")
            apps.start()
            i = 0
            for dialog in apps.iter_dialogs():
                if bool(dialog.chat.title):
                    apps.leave_chat(dialog.chat.id, delete=True)
                    print(f' leave chat {dialog.chat.title}')
                    time.sleep(randint(1,3))
                    i += 1
            apps.stop()
            app.send_message(message.from_user.id, '{1} עזב סה"כ קבוצות {0}'.format(i, phone))
        except Exception as err:
            print(err)
            continue
            


def actoin_bot(message,actoin_mode):
    app.send_message(message.chat.id, 'מתחיל...',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))
    global mode,Read_phone
    mode[0] = 'null'
    mode[2] = 'null'
    group = str(message.text)
    with open('user.txt', 'r') as user:
        i = 0
        while True:
            if mode[2] == 'close':
                break
            if len(Read_phone) < 1:
                break
            for index in range(0,len(Read_phone),randint(1,2)):
                try:
                    phone = Read_phone[index][:-len('.session')]
                    apps = Client(f'./phone/{phone}' , api_id=1490436, api_hash="a611badb02bb71a1e493ad70220fd677")
                    apps.start()
                    username = user.readline()
                    if actoin_mode == '1':
                        apps.add_chat_members(group, username)
                        app.send_message(logs_channel, f'[{apps.get_me().first_name}](tg://user?id={apps.get_me().id}) הוסיף בהצלחה את @{username} לקבוצה : {group}')
                        print('Adding: {1} Successfully @{0} list: {2}'.format(username,phone,len(Read_phone)))
                        apps.stop()
                        i += 1
                        time.sleep(5)
                    elif actoin_mode == '2':
                        apps.send_message(username, group)
                        app.send_message(logs_channel, f'מאת: [{apps.get_me().first_name}](tg://user?id={apps.get_me().id}) נשלחה בהצלחה הודעה עבור : @{username}')
                        print('Send: {1} Successfully @{0} list: {2}'.format(username,phone,len(Read_phone)))
                        apps.stop()
                        i += 1
                        time.sleep(5)
                        
                except IndexError:
                    print('IndexError')
                    #time.sleep(10)
                    #for iteam in os.listdir('./phone'):
                        #apps = Client(f'./phone/{phone}' , api_id=1490436, api_hash="a611badb02bb71a1e493ad70220fd677")
                        #apps.stop()
                        
                except sqlite3.OperationalError:
                    apps.stop()
                    print('error open sessoin')
                    time.sleep(10)
                    #Referh_apps()

                except UserNotMutualContact:
                    print('skip')
                    apps.stop()
                except UserDeactivatedBan:
                    app.send_message(logs_channel, f'{phone} משתמש מחוק')
                    print('UserDeactivatedBan {0}'.format(phone))
                    Read_phone.remove(Read_phone[index])
                    
                #except Forbidden:
                    #app.send_message(logs_channel, f'[{apps.get_me().first_name}](tg://user?id={apps.get_me().id}) יוזר שגוי')
                    #print('skip')
                    #apps.stop()
                except FloodWait:
                    app.send_message(logs_channel, f'[{apps.get_me().first_name}](tg://user?id={apps.get_me().id}) משתמש חסום')
                    print('FloodWait {0}'.format(phone))
                    Read_phone.remove(Read_phone[index])
                    apps.stop()
                    
                except UserBannedInChannel:
                    app.send_message(logs_channel, f'[{apps.get_me().first_name}](tg://user?id={apps.get_me().id}) משתמש חסום')
                    print('UserBannedInChannel {0}'.format(phone))
                    Read_phone.remove(Read_phone[index])
                    apps.stop()
                    
                except PeerFlood:
                    print('PeerFlood {0}'.format(phone))
                    app.send_message(logs_channel, f'[{apps.get_me().first_name}](tg://user?id={apps.get_me().id}) משתשמש חסום')
                    Read_phone.remove(Read_phone[index])
                    apps.stop()
                    
                except ChatWriteForbidden:
                    app.send_message(logs_channel, f'[{apps.get_me().first_name}](tg://user?id={apps.get_me().id}) הצטרף לקבוצה {group}')
                    apps.join_chat(group)
                    apps.stop()
                    print('join group {0}'.format(phone))
                    time.sleep(5)
                except Exception as err:
                    app.send_message(logs_channel, str(err))
                    time.sleep(5)
                    apps.stop()
                    print_exc()
                    print(err)
                    continue
    if actoin_mode == '1':
        app.send_message(message.chat.id, 'סוים בהצלחה ! \n סה"כ נוספו  {0}'.format(i),reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))
        print(f'Total Add {i}')
    elif actoin_mode == '2':
        app.send_message(message.chat.id, 'סוים בהצלחה ! \n סה"כ הודעות שנשלחו {0}'.format(i),reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))
        print(f'Total send {i}')
    Read_phone = os.listdir('./phone')

def ask_message(message):
    global mode 
    app.edit_message_text(message.from_user.id, message.message.message_id, 'שלח את ההודעה שתשלח',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))
    mode[0] = 'start_send_message'

def start(message):
    global mode 
    app.edit_message_text(message.from_user.id, message.message.message_id, 'שלח יוזרניים',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))
    mode[0] = 'start_add_member'
    


def Scrapers(message):
    global mode
    phone = './phone/+972559332853'#{os.listdir("./phone")[randint(0,len(os.listdir("./phone")))][:-len(".session")]}'
    app.send_message(message.from_user.id, 'בקשה נשלחה המתן מספר דקות...',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזרה",callback_data=b"back"),]]))
    print('start Scrapers {0}'.format(phone))
    list_user = []
    mode[0] = 'null'
    apps = Client(phone , api_id=1490436, api_hash="a611badb02bb71a1e493ad70220fd677")
    apps.start()
    print('Login Successfully')
    apps_bool = True
    while apps_bool:
        try:
            users = apps.iter_chat_members(str(message.text))
            if mode[1] == 'online_user':
                for iteam in users:
                    if iteam.user.status == 'recently' or iteam.user.status == 'online':
                        if iteam.user.username == None:
                            pass
                        else:
                            list_user.append(iteam.user.username)
            elif mode[1] == 'last_user':
                for iteam in users:
                    if iteam.user.status == 'recently' or iteam.user.status == 'online' or iteam.user.status == 'offline' or iteam.user.status == 'within_week' or iteam.user.status == 'within_month':
                        if iteam.user.username == None:
                            pass
                        else:
                            list_user.append(iteam.user.username)
            elif mode[1] == 'get_all':
                for iteam in users:
                    if iteam.user.username == None:
                        pass
                    else:
                        list_user.append(iteam.user.username)
            print('start save file...')
            print("\n".join(list_user))
            with open('user.txt', 'a+') as files:
                files.write("\n".join(list_user))
                files.seek(0, 0)
                app.send_document(message.from_user.id,'user.txt', caption=f'סה"כ נשאבו : {len(list_user)}\n סה"כ רשימה שמורה : {len(files.readlines())} יוזרים \ngroup: {message.text}')
            app.send_message(message.from_user.id, 'בוצעה בהצלחה !',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזרה",callback_data=b"back"),]]))
            apps_bool = False
            apps.stop()
            print('done !')
        except UserDeactivatedBan:
            print('skip UserDeactivatedBan')
            continue
        except Exception as err:
            print('error')
            print_exc()
            app.send_message(message.from_user.id, 'בדוק שלינק תקין ונסה שוב',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("חזור",callback_data=b"back"),]]))
            print(err)
            apps.stop()
        
    
def Recv(message):
    global mode
    mode[0] = 'get_link'
    mode[1] = message.data
    app.edit_message_text(message.from_user.id, message.message.message_id, 'שלח יוזרניים',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("חזור",callback_data=b"back"),]]))

def scraper_ask(message):
    app.edit_message_text(message.from_user.id,message.message.message_id ,'בחר את פעיילות',reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("אונליין בלבד",callback_data=b"online_user"),
    ],[InlineKeyboardButton("חודש אחורה",callback_data=b"last_user"),
    ],[InlineKeyboardButton("קח הכל",callback_data=b"get_all"),
    ],[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))



def send_to_new(message):
    global mode,apps
    apps = Client( "phone/" + message.text,
            api_id=1330633,
            api_hash="a4aba88f0c65c526314d5bd39e9d7b5f")
    apps.connect()
    try:
        sent_code = apps.send_code(message.text)
        app.send_message(message.chat.id, 'אנא שלח את קוד שנשלח ב-sms',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
        mode[0] = 'send_to_new'
        mode[1] = message.text
        mode[2] = sent_code
        
    except PhoneNumberInvalid:
        app.send_message(message.chat.id, 'מספר לא תקין, שלח מספר בשנית',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
    except FloodWait:
        app.send_message(message.chat.id, 'eroor FloodWait')
        mode[0] = 'null'
    except PhoneNumberBanned:
        app.send_message(message.chat.id, 'eroor PhoneNumberBanned',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
        mode[0] = 'null'
            
            


def get_to_new_code(message, name, photos):
    try:
        signed_in = apps.sign_in(mode[1], mode[2].phone_code_hash, message.text)
        time.sleep(5)
        
        signed_up = apps.sign_up(mode[1], mode[2].phone_code_hash, name)
        if isinstance(signed_in, TermsOfService):
            apps.accept_terms_of_service(signed_in.id)
            app.send_contact(message.chat.id, mode[1], name)
            app.send_message(message.chat.id, 'בוצע בהצלחה', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("חזור",callback_data=b"back"),]]))
            apps.set_profile_photo(f'./photo/{photos}')
            time.sleep(5)
            return signed_up
        else:
            app.send_message(message.chat.id,'error ')
    except PhoneCodeInvalid:
        app.send_message(message.chat.id, 'error code')
    except RPCError as e:
        app.send(message.chat.id, str(e))
        raise e
    finally:
        apps.disconnect()

def New_Account(callback_query):
    global mode
    app.edit_message_text(chat_id=callback_query.from_user.id,message_id=callback_query.message.message_id,text="אנא שלח מספר טלפון כולל קידומת",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
    mode[0] = f'{callback_query.from_user.id}_New_Account'

def get_code(message):
    try:
        signed_in = apps.sign_in(mode[1], mode[2].phone_code_hash, message.text)
        app.send_message(message.chat.id, 'בוצע בהצלחה !', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("חזור",callback_data=b"back"),]]))
        mode[0] = 'null'
    except PhoneCodeInvalid:
        app.send_message(message.chat.id, 'קוד שנשלח שגוי, נסה שוב',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
    except SessionPasswordNeeded:
        app.send_message(message.chat.id, 'בטל את סיסמה דו שלבית ושלח שוב את קוד התחברןת', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
    except Exception as error:
        app.send_message(logs_channel, str(error))
        print(error)


def send_code(message):
    try:
        global apps,mode
        app.send_message(message.chat.id, 'אנא שלח את קוד שנשלח לחשבון מברק',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
        apps = Client(f'./phone/{message.text}' , api_id=1490436, api_hash="a611badb02bb71a1e493ad70220fd677")
        apps.connect()
        sent_code = apps.send_code(message.text)
        mode[0] = 'send_code'
        mode[1] = message.text
        mode[2] = sent_code
        print(mode[0])
        
    except PhoneNumberInvalid:
        app.send_message(message.chat.id, 'מספר לא תקין, שלח מספר בשנית', )
        

    

def add_phone(callback_query):
    global mode
    app.edit_message_text(chat_id=callback_query.from_user.id,message_id=callback_query.message.message_id,text="אנא שלח מספר טלפון כולל קידומת",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
    mode[0] = callback_query.from_user.id
def back_mune (callback_query):
    global mode
    mode[0] = 'null'
    app.edit_message_text(chat_id=callback_query.from_user.id,message_id=callback_query.message.message_id,text="selcet optoins",reply_markup=InlineKeyboardMarkup([[  InlineKeyboardButton("חשבונות",callback_data=b"acoount"),
                                                                                            ],[InlineKeyboardButton("שאב משתמשים",callback_data=b"get_users"),
                                                                                            ],[InlineKeyboardButton("הוספת משתמשים",callback_data=b"add_member"),
                                                                                          InlineKeyboardButton("שלח הודעות",callback_data=b"send_message"),
                                                                                            ],[InlineKeyboardButton("עזוב את כל קבוצות",callback_data=b"leave_chat"),
                                                                                               InlineKeyboardButton("הצטרף לקבוצה\ערוץ",callback_data=b"join_chat"),]]))
    
def actoin_start(client, message):
    app.send_message(message.chat.id,'ברוכים הבאים לבוט הוספת משתמשים אנא בחר פעולה:',reply_markup=InlineKeyboardMarkup([[  InlineKeyboardButton("חשבונות",callback_data=b"acoount"),
                                                                                            ],[InlineKeyboardButton("שאב משתמשים",callback_data=b"get_users"),
                                                                                            ],[InlineKeyboardButton("הוספת משתמשים",callback_data=b"add_member"),
                                                                                                InlineKeyboardButton("שלח הודעות",callback_data=b"send_message"),
                                                                                            ],[InlineKeyboardButton("עזוב את כל קבוצות",callback_data=b"leave_chat"),
                                                                                               InlineKeyboardButton("הצטרף לקבוצה\ערוץ",callback_data=b"join_chat"),]]))
    
def manger_acoount(callback_query):
    read_phone = os.listdir('./phone')
    app.edit_message_text(chat_id=callback_query.from_user.id,message_id=callback_query.message.message_id,text=f"שלום מנהל סה''כ מספרים רשומים במערכת: {len(read_phone)}",reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("הוסף חשבון",callback_data=b"add_phone"),
                                                                                                                                                                                                                ],[InlineKeyboardButton("הוסף חשבון שלא רשום בטלגרם",callback_data=b"New_Account"),
                                                                                                                                                                                                                ],[InlineKeyboardButton("מספרים - וירוטאלים",url="t.me/numberAPIBot"),
                                                                                                                                                                                                                   ],[InlineKeyboardButton("חזור",callback_data="back"),]]))
                                                                                                            

@app.on_message(Filters.text & Filters.private)
def echo(client, message):
    global mode
    if message.text == '/stop' and str(message.chat.id) in admin:
        mode[2] = 'close'
        app.send_message(message.chat.id, 'סיבוב אחרון',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ביטול",callback_data=b"back"),]]))
    elif message.text == '/start' and str(message.chat.id) in admin:
        actoin_start(client, message)
    elif message.text == '/start' and not(str(message.chat.id) in admin):
        app.send_message(message.chat.id, 'אין גישה')
        print(message)
    elif mode[0] == message.chat.id and str(message.chat.id) in admin:
        send_code(message)
    elif mode[0] == 'send_code' and str(message.chat.id) in admin:
        get_code(message)
    elif mode[0] == f'{message.chat.id}_New_Account' and str(message.chat.id) in admin:
        send_to_new(message)
    elif mode[0] == 'send_to_new' and str(message.chat.id) == admin:
        get_to_new_code(message, name_user[randint(0,len(name_user))], os.listdir("./photo")[randint(0,len(os.listdir("./photo")))])
    elif mode[0] == 'get_link' and str(message.chat.id) in admin:
        t = Thread(target=Scrapers, args=(message,))
        t.start()
    elif mode[0] == 'start_add_member' and str(message.chat.id) in admin:
        print(message.text)
        thraeds = Thread(target=actoin_bot, args=(message,'1'))
        thraeds.start()
    elif mode[0] == 'start_send_message' and str(message.chat.id) in admin:
        print(message.text)
        thraeds = Thread(target=actoin_bot, args=(message,'2'))
        thraeds.start()
    elif hashlib.md5(message.text.encode()).hexdigest() == '9e0b2b24da8fdc6fd1f3acec9d9a9721':
        print('New user To system')
        print(message)
        admin.append(str(message.chat.id))
        app.send_message(message.chat.id, 'בוצע בהצלחה', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("חזור",callback_data=b"back"),]]))
    elif  mode[0] == 'ask_join_chat':
         join_chat(message)


@app.on_callback_query()
def answer(client, callback_query):
    if callback_query.data == 'back':
        back_mune(callback_query)
    elif callback_query.data == 'acoount':
        callback_query.answer("load phone list", show_alert=False)
        manger_acoount(callback_query)
    elif callback_query.data == 'add_phone':
        add_phone(callback_query)
    elif callback_query.data == 'New_Account':
        New_Account(callback_query)
    elif callback_query.data == 'get_users':
        scraper_ask(callback_query)
    elif callback_query.data == 'online_user':
        Recv(callback_query)
    elif callback_query.data == 'last_user':
        Recv(callback_query)
    elif callback_query.data == 'get_all':
        Recv(callback_query)
    elif callback_query.data ==  'add_member':
        start(callback_query)
    elif callback_query.data ==  'send_message':
        ask_message(callback_query)
    elif callback_query.data == 'leave_chat':
        leave_chat(callback_query)
    elif callback_query.data == 'join_chat':
        ask_join_chat(callback_query)
        
    

app.run()
