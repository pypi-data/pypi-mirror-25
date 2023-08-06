'''
Created on Sep 24, 2017

@author: davidlepage
'''
from threading import Timer
import unittest
from smc import session
from smc.base.model import Element
from smc_monitoring.pubsub.subscribers import Notification, Event
from smc.elements.network import Network, Host
from constants import url, api_key
from __builtin__ import int



class Test(unittest.TestCase):


    def setUp(self):
        session.login(
            url=url, api_key=api_key, verify=False,
            timeout=40)

    def tearDown(self):
        try:
            session.logout()
        except (SystemExit, SMCConnectionError):
            # SMC Connection error happens in test_query_no_session
            # bc logout is done and during tearDown logout will be attempted
            # again on a closed session.
            pass


    def test_notification_setup(self):
        notification = Notification('network')
        self.assertDictEqual(notification.request, {'context': 'network'})
    
        notification = Notification('network,host')
        self.assertDictEqual(notification.request, {'context': 'network,host'})
        
        notification = Notification('network')
        notification.subscribe('host')
        self.assertIsInstance(notification.subscriptions[0], Notification)
        self.assertDictEqual(notification.subscriptions[0].request, {'context': 'host'})
        
        
    def test_notification_changes(self):
        notification = Notification('network')
        
        def elements():
            Network.create('foonetwork', '1.1.1.0/24')
            
        t = Timer(1.0, elements)
        t.start()  # after 30 seconds, "hello, world" will be printed
        
        for event in notification.notify():
            self.assertIsInstance(event, dict)
            break
    
    def test_multiple_subscribes(self):
        
        def elements():
            Host.create('myhost', '1.1.1.1')
            Network.create('dingohost', '1.1.1.0/24')
            
        t = Timer(1.0, elements)
        t.start()  # after 30 seconds, "hello, world" will be printed
        
        notification = Notification('network')
        notification.subscribe('host')
        
        i = 0
        for event in notification.notify(as_type=Event):
            self.assertIsInstance(event, Event)
            self.assertIsInstance(event.subscription_id, int)
            self.assertIsInstance(event.action, basestring)
            i += 1
            if i == 5:
                break
            
        
        
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()