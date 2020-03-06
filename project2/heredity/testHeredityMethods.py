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
        self.people_2 = {
            'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False},
            'Hermione': {'name': 'Hermione', 'mother': None, 'father': None, 'trait': False},
            'Molly': {'name': 'Molly', 'mother': None, 'father': None, 'trait': None},
            'Ron': {'name': 'Ron', 'mother': 'Molly', 'father': 'Arthur', 'trait': False},
            'Rose': {'name': 'Rose', 'mother': 'Ron', 'father': 'Hermione', 'trait': True}
        }

        self.probabilities_0 = {
            'Harry': {'gene': {2: 0.1, 1: 0.3, 0: 0.1}, 'trait': {True: 0, False: 0}},
            'James': {'gene': {2: 0.2, 1: 0.3, 0: 0}, 'trait': {True: 0, False: 0}},
            'Lily': {'gene': {2: 0.04, 1: 0.01, 0: 0.01}, 'trait': {True: 0, False: 0}}
        }

        self.probabilities_0_norm = {
            'Harry': {'gene': {2: 0.2, 1: 0.6, 0: 0.2}, 'trait': {True: 0, False: 0}},
            'James': {'gene': {2: 0.4, 1: 0.6, 0: 0}, 'trait': {True: 0, False: 0}},
            'Lily': {'gene': {2: 0.2, 1: 0.0007115724000000001, 0: 0}, 'trait': {True: 0, False: 0}}
        }

    def testJointProbability(self):
        joint_prob_0 = hr.joint_probability(self.people_0, {"Harry"}, {"James"}, {"James"})
        # Verified
        self.assertEqual(joint_prob_0, 0.0026643247488)

    #     joint_prob_1 = hr.joint_probability(self.people_1, {}, {}, {"Fred"})
    #     self.assertEqual(joint_prob_1, 0.00875731494359588)

    #     joint_prob_2 = hr.joint_probability(self.people_2, {}, {}, {"Rose"})
    #     self.assertEqual(joint_prob_2, 0.008495339559497134)

    # def testNormalize(self):
    #     hr.normalize(self.probabilities_0)
    #     self.assertEqual(self.probabilities_0, self.probabilities_0_norm)

if __name__ == '__main__':
    unittest.main()