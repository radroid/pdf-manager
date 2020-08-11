"""Tests for pdf_splitter module."""


from pdf_splitter import PdfSplitter
from PyPDF2 import PdfFileReader
import PyPDF2
import pathlib
import pytest


file_path = 'Fourier Transforms.pdf'


def test_object_creation_1():
    pdf_splitter = PdfSplitter(file_path)
    assert type(pdf_splitter.path_to_file) == pathlib.PosixPath


def test_object_creation_2():
    pdf_splitter = PdfSplitter(file_path)
    assert type(pdf_splitter.pdf_file) == PyPDF2.pdf.PdfFileReader


def test_object_creation_3():
    with pytest.raises(FileExistsError):
        PdfSplitter('file-does-not-exist.pdf')


def test_object_creation_4():
    with pytest.raises(TypeError):
        PdfSplitter('pdf_manager')


def test_object_creation_5():
    with pytest.raises(TypeError):
        PdfSplitter('README.md')


def test_single_split():
    pdf_splitter = PdfSplitter(file_path)
    pdf_splitter.single_split(3)
    path = pathlib.Path('Split PDFs') / 'part_2.pdf'
    part_two = PdfFileReader(str(path))
    num_diff = pdf_splitter.pdf_file.getNumPages() - 2 - part_two.getNumPages()
    assert num_diff == 0
