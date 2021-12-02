# -*- coding: utf-8 -*-
"""
__version__ = 0.4
"""
    
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None
from math import floor
import streamlit as st
from pyairtable import Table
from datetime import datetime
import time

def main():
    
    def airtable2df(airtable):
        ls_wallet = []
        ls_email = []
        ls_launchpad = []
        ls_recordid = []
        
        for json in airtable.all():
            ls_wallet.append(json['fields']['wallet'])
            ls_email.append(json['fields']['email'])
            ls_launchpad.append(json['fields']['launchpad'])
            ls_recordid.append(json['fields']['record_id'])
        
        return pd.DataFrame({'wallet': ls_wallet, 
                             'email': ls_email,
                             'launchpad': ls_launchpad,
                             'record_id': ls_recordid
                            })
    
    st.set_page_config(page_title='$MNFT IDO Launchpads', page_icon=':gear:')

    airtable_key = 'keyxL5TZmSO03vyVf'
    base_table_id = 'appVE9ersJpiL6STN'
    table_name = 'Verified'

    st.title(':gear:ManuFactory - $MNFT IDO') 
    st.header('Launchpad Selection\n')
    
    st.subheader('Current Inscriptions')
    
    verified_table = Table(airtable_key, base_table_id, table_name)
    verified_df = airtable2df(verified_table)
    verified_df['wallet'] = verified_df['wallet'].str.lower()
    verified_df['email'] = verified_df['email'].str.lower()

    oxbull_no = (verified_df['launchpad'] == 'Oxbull').sum()
    nearpad_no = (verified_df['launchpad'] == 'NearPad').sum()
    nftpad_no = (verified_df['launchpad'] == 'NFTPad').sum()
    trustpad_no = (verified_df['launchpad'] == 'TrustPad').sum()

    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Oxbull", "{}".format(oxbull_no))
    col2.metric("NearPad", "{}".format(nearpad_no))
    col3.metric("NFTPad", "{}".format(nftpad_no))
    col4.metric("TrustPad", "{}".format(trustpad_no))
    
    st.subheader('Select your IDO Launchpad')

    wallet = ''
    wallet = st.text_input('Type in your Wallet Address with which you donated:')
    wallet = wallet.lower()

    if wallet in verified_df['wallet'].values:
        st.subheader('Status: Verified This wallet address is in the whitelist.')

        record_id = verified_df[verified_df.wallet == wallet]['record_id'].values[0]
        email_id = verified_df[verified_df.wallet == wallet]['email'].values[0]

        email = ''
        email = st.text_input('Type in your Email Address (which you used to fill in the form):', type='password')
        email = email.lower()

        if email == email_id:
            st.subheader('Status: Verified Your email and wallet information match correctly.')
            st.write('\n')

            launchpad = verified_df[verified_df.wallet == wallet].launchpad.values[0]
            
            if launchpad != email:
                st.subheader('Your current launchpad is: {}'.format(launchpad))

                st.write('Note: once information/tutorials on how to use each launchpad is posted on our social media channels, we will enable the ability to switch launchpads at will.')

            else:
                st.subheader('You are currently not registered in any launchpad, choose one below:')
                
                option = ''
                option = st.selectbox('Choose your Launchpad',
                                     ['Oxbull', 'NearPad', 'NFTPad', 'TrustPad'])

                if option in ['Oxbull', 'NearPad', 'NFTPad', 'TrustPad']:
                    try:
                        verified_table.update(record_id, {'launchpad': option})
                        st.write('Success! You have registered on:  {}'.format(option))
                    except:
                        st.write('We are sorry, the servers are currently busy from traffic, please try again in a few minutes.)')
                        st.write('If it still does not work, please open a ticket in the #Reports channel of the Discord, and we will help you.')
                elif option == '':
                    st.write('Select an option from the Dropdown menu.')

        elif email == '':
            st.write('Remember to press enter after inputting your email.')

        else:

            st.subheader('Error: the wallet-email address combination is incorrect.')
            st.write('Please try again making sure to input the email you associated with your wallet when you filled in the form.')
            st.write('If you need help/forgot which email you used, please open a ticket in the #Reports channel in the Discord, and we will help you.')
    
    elif wallet == '':
        st.write('Remember to press enter after inputting your wallet.')

    else:

        st.subheader('Error: the wallet address submitted is not in the whitelist.')
        st.write('Please try again, making sure to input the correct whitelisted wallet, which you can find in the whitelist document.')
        st.write('If you need help, please open a ticket in the #Reports channel in the Discord, and we will help you.')          
                    
     
if __name__ == '__main__':
    main()



    
    




