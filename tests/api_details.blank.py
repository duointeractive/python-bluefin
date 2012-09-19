"""
The following credentials are used to run the unit tests. Please copy this
file to api_details.py and modify the values to fit your account.
"""
API_DETAILS = {
    # You can get this from your account dashboard on secure.bluefingateway.com.
    'account_id': 123456789012,
    # Under Setup -> Account Security.
    'dynip_sec_code': 'YOUR_CODE_HERE',
    # For dataretrieval tests, navigate to your Site Tags setup and pick the
    # auth code out.
    'site_tag_auth_code': 'YOUR_AUTH_CODE_HERE'
}

# Make sure you enter your test credit card here. Under Setup -> Credit Cards.
TEST_CARD = {
    'card_number': 4444333322221111,
    'card_expire': '1212',
}

# An invalid card number that doesn't match your test card number.
INVALID_CARD_NUM = 4012888888881881
# This has to not equal your test card number in order for it to fail.
assert INVALID_CARD_NUM != TEST_CARD['card_number']