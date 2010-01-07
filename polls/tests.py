from django.test import TestCase
from django.test.client import Client

class PollTest(TestCase):

    fixtures = ['test_polls.json']

    def setUp(self):
        self.c = Client()

    def test_poll_list(self):
        response = self.c.get('/polls/')
        self.assertEqual(response.status_code, 200)
        polls = response.context['latest_poll_list']
        self.assertEqual(len(polls), 2)

    def test_poll_detail(self):
        response = self.c.get('/polls/1/')
        self.assertEqual(response.status_code, 200)
        poll = response.context['poll']
        self.assertEqual(len(poll.choice_set.all()), 3)

    def test_poll_vote_get(self):
        response = self.c.get('/polls/1/vote/')
        self.assertContains(response, "You did not select a choice")

    def test_poll_vote(self):
        response = self.c.post('/polls/1/vote/', data = {'choice': 1}, follow = True)
        self.assertRedirects(response, '/polls/1/results/')
        poll = response.context['poll']
        self.assertEqual(poll.id, 1)
        self.assertEqual(poll.choice_set.filter(id = 1)[0].votes, 1)
        # Vote again 
        response = self.c.post('/polls/1/vote/', data = {'choice': 1}, follow = True)
        self.assertRedirects(response, '/polls/1/results/')
        poll = response.context['poll']
        self.assertEqual(poll.id, 1)
        self.assertEqual(poll.choice_set.filter(id = 1)[0].votes, 2)
    
