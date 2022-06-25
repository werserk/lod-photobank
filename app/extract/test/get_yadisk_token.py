import sys
import yadisk

y = yadisk.YaDisk("<app-id>", "<app-password>")
url = y.get_code_url()

print("Go to the following url: %s" % url)
code = input("Enter the confirmation code: ")

try:
    response = y.get_token(code)
    print(response)
except yadisk.exceptions.BadRequestError:
    print("Bad code")
    sys.exit(1)

y.token = response.access_token

if y.check_token():
    print("Sucessfully received token!")
else:
    print("Something went wrong. Not sure how though...")