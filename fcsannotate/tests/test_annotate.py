import unittest, StringIO, os, requests
from datetime import datetime
from fcsannotate.fcsannotate import annotate_file
from fcsparser.api import FCSParser

class TestAnnotate(unittest.TestCase):

	#test annotating FCS file with 'labeled_at' and 'flow_cytometer' fields
	def test_basic_annotate(self):
		outfile = annotate_file('./fcsannotate/tests/data/Well_A01.fcs', 'iQue_1')
		fp1 = FCSParser(outfile)
		annotations = fp1.annotation
		self.assertIn('labeled_at', annotations)
		self.assertIn('flow_cytometer', annotations)
		self.assertEquals(annotations['flow_cytometer'], 'iQue_1')
		day = '{:%d-%b-%Y}'.format(datetime.now()).upper()
		self.assertTrue(day in annotations['labeled_at']) #only checks day portion of timestamp

	#test annotating FCS file with custom experimental field.
	def test_custom_annotate(self):
		outfile = annotate_file('./fcsannotate/tests/data/Well_A01.fcs', 'iQue_1', expdata1='d1', expdata2='d2')
		fp2 = FCSParser(outfile)
		annotations = fp2.annotation
		#make sure basic fields not affected
		self.assertIn('labeled_at', annotations)
		self.assertIn('flow_cytometer', annotations)
		self.assertEquals(annotations['flow_cytometer'], 'iQue_1')
		#check for custom fields
		self.assertIn('expdata1', annotations)
		self.assertIn('expdata2', annotations)
		self.assertEquals(annotations['expdata1'], 'd1')
		self.assertEquals(annotations['expdata2'], 'd2')

	#test annotating FCS file with restricted fields
	def test_bad_annotate(self):
		with self.assertRaises(ValueError) as context:
			annotate_file('./fcsannotate/tests/data/Well_A01.fcs', 'iQue_1', **{'kw1':'value1', '$restricted': 'value2'})

	def test_corrupted_file(self):
		with self.assertRaises(ValueError) as context:
			annotate_file('./fcsannotate/tests/data/corrupted.fcs')

if __name__ == "__main__":
    unittest.main()
