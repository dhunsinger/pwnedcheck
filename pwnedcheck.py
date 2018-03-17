import hashlib
import urllib.request as req, urllib.parse, urllib.error
import ssl
import getpass
import time
import re
import json
import textwrap

# function courtesy of
# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

# Ignore SSL certificate errors
def do_ssl():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return(ctx)

text = '''
This progam checks over a half billion compromised email accounts and passwords
It DOES NOT send your password to the password database but does send the first
five characters of a SHA-1 encrypted string representing the password via ssl
encrytion, or it passes the email address via SSL encryption.

NEVER enter your password for checking on ANY WEBSITE. This service uses
an API from haveibeenpwned.com - IF YOU DO NOT TRUST THE SERVICE, DO NOT USE
THIS PROGRAM. Hit Ctrl+c to quit now. haveibeenpwned is an offering from
Troy Hunt, Microsoft Regional Director and MVP and a respected security
authority. The UK and  Austrailian governments trust the service for monitoring
their own domains, BUT IF YOU DO NOT TRUST TROY OR THE SERVICE,
DO NOT USE THIS PROGRAM.

You may search by password or by breached email address, by entering
either 1 or 2.

1) Check password for breach.
2) Check email address for breach.
'''
print(text)
time.sleep(1)
choice = input('Enter 1 or 2: ')

for val in choice:
    if val in ['1', '2']:
        break
    else:
        print('Enter only 1 or 2. Quitting.')
        quit()

if choice == '1':
    print('To see a sample positive response, enter the password \'password\'')
    time.sleep(2)
    pass1 = getpass.getpass('Enter password: ')
    if  not pass1:
        print('No password entered.')
        quit()
    pass2 = getpass.getpass('Enter again: ')
    if  not pass2:
        print('No password entered. Quitting.')
        quit()
    if pass1 == pass2:
        print('Passwords match - continuing...')
    pass1 = pass1.encode('utf-8')
    pass1 = hashlib.sha1(pass1)
    pass1 = (pass1.hexdigest())
    pass1 = pass1[:5]
    url = "https://api.pwnedpasswords.com/pwnedpassword/" + pass1
    print('Retrieving results...')
    time.sleep(3)
    headers = {}
    headers['User-Agent'] = "git@github.com:dhunsinger/pwnedcheck.git"
    req = urllib.request.Request(url, headers = headers)
    # print(req)
    try:
        resp = urllib.request.urlopen(req, context=do_ssl())
        # print(resp)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print('Password not found in database.')
            quit()
    respData = resp.read()
    respData = respData.decode()
    print('The password entered appeared', respData, 'times in the database.')
    print('Your password may be compromised!')
if choice == '2':
    email = input('Enter email address: ')
    addressToVerify = email
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    if match == None:
    	print('Not a valid email address. Quitting.')
    	quit()
    url = 'https://haveibeenpwned.com/api/v2/breachedaccount/' + email
    # print(url)
    headers = {}
    headers['User-Agent'] = "pwnedcheck.py"
    req = urllib.request.Request(url, headers = headers)
    # print(req)
    try:
        resp = urllib.request.urlopen(req, context=do_ssl())
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print('Email address not found in any breaches. Phew.')
            quit()
    resp = resp.read()
    resp = resp.decode()
    resp = json.loads(resp)
    print('')
    count = 0
    for i in resp:
        count += 1
    print('BUMMER - Email address is included in', count, 'breach(es):')
    for d in resp:
        print('===============================================================')
        print('Name of breach:', d['Name'])
        print('Description:', textwrap.fill(remove_html_markup(d['Description']), 60))
        print('===============================================================')
