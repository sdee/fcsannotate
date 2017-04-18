import unittest, StringIO, os, requests
from datetime import datetime
from fcsannotate import app
from fcsparser.api import FCSParser
from fcsannotate.utils import create_temporary_copy

#integration test for Annotate endpoint
class TestAnnotateEndpoint(unittest.TestCase):

	def test_annotation_endpoint(self):
		with open('./fcsannotate/tests/data/Well_A01.fcs', 'rb') as fcs:
			fcsStringIO = StringIO.StringIO(fcs.read())
		with app.test_client() as c:
			resp = c.put('http://localhost/fcs_data/annotate/',
				input_stream=fcsStringIO,
				headers={'Content-Type': 'application/octet-stream'})
			self.assertEqual(resp.status_code, 200)
			#write data to tempfile, read into FCSParser, and verify annotation
			fpath = create_temporary_copy(resp.data)
			fp = FCSParser(fpath)
			if (os.path.exists(fpath)):
				os.remove(fpath)
			annotations = fp.annotation
			self.assertIn('labeled_at', annotations)
			self.assertIn('flow_cytometer', annotations)
			self.assertEquals(annotations['flow_cytometer'], 'iQue_1')
			day = '{:%d-%b-%Y}'.format(datetime.now()).upper()
			self.assertTrue(day in annotations['labeled_at']) #only checks day portion of timestamp

	def test_no_file(self):
		with app.test_client() as c:
			resp = c.put('http://localhost/fcs_data/annotate/',
				headers={'Content-Type': 'application/octet-stream'})
			self.assertEqual(resp.status_code, 404)

	def test_corrupted_file(self):
		with open('./fcsannotate/tests/data/corrupted.fcs', 'rb') as fcs:
			fcsStringIO = StringIO.StringIO(fcs.read())
		with app.test_client() as c:
			resp = c.put('http://localhost/fcs_data/annotate/',
				input_stream=fcsStringIO,
				headers={'Content-Type': 'application/octet-stream'})
			self.assertEqual(resp.status_code, 500)

if __name__ == "__main__":
    unittest.main()
