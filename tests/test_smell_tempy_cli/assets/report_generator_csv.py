import sys,re,pathlib,os,shutil,subprocess
from components import SourceCode, Method, Classe, Data


class ReportGeneratorCSV:

	def __init__(self, tempdir):
		self.file = open("./tests/test_smell_tempy_cli/report/test_smell_csv_log.csv", 'w')
		self.content = ''
		self.number_of_test_smells = 1
		self.tempdir = tempdir
		self.add_csv_head()


	def add_csv_head(self):
		self.content += "".join([
			'#,',
			'Project,',
			'File,',
			'Path,',
			'Test Smell,',
			'Method,',
			'start,end',
			'\n'
		])

	def add_csv_body(self, ts, method, lines, path):
		self.content += "".join([
			str(self.number_of_test_smells).lstrip(),',',
			str(self.get_project_name(path)).lstrip(),',',
			str(self.get_testfile_name(path)).lstrip(),',',
			str(self.get_path(path)).lstrip(),',',
			ts.lstrip(),',',
			method.lstrip(),',',
			str(lines)[1:-1],
			'\n'
		])
		self.number_of_test_smells += 1


	def build(self): # final step (step 7)
		self.file.write( self.content )
		self.file.close()

	def get_testfile_name(self, path):
		for x in range(len(path)-1, -1, -1):
			if (path[x] == '/'):
				return path[x+1:]

	def get_path(self, path):
		for x in range(len(path)-1, -1, -1):
			if (path[x] == '/'):
				return path[0:x+1]
			
	def get_project_name(self, path):
		path2 = path.replace(self.tempdir+'/','')
		path2 = path2[0:path2.find('/')]
		return path2

	def get_file_name(self):
		return self.file.name