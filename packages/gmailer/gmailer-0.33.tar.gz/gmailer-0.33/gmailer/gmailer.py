#!/usr/bin/env python
import os
from gmail import gmail
from gmail import message
import sys
import vmtools

vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
import pkgutil
local_settings_present = pkgutil.find_loader('local_settings')
if local_settings_present:
    from local_settings import *

def senderror(subject_text, body_text, username, password, recipients, attachment_files_path=None):
    """Take subject_text, body_text, username, password, recipients, and optionally attachment_files_path, send email
    
    :type subject_text: string
    :param subject_text: the subject for the email
    :type body_text: string
    :param body_text: the body for the email
    :type username: string
    :param username: the gmail username
    :type password: string
    :param password: the gmail password
    :type recipients: list
    :param recpients: list of recipients
    :type attachment_files_path: list
    :param attachment_files_path: list of strings that are absolute file paths to the files to attach
    """

    gmailconn = gmail.GMail(username=username, password=password)
    if isinstance(recipients, list):
        recipients_string = ', '.join(recipients)
    else:
        error_message = 'Error: the argument "recipients" was found to be a {}. It must be a list! '.format(type(recipients))
        print(error_message)

    if attachment_files_path:
        msg = message.Message(subject=subject_text, to=recipients_string, text=body_text, attachments=attachment_files_path)
    else:
        msg = message.Message(subject=subject_text, to=recipients_string, text=body_text)

    gmailconn.send(msg)
    gmailconn.close()

def senderror_simple(subject_text, body_text):
    """Take subject_text and body_text and send with mail account
    NB: this function requires thatf you store in local_settings.py at the root of the python virtual machine the following (you can avoid specifying the arguments: username, password, recipients):
    import os
    #mail settings
    MAIL_CONFIG_DICT = {
        MAIL_USER='you@yourdomain.com'
        MAIL_PASS='changeme'
        MAIL_RECIPIENTS=['friend1@theirdomain.com', 'friend2@theirdoman.com']
        }
    
    :type subject_text: string
    :param subject_text: the subject for the email
    :type body_text: string
    :param body_text: the body for the email
    """
    senderror(subject_text, body_text, username=MAIL_CONFIG_DICT['MAIL_USER'], password=MAIL_CONFIG_DICT['MAIL_PASS'], recipients=MAIL_CONFIG_DICT['MAIL_RECIPIENTS'])

