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
            'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': True},
            'Hermione': {'name': 'Hermione', 'mother': None, 'father': None, 'trait': False},
            'Molly': {'name': 'Molly', 'mother': None, 'father': None, 'trait': False},
            'Ron': {'name': 'Ron', 'mother': 'Molly', 'father': 'Arthur', 'trait': False},
            'Rose': {'name': 'Rose', 'mother': 'Ron', 'father': 'Hermione', 'trait': True}
        }

        self.probabilities_0 = {
            'Harry': {'gene': {2: 0.1, 1: 0.3, 0: 0.1}, 'trait': {True: 0.9, False: 0}},
            'James': {'gene': {2: 0.2, 1: 0.3, 0: 0}, 'trait': {True: 0.8, False: 0}},
            'Lily': {'gene': {2: 0.04, 1: 0.01, 0: 0.01}, 'trait': {True: 0, False: 1}}
        }

        self.probabilities_0_norm = {
            'Harry': {'gene': {2: 0.2, 1: 0.6, 0: 0.2}, 'trait': {True: 1.0, False: 0}},
            'James': {'gene': {2: 0.4, 1: 0.6, 0: 0}, 'trait': {True: 1.0, False: 0}},
            'Lily': {'gene': {2: 0.6666666666666666, 1: 0.16666666666666666, 0: 0.16666666666666666}, 'trait': {True: 0.0, False: 1.0}}
        }

        self.probabilities_1 = {
            'Arthur': {'gene': {2: 0.0010715694733938617, 1: 0.006092582611726968, 0: 0.026465216431249546}, 'trait': {True: 0, False: 0.03362936851637028}},
            'Charlie': {'gene': {2: 9.660732549755268e-05, 1: 0.004521731224790018, 0: 0.02901102996608282}, 'trait': {True: 0, False: 0.03362936851637028}},
            'Fred': {'gene': {2: 0.00046837620497237127, 1: 0.023468597147422585, 0: 0.009692395163975381}, 'trait': {True: 0.03362936851637028, False: 0}},
            'Ginny': {'gene': {2: 0.00018626549455374455, 1: 0.006790126989805804, 0: 0.026652976032010882}, 'trait': {True: 0.004187262672044918, False: 0.029442105844325498}},
            'Molly': {'gene': {2: 0.0010715694733938615, 1: 0.006092582611726968, 0: 0.026465216431249543}, 'trait': {True: 0, False: 0.03362936851637028}},
            'Ron': {'gene': {2: 0.00018626549455374474, 1: 0.006790157042721004, 0: 0.02665294597909568}, 'trait': {True: 0.00418726267204492, False: 0.029442105844325498}}
            }

        self.probabilities_1_updated = {
            'Arthur': {'gene': {2: 0.0010715694733938617, 1: 0.006093070971598968, 0: 0.026465216431249546}, 'trait': {True: 0, False: 0.03362985687624228}},
            'Charlie': {'gene': {2: 9.660732549755268e-05, 1: 0.0045222195846620185, 0: 0.02901102996608282}, 'trait': {True: 0, False: 0.03362985687624228}},
            'Fred': {'gene': {2: 0.00046837620497237127, 1: 0.023469085507294585, 0: 0.009692395163975381}, 'trait': {True: 0.03362985687624228, False: 0}},
            'Ginny': {'gene': {2: 0.00018675385442574454, 1: 0.006790126989805804, 0: 0.026652976032010882}, 'trait': {True: 0.004187751031916918, False: 0.029442105844325498}},
            'Molly': {'gene': {2: 0.0010715694733938615, 1: 0.006093070971598968, 0: 0.026465216431249543}, 'trait': {True: 0, False: 0.03362985687624228}},
            'Ron': {'gene': {2: 0.00018626549455374474, 1: 0.006790645402593004, 0: 0.02665294597909568}, 'trait': {True: 0.0041877510319169205, False: 0.029442105844325498}}
        }

    def testJointProbability(self):
        joint_prob_0 = hr.joint_probability(self.people_0, {"Harry"}, {"James"}, {"James"})
        # Verified
        self.assertEqual(joint_prob_0, 0.0026643247488)

        joint_prob_1 = hr.joint_probability(self.people_1, {}, {}, {"Fred"})
        self.assertEqual(joint_prob_1, 0.008764324299878399)

        joint_prob_2 = hr.joint_probability(self.people_2, {}, {'Arthur'}, {'Arthur'})
        self.assertEqual(joint_prob_2, 0.00022787243179683852)

    def testNormalize(self):
        hr.normalize(self.probabilities_0)
        self.assertEqual(self.probabilities_0, self.probabilities_0_norm)

    def testUpdate(self):
        hr.update(self.probabilities_1, {'Fred', 'Ron', 'Arthur', 'Charlie', 'Molly'}, {'Ginny'},{'Ginny', 'Fred', 'Ron'}, 4.883598720000002e-07)
        self.assertEqual(self.probabilities_1, self.probabilities_1_updated)

if __name__ == '__main__':
    unittest.main()