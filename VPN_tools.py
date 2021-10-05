#Uso:
# rasdial entryname [username [password|*]] [/domain:<domain>] [/phone:<phonenumber>] 
#                   [/callback:<callbacknumber>] [/phonebook:<phonebookfile>] [/PrefixSuffix]
# EntryName
#   Required when connecting to a phonebook (.pbk) entry. Specifies an entry in the current .pbk file, 
#   located in the systemroot\System32\Ras folder. If the ConnectionName contains spaces or special 
#   characters, use quotation marks around the text (that is, "Connection Name").
#   The Rasphone.pbk file is used unless the Personal Phonebook option is selected. If the Personal Phonebook 
#   option is selected, the file UserName.pbk is used. The name is shown on the Rasphone title bar when Personal 
#   Phonebook/p is selected. Numbers are appended if name conflicts occur.
# UserName[{ Password| *}]
#    Specifies a user name and password with which to connect. If an asterisk is used, the user is prompted 
#    for the password, but the characters typed do not display.
# /domain: Domain
#    Specifies the domain in which the user account is located. If unspecified, the last value of the Domain field 
#    in the Connect To dialog box is used.
# /phone: PhoneNumber
#   Substitutes the specified phone number for the entry's phone number in Rasphone.pbk.
# /callback: CallbackNumber
#    Substitutes the specified callback number for the entry's callback number in Rasphone.pbk.
# /phonebook: PhonebookPath
#    Specifies the path to the phonebook file. The default is systemroot\System32\Ras\UserName.pbk. You can specify 
#    a full path to the file.
# /prefixsuffix
#    Applies the current TAPI location dialing settings to the phone number. These settings are configured in Telephony,
#     which is located in Control Panel. This option is turned off by default.
#  /disconnect
#     Required when disconnecting. Disconnects the specified entry. You can also disconnect by typing /d.
import os

log_output=''

def Rasdial():
    try:
        os.system("rasdial [vpn_name] [username] [password]")
        log_ouput='VPN rised up'
    except:
        log_ouput='error rasdial command'
    return log_output