#!/usr/bin/env python

import socket
import sys
import struct
import sqlite3

from binascii import hexlify
from time import sleep

from bpc8583.ISO8583 import ISO8583, MemDump, ParseError
from bpc8583.spec import IsoSpec, IsoSpec1987BPC
from bpc8583.tools import get_response, get_stan, get_datetime_with_year

from tracetools.tracetools import trace
from pynblock.tools import B2raw

from pybank.db import Database

class CBS:
    def __init__(self, host=None, port=None):
        self.host = host if host else '127.0.0.1'

        if port:
            try:
                self.port = int(port)
            except ValueError:
                print('Invalid TCP port: {}'.format(arg))
                sys.exit()
        else:
            self.port = 3388

        self.db = Database('cbs.db')
        self.responses = {'Approval': '000', 'Invalid Amount': '903', 'Invalid account number': '914', 'Insufficient funds': '915', }


    def get_message_length(self, message):
        return B2raw(bytes(str(len(message)).zfill(4), 'utf-8'))


    def build_tlv_tag(self, tag, value):
        return str(tag).zfill(3) + str(len(value)).zfill(3) + str(value)


    def get_balance_string(self, balance, currency_code):
        """
        Get balance string, according to Field 54 description
        """
        if not balance or not currency_code:
            return ''
    
        amount_sign = 'C' if balance > 0 else 'D'
    
        balance_formatted = '{0:.2f}'.format(balance).replace(' ', '').replace('.', '').replace('-', '').zfill(12)
        balance_string = amount_sign + balance_formatted + currency_code
    
        return '007' + str(len(balance_string)).zfill(3) + balance_string


    def get_float_amount(self, amount, currency):
        """
        TODO: check currency exponent, currently using 2 by default
        """
        return amount / 100.0 if amount else .0


    def connect(self):
        """
        """
        try:
            self.sock = None
            for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                self.sock = socket.socket(af, socktype, proto)
                self.sock.connect(sa)
        except OSError as msg:
            print('Error connecting to {}:{} - {}'.format(self.host, self.port, msg))
            sys.exit()
        print('Connected to {}:{}'.format(self.host, self.port))


    def process_trxn_balance_inquiry(self, request, response):
        card_number = request.FieldData(2)
        currency_code = request.FieldData(51)
        if not currency_code:
            currency_code = request.FieldData(49)

        available_balance = self.db.get_card_balance(card_number, currency_code)

        response.FieldData(54, self.get_balance_string(available_balance, currency_code))
        response.FieldData(39, self.responses['Approval'])


    def get_transaction_type_mnemonic(self, prcode):
        trxn_type = prcode[0:2]

        if trxn_type == '00':
            return 'PRC'
        elif trxn_type == '01':
            return 'WDL'
        else:
            return 'OTH'


    def get_field62_data(self, trxn_data):
        """
        """
        field_data = ''
        print_data = '\tStatement data:\n'

        for record in trxn_data:
            # Date
            # '2017-09-20 15:12:40.617' -> '170920'
            date = record[4].split(' ')[0].split('-')
            field_data += date[0][2:4] + date[1] + date[2]
            print_data += record[4] + '\t'

            # Transaction type
            field_data += self.get_transaction_type_mnemonic(record[2])
            print_data += self.get_transaction_type_mnemonic(record[2]) + '\t'

            # Debit/Credit flag
            field_data += record[0]
            print_data += record[0] + ' '

            # Amount
            amount = str(record[1]).zfill(12)
            field_data += amount
            print_data += amount + '\n'

            # Dummy Fee
            fee_amount = '000000000000'
            field_data += fee_amount

        print(print_data)
        return field_data

    def process_cardholder_name_inquiry(self, request, response):
        """
        """
        card_number = request.FieldData(2)
        cardholder_name = self.db.get_cardholder_name(card_number)
        response.FieldData(48, self.build_tlv_tag(29, cardholder_name))
        response.FieldData(39, self.responses['Approval'])


    def process_statement_request(self, request, response):
        """
        """
        card_number = request.FieldData(2)

        trxns = self.db.get_last_transactions(card_number, 10)

        response.FieldData(39, self.responses['Approval'])
        response.FieldData(48, None)
        response.FieldData(62, self.get_field62_data(trxns))


    def save_transaction(self, request, flag='D'):
        """
        """
        MTI = str(request.get_MTI()).zfill(4)[-3:]
        card_number = request.FieldData(2)
        billing_currency_code = request.FieldData(51)
        amount_cardholder_billing = self.get_float_amount(request.FieldData(6), billing_currency_code)
        prcode = str(request.FieldData(3)).zfill(6)
        STAN = request.FieldData(11)
        RRN = request.FieldData(37)
        Field48 = request.FieldData(48)

        if amount_cardholder_billing:
            self.db.insert_transaction_record(mti=MTI, card=card_number, currency=billing_currency_code, amount=amount_cardholder_billing, flag=flag, prcode=prcode, STAN=STAN, RRN=RRN, Field48=Field48);


    def process_trxn_debit_account(self, request, response):
        """
        """
        card_number = request.FieldData(2)
        transaction_currency_code = request.FieldData(49)
        billing_currency_code = request.FieldData(51)
        amount_cardholder_billing = self.get_float_amount(request.FieldData(6), billing_currency_code)

        available_balance = self.db.get_card_balance(card_number, billing_currency_code)

        print('Trying to debit customer. Card [{}], currency [{}], balance before[{}]\n'.format(card_number, billing_currency_code, available_balance));

        if available_balance:

            if transaction_currency_code == billing_currency_code and not amount_cardholder_billing:
                amount_cardholder_billing = self.get_float_amount(request.FieldData(4), billing_currency_code)

            if amount_cardholder_billing:
                if available_balance > amount_cardholder_billing:
                    self.db.update_card_balance(card_number, billing_currency_code, available_balance - amount_cardholder_billing)

                    response.FieldData(39, self.responses['Approval'])
    
                    available_balance = self.db.get_card_balance(card_number, billing_currency_code)
                    response.FieldData(54, self.get_balance_string(available_balance, billing_currency_code))
                    print('Debited succesfully');
                    self.save_transaction(request, 'D')

                else:
                    response.FieldData(39, self.responses['Insufficient funds'])
                    response.FieldData(54, self.get_balance_string(available_balance, billing_currency_code))
                    print('Debit failed: insufficient funds');
            else:
                response.FieldData(39, self.responses['Invalid Amount'])
                print('Invalid Cardholder billing amount')
        else:
            response.FieldData(39, self.responses['Invalid account number'])
            print('Invalid account number')


    def settle_auth_advice(self, request, response):
        """
        """
        card_number = request.FieldData(2)
        currency_code = request.FieldData(51)
        amount_cardholder_billing = self.get_float_amount(request.FieldData(6), currency_code)

        available_balance = self.db.get_card_balance(card_number, currency_code)
        self.db.update_card_balance(card_number, currency_code, available_balance - amount_cardholder_billing)
        self.save_transaction(request, 'D')

        response.FieldData(39, self.responses['Approval'])


    def settle_reversal(self, request, response):
        """
        """
        card_number = request.FieldData(2)
        currency_code = request.FieldData(51)
        amount_cardholder_billing = self.get_float_amount(request.FieldData(6), currency_code)

        available_balance = self.db.get_card_balance(card_number, currency_code)
        self.db.update_card_balance(card_number, currency_code, available_balance + amount_cardholder_billing)
        self.save_transaction(request, 'C')
        response.FieldData(39, self.responses['Approval'])


    def init_response_message(self, request):
        """
        """
        response = ISO8583(None, IsoSpec1987BPC())
        response.MTI(get_response(request.get_MTI()))

        # Copy some key fields from original message:
        for field in [2, 3, 4, 5, 6, 11, 12, 14, 15, 17, 24, 32, 37, 48, 49, 50, 51, 102]:
            response.FieldData(field, request.FieldData(field))

        # Copy Amount, cardholder billing -> Amount, settlement
        response.FieldData(5, request.FieldData(6))

        # Copy Currency code, cardholder billing -> Currency code, settlement
        response.FieldData(50, request.FieldData(51))

        return response


    def get_transaction_type(self, request):
        """
        """
        if request.FieldData(3) != None:
            processing_code = str(request.FieldData(3)).zfill(6)
            return processing_code[0:2]
        else:
            return None


    def send_logon_handshake(self):
        """
        """
        while True:
            request = ISO8583(None, IsoSpec1987BPC())
    
            request.MTI('1804')
            request.FieldData(11, get_stan())
            request.FieldData(12, get_datetime_with_year())
            request.FieldData(24, 801)
    
            request.Print()
            data = request.BuildIso()
            data = self.get_message_length(data) + data
            self.send(data)
    
            data = self.recv()
            response = ISO8583(data, IsoSpec1987BPC())
            response.Print()
    
            if response.get_MTI() != '1814' or response.FieldData(24) != 801 or response.FieldData(39) != '000':
                print('\tLogon failed')
                sleep(5)
            else:
                break


    def recv(self):
        """
        """
        data = self.sock.recv(4096)
        if len(data) > 0:
            trace(title='<< {} bytes received: '.format(len(data)), data=data)
            return data[2:]
        else:
            return None


    def send(self, data):
        """
        """
        self.sock.send(data)
        trace(title='>> {} bytes sent:'.format(len(data)), data=data)


    def run(self):
        """
        """
        while True:
            try:
                self.connect()
                self.send_logon_handshake()

                while True:
                    data = self.recv() 
                    if not data:
                        raise ParseError

                    request = ISO8583(data, IsoSpec1987BPC())
                    request.Print()

                    response = self.init_response_message(request)

                    MTI = str(request.get_MTI()).zfill(4)[-3:]
                    trxn_type = self.get_transaction_type(request)
                    card_number = request.FieldData(2)
                    currency_code = request.FieldData(51)

                    if MTI in ['100', '200']:
                        # Authorization request or financial request
                        if not self.db.card_exists(card_number):
                            # TODO: command line option to add cards autmatically
                            print('\nWARNING: Card {} does not exist!\n'.format(card_number));
                            self.db.insert_card_record(card_number, currency_code, 0);

                        if trxn_type == '31':
                            # Balance
                            self.process_trxn_balance_inquiry(request, response)
                        elif trxn_type in ['00', '01', '50']:
                            # Purchase or ATM Cash
                            self.process_trxn_debit_account(request, response)
                        elif trxn_type == '39':
                            # Ministatement
                            self.process_statement_request(request, response)
                        elif trxn_type == '88':
                            # Cardholder name inquiry
                            self.process_cardholder_name_inquiry(request, response)
                        else:
                            print('Unsupported transaction type {}. Responding APPROVAL by default'.format(trxn_type))
                            response.FieldData(39, self.responses['Approval'])

                    elif MTI in ['120']:
                        # Authorization advice
                        if trxn_type in ['00', '01']:
                            # Purchase or ATM Cash
                            self.settle_auth_advice(request, response)
                        else:
                            response.FieldData(39, self.responses['Approval'])

                    elif MTI in ['400', '420']:
                        # Reversal
                        if trxn_type in ['00', '01']:
                            # Purchase or ATM Cash
                            self.settle_reversal(request, response)

                    response.Print()
                    
                    data = response.BuildIso()
                    data = self.get_message_length(data) + data
                    self.send(data)
        
            except ParseError:
                print('Connection closed')
                conn.close()

        self.sock.close()
        conn.close()
