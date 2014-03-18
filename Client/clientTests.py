__author__ = 'harry'

import unittest
import TankClient
import time

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TankClient.GameController(0,0,0,0, True)
        self.bullet = TankClient.Bullet(0,0,0,0,0,0,0)

    def setBulletPen(self, pen):
        self.bullet.penetration = pen
        time.sleep(0.2)
        #print "Bullet pen set to: " + str(self.bullet.penetration)

    def test_penetration(self):
        print "\nTesting 100 pen at 90 degrees against 50mm of armour"
        self.setBulletPen(100)
        self.assertTrue(self.client.doesPenetrate(90, self.bullet, 50))
        ###############################################################
        print "\nTesting 100 pen at 90 degrees against 100mm of armour"
        self.setBulletPen(100)
        self.assertTrue(self.client.doesPenetrate(90, self.bullet, 100))
        ###############################################################
        print "\nTesting 100 pen at 45 degrees against 100mm of armour"
        self.setBulletPen(100)
        self.assertFalse(self.client.doesPenetrate(45, self.bullet, 100))
        ###############################################################
        print "\nTesting 150 pen at 45 degrees against 100mm of armour"
        self.setBulletPen(150)
        self.assertTrue(self.client.doesPenetrate(45, self.bullet, 100))
        ###############################################################
        print "\nTesting 20000 pen at 10 degrees against 1mm of armour"
        self.setBulletPen(100)
        self.assertFalse(self.client.doesPenetrate(20000, self.bullet, 1))
        ###############################################################


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
