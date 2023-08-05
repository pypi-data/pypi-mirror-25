import json
import responses
from django.apps import apps
from django.conf import settings
from casepro.cases.models import Case
from casepro.test import BaseCasesTest
from mock import patch
from .plugin import SubscriptionPodConfig, SubscriptionPod


class SubscriptionPodTest(BaseCasesTest):
    def setUp(self):
        super(SubscriptionPodTest, self).setUp()
        self.contact = self.create_contact(self.unicef, 'test_id', "Tester")
        self.msg1 = self.create_message(
            self.unicef, 123, self.contact, "Test message")
        self.case = Case.get_or_open(
            self.unicef, self.user1, self.msg1, "Summary", self.moh)
        self.base_url = 'http://example.com/'

        self.pod = SubscriptionPod(
            apps.get_app_config('family_connect_subscription_pod'),
            SubscriptionPodConfig({
                'index': 23,
                'title': "My subscription Pod",
                'url': "http://example.com/",
                'token': "test_token",
            }))

        self.subscription_data = {
            "url": "http://example.com/api/v1/subscriptions/sub_id/",
            "id": "sub_id",
            "version": 1,
            "identity": "C-002",
            "messageset": 1,
            "next_sequence_number": 1,
            "lang": "eng",
            "active": True,
            "completed": False,
            "schedule": 1,
            "process_status": 0,
            "metadata": None,
            "created_at": "2016-07-22T15:53:42.282902Z",
            "updated_at": "2016-09-06T17:17:54.746390Z"
        }

    def subscription_callback_no_matches(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            'next': None,
            'previous': None,
            'results': []
        }
        return (200, headers, json.dumps(resp))

    def subscription_filter_callback_one_match(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "next": None,
            "previous": None,
            "results": [self.subscription_data]
        }
        return (200, headers, json.dumps(resp))

    def subscription_callback(self, request):
        headers = {'Content-Type': "application/json"}
        resp = self.subscription_data
        return (200, headers, json.dumps(resp))

    def message_set_callback(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "id": 1,
            "short_name": "test_set",
            "content_type": "text",
            "notes": "",
            "next_set": 1,
            "default_schedule": 1,
            "created_at": "2016-07-22T15:52:16.308779Z",
            "updated_at": "2016-07-22T15:52:16.308802Z"
        }
        return (200, headers, json.dumps(resp))

    def schedule_callback(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "id": 1,
            "minute": "0",
            "hour": "8",
            "day_of_week": "1,2",
            "day_of_month": "*",
            "month_of_year": "*"
        }
        return (200, headers, json.dumps(resp))

    def error_callback(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "detail": "Bad Request"
        }
        return (400, headers, json.dumps(resp))

    @responses.activate
    def test_read_data_no_subscriptions(self):
        # Add callback
        responses.add_callback(
            responses.GET,
            self.base_url + 'subscriptions/?identity=' + self.contact.uuid,
            callback=self.subscription_callback_no_matches,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        auth_header = responses.calls[0].request.headers['Authorization']
        self.assertEqual(auth_header, "Token test_token")
        self.assertEqual(result, {"items": [{
            "rows": [{
                "name": "No subscriptions", "value": ""
            }]}]})

    @responses.activate
    def test_read_data_one_subscription(self):
        # Add callbacks
        responses.add_callback(
            responses.GET,
            self.base_url + 'subscriptions/?identity=' + self.contact.uuid,
            callback=self.subscription_filter_callback_one_match,
            match_querystring=True, content_type="application/json")
        responses.add_callback(
            responses.GET, self.base_url + 'messageset/1/',
            callback=self.message_set_callback,
            match_querystring=True, content_type="application/json")
        responses.add_callback(
            responses.GET, self.base_url + 'schedule/1/',
            callback=self.schedule_callback,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        auth_header = responses.calls[0].request.headers['Authorization']
        self.assertEqual(auth_header, "Token test_token")
        # Check items returned
        self.assertEqual(result['items'], [{"rows": [
                {"name": "Message Set", "value": "test_set"},
                {"name": "Next Sequence Number", "value": 1},
                {"name": "Schedule",
                 "value": "At 08:00 every Monday and Tuesday"},
                {"name": "Active", "value": True},
                {"name": "Completed", "value": False},
            ]}])
        # Check actions returned
        self.assertEqual(result['actions'], [{
                'type': 'switch_message_set',
                'name': 'Switch from test_set to test_set',
                'confirm': True,
                'busy_text': 'Processing...',
                'payload': {
                    'new_set_id': 1,
                    'new_set_name': 'test_set',
                    'old_set_name': 'test_set',
                    'subscription_id': 'sub_id'
                }
            }, {
                'type': 'full_opt_out',
                'name': 'Full Opt-Out',
                'confirm': True,
                'busy_text': 'Processing...',
                'payload': {
                    'contact_id': self.contact.id,
                    'subscription_ids': ["sub_id"]
                }
            }, {
                'type': 'cancel_subs',
                'name': 'Cancel All Subscriptions',
                'confirm': True,
                'busy_text': 'Cancelling...',
                'payload': {
                    'subscription_ids': ["sub_id"]
                }
            }])

    @responses.activate
    def test_read_data_error_case(self):
        # Add callback
        responses.add_callback(
            responses.GET,
            self.base_url + 'subscriptions/?identity=' + self.contact.uuid,
            callback=self.error_callback,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        auth_header = responses.calls[0].request.headers['Authorization']
        self.assertEqual(auth_header, "Token test_token")
        self.assertEqual(result, {"items": [
            {"name": "Error", "value": "Bad Request"}
        ]})

    @responses.activate
    def test_cancel_subscriptions_method_success(self):
        # Add callback
        responses.add_callback(
            responses.PATCH, self.base_url + 'subscriptions/sub_id/',
            callback=self.subscription_callback,
            match_querystring=True, content_type="application/json")

        self.assertTrue(self.pod.cancel_subscriptions(['sub_id']))

        request = responses.calls[0].request
        self.assertEqual(request.url, self.base_url + 'subscriptions/sub_id/')
        self.assertEqual(request.body, '{"active": false}')
        self.assertEqual(request.method, 'PATCH')
        self.assertEqual(request.headers['Authorization'], "Token test_token")

    @responses.activate
    def test_cancel_subscriptions_method_fail(self):
        # Add callback
        responses.add_callback(
            responses.PATCH, self.base_url + 'subscriptions/sub_id/',
            callback=self.error_callback,
            match_querystring=True, content_type="application/json")

        self.assertFalse(self.pod.cancel_subscriptions(['sub_id']))

        request = responses.calls[0].request
        self.assertEqual(request.url, self.base_url + 'subscriptions/sub_id/')
        self.assertEqual(request.body, '{"active": false}')
        self.assertEqual(request.method, 'PATCH')
        self.assertEqual(request.headers['Authorization'], "Token test_token")

    def test_cancel_subs_action_success(self):
        with patch.object(
                SubscriptionPod, 'cancel_subscriptions', return_value=True) \
                as mock_method:
            response = self.pod.perform_action(
                'cancel_subs', {'subscription_ids': ['sub_id']})
        mock_method.assert_called_with(['sub_id'])
        self.assertEqual(
            response, (True, {"message": "cancelled all subscriptions"}))

    def test_cancel_subs_action_fail(self):
        with patch.object(
                SubscriptionPod, 'cancel_subscriptions', return_value=False) \
                as mock_method:
            response = self.pod.perform_action(
                'cancel_subs', {'subscription_ids': ['sub_id']})
        mock_method.assert_called_with(['sub_id'])
        self.assertEqual(
            response,
            (False, {"message": "Failed to cancel some subscriptions"}))

    @responses.activate
    def test_opt_out_action_success(self):
        self.contact.urns = ['msisdn:+27345']
        self.contact.save()
        # Add callback
        responses.add(
            responses.POST, settings.IDENTITY_API_ROOT + "api/v1/optout/",
            content_type="application/json",
            status=201)
        with patch.object(
                SubscriptionPod, 'cancel_subscriptions', return_value=True) \
                as mock_method:
            response = self.pod.perform_action(
                'full_opt_out', {'contact_id': self.contact.id,
                                 'subscription_ids': ['sub_id']})
        mock_method.assert_called_with(['sub_id'])
        self.assertEqual(
            response, (True, {
                "message": "Opt-Out completed. All subscriptions cancelled."}))

    @responses.activate
    def test_opt_out_action_no_urn(self):
        self.contact.urns = []
        self.contact.save()
        # Add callback
        responses.add(
            responses.POST, settings.IDENTITY_API_ROOT + "api/v1/optout/",
            content_type="application/json",
            status=201)
        with patch.object(
                SubscriptionPod, 'cancel_subscriptions', return_value=True) \
                as mock_method:
            response = self.pod.perform_action(
                'full_opt_out', {'contact_id': self.contact.id,
                                 'subscription_ids': ['sub_id']})
        mock_method.assert_called_with(['sub_id'])
        self.assertEqual(
            response, (False, {
                "message": "An error occured while opting the user out. "
                "All subscriptions cancelled."}))

    @responses.activate
    def test_opt_out_action_opt_out_fails(self):
        self.contact.urns = ['msisdn:+27345']
        self.contact.save()
        # Add callback
        responses.add(
            responses.POST, settings.IDENTITY_API_ROOT + "api/v1/optout/",
            content_type="application/json",
            status=400)
        with patch.object(
                SubscriptionPod, 'cancel_subscriptions', return_value=True) \
                as mock_method:
            response = self.pod.perform_action(
                'full_opt_out', {'contact_id': self.contact.id,
                                 'subscription_ids': ['sub_id']})
        mock_method.assert_called_with(['sub_id'])
        self.assertEqual(
            response, (False, {
                "message": "An error occured while opting the user out. "
                "All subscriptions cancelled."}))

    @responses.activate
    def test_opt_out_action_cancel_sub_fails(self):
        self.contact.urns = ['msisdn:+27345']
        self.contact.save()
        # Add callback
        responses.add(
            responses.POST, settings.IDENTITY_API_ROOT + "api/v1/optout/",
            content_type="application/json",
            status=201)
        with patch.object(
                SubscriptionPod, 'cancel_subscriptions', return_value=False) \
                as mock_method:
            response = self.pod.perform_action(
                'full_opt_out', {'contact_id': self.contact.id,
                                 'subscription_ids': ['sub_id']})
        mock_method.assert_called_with(['sub_id'])
        self.assertEqual(
            response, (False, {
                "message":
                "Opt-Out completed. Failed to cancel some subscriptions."}))

    @responses.activate
    def test_opt_out_action_all_fails(self):
        self.contact.urns = ['msisdn:+27345']
        self.contact.save()
        # Add callback
        responses.add(
            responses.POST, settings.IDENTITY_API_ROOT + "api/v1/optout/",
            content_type="application/json",
            status=400)
        with patch.object(
                SubscriptionPod, 'cancel_subscriptions', return_value=False) \
                as mock_method:
            response = self.pod.perform_action(
                'full_opt_out', {'contact_id': self.contact.id,
                                 'subscription_ids': ['sub_id']})
        mock_method.assert_called_with(['sub_id'])
        self.assertEqual(
            response, (False, {
                "message":
                "An error occured while opting the user out. "
                "Failed to cancel some subscriptions."}))

    @responses.activate
    def test_activate_message_set(self):
        # Add callback
        responses.add_callback(
            responses.GET, self.base_url + 'messageset/1/',
            callback=self.message_set_callback,
            match_querystring=True, content_type="application/json")
        responses.add_callback(
            responses.GET, self.base_url + 'subscriptions/sub_id/',
            callback=self.subscription_callback,
            match_querystring=True, content_type="application/json")
        responses.add(
            responses.POST, self.base_url + 'subscriptions/',
            content_type="application/json",
            status=201)

        self.assertTrue(self.pod.activate_message_set('sub_id', 1))

        request = responses.calls[2].request
        self.assertEqual(request.url, self.base_url + 'subscriptions/')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.headers['Authorization'], "Token test_token")
        self.assertEqual(json.loads(request.body), {
            'identity': "C-002",
            'lang': "eng",
            'messageset': 1,
            'schedule': 1
        })

    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "cancel_subscriptions", return_value=True)
    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "activate_message_set", return_value=True)
    def test_switch_action_success(self, mock_activate, mock_cancel):
        response = self.pod.perform_action(
            'switch_message_set',
            {'new_set_id': 1,
                'new_set_name': "test_set2",
                'old_set_name': "test_set1",
                'subscription_id': "sub_id"})
        mock_cancel.assert_called_with(['sub_id'])
        mock_activate.assert_called_with('sub_id', 1)
        self.assertEqual(
            response, (True, {
                "message": "switched from test_set1 to test_set2."}))

    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "cancel_subscriptions", return_value=False)
    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "activate_message_set", return_value=False)
    def test_switch_action_fail(self, mock_activate, mock_cancel):
        response = self.pod.perform_action(
            'switch_message_set',
            {'new_set_id': 1,
                'new_set_name': "test_set2",
                'old_set_name': "test_set1",
                'subscription_id': "sub_id"})
        mock_cancel.assert_called_with(['sub_id'])
        mock_activate.assert_called_with('sub_id', 1)
        self.assertEqual(
            response, (False, {
                "message": "Failed to switch message sets."}))

    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "cancel_subscriptions", return_value=False)
    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "activate_message_set", return_value=True)
    def test_switch_action_cancel_sub_fail(self, mock_activate, mock_cancel):
        response = self.pod.perform_action(
            'switch_message_set',
            {'new_set_id': 1,
                'new_set_name': "test_set2",
                'old_set_name': "test_set1",
                'subscription_id': "sub_id"})
        mock_cancel.assert_called_with(['sub_id'])
        mock_activate.assert_called_with('sub_id', 1)
        self.assertEqual(
            response, (False, {
                "message": "An error occured removing the old subscription. "
                           "The user is subscribed to both sets"}))

    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "cancel_subscriptions", return_value=True)
    @patch("casepropods.family_connect_subscription.plugin.SubscriptionPod."
           "activate_message_set", return_value=False)
    def test_switch_action_activate_new_fail(self, mock_activate, mock_cancel):
        response = self.pod.perform_action(
            'switch_message_set',
            {'new_set_id': 1,
                'new_set_name': "test_set2",
                'old_set_name': "test_set1",
                'subscription_id': "sub_id"})
        mock_cancel.assert_called_with(['sub_id'])
        mock_activate.assert_called_with('sub_id', 1)
        self.assertEqual(
            response, (False, {
                "message": "An error occured creating the new subscription. "
                           "The user has been unsubscribed."}))
