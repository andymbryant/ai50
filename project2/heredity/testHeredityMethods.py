import unittest
import heredity as hr

class TestHeredityMethods(unittest.TestCase):
    def setUp(self):
        self.people_0 = {
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }
        self.people_1 = {
            'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False},
            'Charlie': {'name': 'Charlie', 'mother': 'Molly', 'father': 'Arthur', 'trait': False},
            'Fred': {'name': 'Fred', 'mother': 'Molly', 'father': 'Arthur', 'trait': True},
            'Ginny': {'name': 'Ginny', 'mother': 'Molly', 'father': 'Arthur', 'trait': None},
            'Molly': {'name': 'Molly', 'mother': None, 'father': None, 'trait': False},
            'Ron': {'name': 'Ron', 'mother': 'Molly', 'father': 'Arthur', 'trait': None}
        }

    def testJointProbability0(self):
        joint_prob_0 = hr.joint_probability(self.people_0, {"Harry"}, {"James"}, {"James"})
        self.assertEqual(joint_prob_0, 0.0026643247488)

    def testJointProbability1(self):
        joint_prob_1 = hr.joint_probability(self.people_1, {}, {}, {"Fred"})
        self.assertEqual(joint_prob_1, 0.00036864)

if __name__ == '__main__':
    unittest.main()