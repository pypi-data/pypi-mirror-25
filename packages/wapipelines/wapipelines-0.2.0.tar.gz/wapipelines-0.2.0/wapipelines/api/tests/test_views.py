import responses
import json
from uuid import UUID

from django.shortcuts import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from wapipelines.models import Pipeline, PipelineRun, Step

from mock import patch

ARTEFACT1 = 'artefact-1'


class PipelineAPITestCase(APITestCase):

    DEFAULT_USERNAME = 'username'

    def setUp(self):
        self.user = self.get_user(
            username='view-username', password='password')
        self.user.is_superuser = True
        self.user.save()

        self.pipeline = Pipeline.objects.create(
            user=self.user,
            name='test pipeline')

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

    def get_user(self, username=None, email_address='user@example.org',
                 password=None):
        user, _ = User.objects.get_or_create(
            username=(username or self.DEFAULT_USERNAME), email=email_address)
        if password:
            user.set_password(password)
        user.save()
        Token.objects.update_or_create(user=user, defaults={})
        return user

    @responses.activate
    def test_run_pipeline_bad_request(self):
        response = self.client.post(reverse('api:pipeline-run', kwargs={
            'uuid': self.pipeline.uuid,
        }))
        self.assertEqual(response.json(), {
            "payload": ["This field is required."],
            "inputs": ["This field is required."],
        })

    @responses.activate
    @patch('wapipelines.tasks.run_step_task')
    def test_run_pipeline_good_request(self, mocked_task):
        step = self.pipeline.step_set.create(
            name='step1', url='http://example.org/',
            inputs=Step.EMPTY_INPUTS,
            outputs=[ARTEFACT1])

        response = self.client.post(reverse('api:pipeline-run', kwargs={
            'uuid': self.pipeline.uuid,
        }), data=json.dumps({
            'payload': {'foo': 'bar'},
            'inputs': {},
        }), content_type='application/json')
        data = response.json()
        self.assertEqual(list(data.keys()), ['run'])
        self.assertTrue(UUID(data['run']))
        run = PipelineRun.objects.get(uuid=data['run'])
        mocked_task.delay.assert_called_with(
            run.pk, step.pk, {'foo': 'bar'}, {})

    @responses.activate
    @patch('wapipelines.tasks.run_step_task')
    def test_run_pipeline_good_direct(self, mocked_task):
        step = self.pipeline.step_set.create(
            name='step1', url='http://example.org/',
            inputs=Step.EMPTY_INPUTS,
            outputs=[ARTEFACT1])

        response = self.client.post(
            reverse('api:pipeline-direct', kwargs={
                'uuid': self.pipeline.uuid,
            }),
            data=json.dumps({'foo': 'bar'}),
            content_type='application/json')
        data = response.json()
        self.assertEqual(list(data.keys()), ['run'])
        self.assertTrue(UUID(data['run']))
        run = PipelineRun.objects.get(uuid=data['run'])
        mocked_task.delay.assert_called_with(
            run.pk, step.pk, {'foo': 'bar'}, {})

    @responses.activate
    def test_run_pipeline_good_request_bad_inputs(self):
        self.pipeline.step_set.create(
            name='step1', url='http://example.org/',
            inputs=[ARTEFACT1],
            outputs=[])

        response = self.client.post(reverse('api:pipeline-run', kwargs={
            'uuid': self.pipeline.uuid,
        }), data=json.dumps({
            'payload': {'foo': 'bar'},
            'inputs': {},
        }), content_type='application/json')
        self.assertEqual(response.json(), {
            'inputs': ['No suitable inputs given'],
        })

    @responses.activate
    @patch('wapipelines.tasks.run_step_task')
    def test_run_pipeline_bad_direct(self, mocked_task):
        self.pipeline.step_set.create(
            name='step1', url='http://example.org/',
            inputs=[ARTEFACT1],
            outputs=Step.EMPTY_OUTPUTS)

        response = self.client.post(
            reverse('api:pipeline-direct', kwargs={
                'uuid': self.pipeline.uuid,
            }),
            data=json.dumps({'foo': 'bar'}),
            content_type='application/json')
        self.assertEqual(response.json(), {
            'inputs': ['This pipeline requires inputs.'],
        })
