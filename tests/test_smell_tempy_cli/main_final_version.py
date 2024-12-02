import sys,re,pathlib,os,shutil,subprocess

sys.path.append('./tests/test_smell_tempy_cli/assets')  
from components import SourceCode, Method, Classe, Data
from python_parser import PythonParser
from detector import *
from report_generator import ReportGenerator
from report_generator_csv import ReportGeneratorCSV

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter import messagebox
from pathlib import Path


def get_all_test_file(new_list, tempdir):
	"""
	Aqui parte final onde voce da ok e gera os reports.
	windows_3_part2.

	:param lista: lista dos arquivos de testes encontrados.
	:type lista: lkinter.listbox
	:param tempdir: diretorio pai onde estão os arquivos
	:type tempdir: str

	"""
	all_logs, projects = [], []

	for x in range(len(new_list)):
		p = PythonParser(new_list[x])
		if (p.ast_parser):
			all_logs.append(p.start())
		else:
			all_logs.append(p.start2())
		
		projects.append( new_list[x] )
	prev, cont_proj, cont_total, ts_qtd  = None, 0, 0, []

	for index in range(len(all_logs)):
		for log in all_logs[index]:
			if (log.lines == prev):
				pass
			else:
				cont_proj += 1
				cont_total += 1
			prev = log.lines
		ts_qtd.append( cont_proj )
		cont_proj = 0

	report_generator(cont_total, all_logs, projects, ts_qtd)
	report_generator_csv(all_logs,projects,tempdir)
	sys.exit(0)
		

def close_window(window): # nao usa 
	window.destroy()


def close_window_confirmation(newWindow): # nao usa
    if (tkinter.messagebox.askokcancel(title=None, message="Do you really want to close this window?")):
    	close_window(newWindow)


def test_file_selection_window(nomes,paths,tempdir):
	"""
	Monsta a lista de paths dos arquivos de teste e faz a analise.
	""" 
	new_list = []

	for x in range(0,len(nomes)):
		new_list.append(paths[x] + "/" + nomes[x])

	get_all_test_file(new_list,tempdir)


def generate_test_file_list_log(files,nomes,paths, tempdir):
	"""
	Momento de analisar testes ou não, dependendo se existe testes no diretorio.
	"""
	if (files >= 1):
		test_file_selection_window(nomes,paths,tempdir)

	else:
		print('No Python test file found.')


def is_hidden_directory(dirName):
	if( dirName.find( '/.' )!=-1 ):
		return True
	else:
		return False


def is_test_file(filename,path='0'):
	""" A verificação de ser um arquivo de test é além de outras coisas (em outros metodos) é 
	encontrar qual o framework de teste. Ou unittest ou pytest."""
	if (path=='0'):
		f = open(filename, 'r', encoding="utf8", errors='ignore')
	else:
		f = open(path + '/' + filename, 'r', encoding="utf8", errors='ignore')
	for line in f:
		if (line.find('assert') == 0):
			f.close()
			return True
		if (line.find('import unittest') != -1 or line.find('import pytest') != -1 or line.find('from unittest') != -1 or line.find('from pytest') != -1):
			f.close()
			return True
	f.close()
	return False


def search_test_file(tempdir):
	"""
	Aqui é feito a busca de todos os arquivos de testes a partir desse diretorio fornecido.
	"""
	number_of_files, paths, nomes = 0,[],[]
	for dirName, subdirList, fileList in os.walk(tempdir):
		if( not is_hidden_directory(dirName) ):
			for x in fileList:
				if ( x.endswith( '.py' ) and x.find( 'main.py' )==-1):
					if (is_test_file(x,dirName)):
						number_of_files += 1
						nomes.append(x)
						paths.append(dirName)

	generate_test_file_list_log(number_of_files,nomes,paths,tempdir)


def report_generator(cont, all_logs, projects, ts_qtd):
	report = ReportGenerator()
	report.add_header( cont, len(all_logs) , projects, ts_qtd)
	prev = None
	for index in range(len(all_logs)):			
		report.add_table_header( projects[index], ts_qtd[index] )
		for log in all_logs[index]:
			if (log.lines == prev):
				pass
			else:
				report.add_table_body( log.test_smell_type, log.method_name, log.lines )
			prev = log.lines
		report.add_table_close(ts_qtd[index])
	report.add_footer()
	report.build()

def report_generator_csv(all_logs, projects, tempdir):
	report2 = ReportGeneratorCSV(tempdir)
	prev2 = None
	for index2 in range(len(all_logs)):
		for log2 in all_logs[index2]:
			if log2.lines == prev2:
				pass
			else:
				report2.add_csv_body(log2.test_smell_type, log2.method_name, log2.lines, projects[index2])
			prev2 = log2.lines
	report2.build()
	return report2.get_file_name()


def select_directory(path_root: str):
	"""
	Identificado o caminho onde estão os testes.
	"""
	currdir = os.getcwd()
	#new_path = os.path.join(currdir, 'tests/unit')   <<<<<<<<
	new_path = os.path.join(currdir, path_root)

	if (len(new_path) > 0):
		search_test_file(new_path)


if __name__ == '__main__':
	p = Path("./tests/test_smell_tempy_cli/report/") 
	#p = Path("./TEMPY/report/")
	if p.exists() == False:
		os.mkdir("./tests/test_smell_tempy_cli/report/")
	
	if len(sys.argv) != 2:
		sys.stderr.write('Usage: Missing argv <directory_test_root> class "str"')
		sys.exit(1)
		
	directory = sys.argv[1]
	select_directory(path_root=directory)
