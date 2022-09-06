from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

     def testOne(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def testPage(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('plays'))
            self.assertIsNone(session.get('bestscore'))
            self.assertIn(b'<p>Best Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def testWord(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "A", "P", "A", "M"], 
                                 ["M", "K", "U", "Y", "O"], 
                                 ["B", "C", "I", "A", "Q"], 
                                 ["L", "T", "S", "Z", "S"], 
                                 ["W", "R", "M", "A", "P"]]
        response = self.client.get('/check-word?word=map')
        self.assertEqual(response.json['result'], 'ok')

    def testOnBoard(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'notaword')

    def testIfRealWord(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'notontheboard')


