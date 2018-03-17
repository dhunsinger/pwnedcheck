# pwnedcheck

This python script utilizes Troy Hunt's Haveibeenpwned service to 
either check the first five characters of a SHA-1 encrypted password
against a list of over a half billion known compromised passwords,
while ONLY sending the bare minuimum information to the service to
generate a _(potential)_ positive or _(definite)_ negative result OR whether
an email address has been included in listed breaches. You can read more about 
the API/service here: 

https://haveibeenpwned.com/API/v2#PwnedPasswords

Detail about the working theory for checking passwords is on Troy Hunt's blog:

https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/

The script stores your email address or password in local memory so no sensitive information is ever transferred over the wire. Once the script completes, the memory structures are destroyed.

WARNING/DISCLAIMER:

IF YOU'RE NOT COMFORTABLE THAT THE hveibeenpwned.com SITE IS SAFE THEN 
DON'T RUN THE SCRIPT! 
Troy Hunt, the site operator, is a Microsoft Regional Director and Microsoft 
Most Valuable Professional for Developer Security. If he's trying to collect 
email addresses or the first five characters of SHA-1 passwords on the service
to do *bad things* we're all pretty well screwed, 

BUT USE AT YOUR OWN RISK.

This script was written for Python v3. Run with:
```
python3 pwnedcheck.py
```
I welcome comments, code improvements or collaboration. Enjoy! 
