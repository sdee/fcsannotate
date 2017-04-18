import unittest, StringIO, os, requests
from datetime import datetime
from fcsannotate.fcsannotate import annotate_file
from fcsparser.api import FCSParser

class TestAnnotate(unittest.TestCase):

	TEST_DIR = os.path.abspath(os.path.dirname(__file__))
	TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
	TEST_FCS_FILE = os.path.join(TEST_DATA_DIR, 'Well_A01.fcs')
	TEST_CORRUPTED_FILE = os.path.join(TEST_DATA_DIR, 'corrupted.fcs')

	#test annotating FCS file with 'labeled_at' and 'flow_cytometer' fields
	def test_basic_annotate(self):
		outfile = annotate_file(self.TEST_FCS_FILE, 'iQue_1')
		fp1 = FCSParser(outfile)
		annotations = fp1.annotation
		self.assertIn('labeled_at', annotations)
		self.assertIn('flow_cytometer', annotations)
		self.assertEquals(annotations['flow_cytometer'], 'iQue_1')
		day = '{:%d-%b-%Y}'.format(datetime.now()).upper()
		self.assertTrue(day in annotations['labeled_at']) #only checks day portion of timestamp

	#test annotating FCS file with custom experimental fields.
	def test_custom_annotate(self):
		outfile = annotate_file(self.TEST_FCS_FILE, 'iQue_1', expdata1='d1', expdata2='d2')
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
			annotate_file(self.TEST_FCS_FILE, 'iQue_1', **{'kw1':'value1', '$restricted': 'value2'})

	def test_corrupted_file(self):
		with self.assertRaises(ValueError) as context:
			annotate_file(self.TEST_CORRUPTED_FILE)

if __name__ == "__main__":
    unittest.main()
