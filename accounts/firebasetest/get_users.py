import argparse
from typing import Optional

from firebase_admin import auth
from firebase_admin.auth import UserRecord

from initialise_firebase_admin import app



page = auth.list_users()
while page:
    for user in page.users:
        print('User: ' + user.uid)
    page = page.get_next_page()

for user in auth.list_users().iterate_all():
    print('User: ' + user.uid)

