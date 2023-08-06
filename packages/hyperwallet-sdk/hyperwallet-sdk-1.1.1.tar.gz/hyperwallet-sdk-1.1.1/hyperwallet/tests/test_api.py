#!/usr/bin/env python

import mock
import unittest
import hyperwallet

from hyperwallet.exceptions import HyperwalletException


class ApiInitializationTest(unittest.TestCase):

    def test_initialize_fail_need_username(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api()

        self.assertEqual(exc.exception.message, 'username is required')

    def test_initialize_fail_need_password(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api(
                'username'
            )

        self.assertEqual(exc.exception.message, 'password is required')

    def test_initialize_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api(
                'username',
                'password'
            )

        self.assertEqual(exc.exception.message, 'programToken is required')


class ApiTest(unittest.TestCase):

    def setUp(self):

        self.api = hyperwallet.Api(
            'test-user',
            'test-pass',
            'prg-12345'
        )

        self.data = {
            'token': 'tkn-12345'
        }

        self.data_with_type = {
            'token': 'tkn-12345',
            'type': 'BANK_ACCOUNT'
        }

        self.balance = {
            'currency': 'USD'
        }

        self.configuration = {
            'countries': ['US'],
            'currencies': ['USD'],
            'type': 'INDIVIDUAL'
        }

    '''

    Users

    '''

    def test_create_user_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUser()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createUser(self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_user_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_user_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getUser('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_user_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_user_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_user_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateUser('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_users_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listUsers()

        self.assertEqual(response[0].token, self.data.get('token'))

    def test_create_user_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUserStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_user_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUserStatusTransition('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createUserStatusTransition('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_user_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getUserStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_user_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getUserStatusTransition('token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_user_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getUserStatusTransition('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_user_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listUserStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listUserStatusTransitions('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    '''

    Bank Accounts

    '''

    def test_create_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankAccount('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_account_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_account_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_bank_account_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    def test_update_bank_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_account_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateBankAccount('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_accounts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccounts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_accounts_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankAccounts('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_bank_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_account_status_transition_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    def test_create_bank_account_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankAccountStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_account_status_transition_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    def test_get_bank_account_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_account_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankAccountStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_account_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccountStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_bank_account_status_transitions_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccountStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_account_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankAccountStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_bank_account_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_account_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivateBankAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_account_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivateBankAccount('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Bank Cards

    '''

    def test_create_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_card_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCard('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankCard('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCard('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_card_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_bank_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    def test_update_bank_card_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_card_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateBankCard('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_cards_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCards()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_cards_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankCards('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_bank_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    def test_create_bank_card_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_card_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankCardStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    def test_get_bank_card_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_card_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankCardStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_card_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCardStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_bank_card_status_transitions_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCardStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_card_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankCardStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_bank_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankCard('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivateBankCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivateBankCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Prepaid Cards

    '''

    def test_create_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_prepaid_card_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPrepaidCard('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_prepaid_card_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_prepaid_cards_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCards()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_cards_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPrepaidCards('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_prepaid_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_prepaid_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    def test_create_prepaid_card_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPrepaidCardStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_prepaid_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_prepaid_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    def test_get_prepaid_card_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_prepaid_card_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPrepaidCardStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_prepaid_card_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_prepaid_card_status_transitions_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPrepaidCardStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivatePrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivatePrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_suspend_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.suspendPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_suspend_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.suspendPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_suspend_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.suspendPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_suspend_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.suspendPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_unsuspend_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unsuspendPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_unsuspend_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unsuspendPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unsuspend_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.unsuspendPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unsuspend_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.unsuspendPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_lost_or_stolen_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lostOrStolenPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_lost_or_stolen_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lostOrStolenPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lost_or_stolen_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.lostOrStolenPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lost_or_stolen_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.lostOrStolenPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_lock_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lockPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_lock_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lockPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lock_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.lockPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lock_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.lockPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_unlock_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unlockPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_unlock_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unlockPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unlock_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.unlockPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unlock_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.unlockPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Paper Checks

    '''

    def test_create_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_paper_check_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPaperCheck('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_paper_check_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_paper_check_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPaperCheck('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_paper_check_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    def test_update_paper_check_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paper_check_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updatePaperCheck('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_paper_checks_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperChecks()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_checks_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaperChecks('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_paper_check_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_paper_check_status_transition_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    def test_create_paper_check_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPaperCheckStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_paper_check_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheckStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_paper_check_status_transition_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheckStatusTransition('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    def test_get_paper_check_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheckStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_paper_check_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPaperCheckStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_paper_check_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperCheckStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_paper_check_status_transitions_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperCheckStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_check_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaperCheckStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_paper_check_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_paper_check_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivatePaperCheck('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_paper_check_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivatePaperCheck('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Payments

    '''

    def test_create_payment_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayment()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_payment_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPayment(self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_payment_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPayment()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_payment_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPayment('token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payments_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayments()

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_get_payment_status_transition_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaymentStatusTransition()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    def test_get_payment_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaymentStatusTransition('token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_payment_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPaymentStatusTransition('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_payment_status_transitions_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaymentStatusTransitions()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payment_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaymentStatusTransitions('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    '''

    Balances

    '''

    def test_list_user_balances_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_balances_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForUser('token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_prepaid_card_balances_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_prepaid_card_balances_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_balances_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForPrepaidCard('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_account_balances_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_list_account_balances_fail_need_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForAccount('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_balances_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForAccount('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    '''

    Receipts

    '''

    def test_list_user_receipts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_receipts_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForUser('token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_prepaid_card_receipts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_prepaid_card_receipts_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_receipts_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForPrepaidCard('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_account_receipts_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_list_account_receipts_fail_need_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForAccount('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_receipts_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForAccount('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    '''

    Programs

    '''

    def test_get_program_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getProgram()

        self.assertEqual(exc.exception.message, 'programToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_program_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getProgram('token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

    Accounts

    '''

    def test_get_account_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_get_account_fail_need_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getAccount('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_account_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

    Transfer Methods

    '''

    def test_create_transfer_method_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferMethod()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_transfer_method_fail_need_cache_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferMethod('token')

        self.assertEqual(exc.exception.message, 'cacheToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_method_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createTransferMethod('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_method_success_with_type(self, mock_post):

        mock_post.return_value = self.data_with_type
        response = self.api.createTransferMethod('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_transfer_method_configuration_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_transfer_method_configuration_fail_need_country(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token')

        self.assertEqual(exc.exception.message, 'country is required')

    def test_get_transfer_method_configuration_fail_need_currency(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token', 'country')

        self.assertEqual(exc.exception.message, 'currency is required')

    def test_get_transfer_method_configuration_fail_need_type(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token', 'country', 'currency')

        self.assertEqual(exc.exception.message, 'type is required')

    def test_get_transfer_method_configuration_fail_need_profile_type(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token', 'country', 'currency', 'type')

        self.assertEqual(exc.exception.message, 'profileType is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_transfer_method_configuration_success(self, mock_get):

        mock_get.return_value = self.configuration
        response = self.api.getTransferMethodConfiguration('token', 'country', 'currency', 'type', 'token')

        self.assertTrue(response.type, self.configuration.get('type'))

    def test_list_transfer_method_configurations_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferMethodConfigurations()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_method_configurations_success(self, mock_get):

        mock_get.return_value = {'data': [self.configuration]}
        response = self.api.listTransferMethodConfigurations('token')

        self.assertTrue(response[0].type, self.configuration.get('type'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_method_configurations_success_empty(self, mock_get):

        mock_get.return_value = {}
        response = self.api.listTransferMethodConfigurations('token')

        self.assertEqual(response, [])

    '''

    Webhook Notifications

    '''

    def test_get_webhook_fail_need_webhook_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getWebhookNotification()

        self.assertEqual(exc.exception.message, 'webhookToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_webhook_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getWebhookNotification('token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_webhooks_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listWebhookNotifications()

        self.assertTrue(response[0].token, self.data.get('token'))


if __name__ == '__main__':
    unittest.main()
