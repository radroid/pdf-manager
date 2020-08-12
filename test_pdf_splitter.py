"""Tests for pdf_splitter module."""


from pdf_splitter import PdfSplitter
from PyPDF2 import PdfFileReader
import PyPDF2
import pathlib
import pytest


file_path = 'Fourier Transforms.pdf'
pdf_splitter = PdfSplitter(file_path)


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
    p1, p2 = pdf_splitter.single_split(3)
    part_two = PdfFileReader(str(p2))
    num_diff = pdf_splitter.pdf_file.getNumPages() - 2 - part_two.getNumPages()
    assert num_diff == 0

    # Delete created files
    p1.unlink()
    p2.unlink()
    p1.parent.rmdir()


def test_multi_splitter_file_len():
    filenames = ['Index.pdf',
                 'Data in frequency domain.pdf',
                 'The complex Fourier Series',
                 'The Rest']
    file_lens = [2, 4, 2, 18]

    out = pdf_splitter.multi_split(3, 7, 9, filenames=filenames)
    directory = out[0]
    for num, name in zip(file_lens, filenames):
        path = directory / name
        part = PdfFileReader(str(path))
        assert part.getNumPages() == num

    # Delete created files
    for path in directory.iterdir():
        path.unlink()
    directory.rmdir()


def test_multi_splitter_pg_ValueError_1():
    with pytest.raises(ValueError):
        pdf_splitter.multi_split(-1)


def test_multi_splitter_pg_ValueError_2():
    with pytest.raises(ValueError):
        pdf_splitter.multi_split(27)


def test_multi_splitter_file_ValueError_2():
    with pytest.raises(ValueError):
        pdf_splitter.multi_split(filenames=['test1.pdf'])


def test_multi_splitter_filenames():
    directory, filenames = pdf_splitter.multi_split(3)
    assert filenames == ['part_1.pdf', 'part_2.pdf']

    # Delete created files
    for path in directory.iterdir():
        path.unlink()
    directory.rmdir()


def test_multi_splitter_dir_1():
    directory, filenames = pdf_splitter.multi_split(3, new_dir_name='Test dir')
    assert directory.name == 'Test dir'

    # Delete created files
    for path in directory.iterdir():
        path.unlink()
    directory.rmdir()


def test_multi_splitter_dir_2():
    directory, filenames = pdf_splitter.multi_split(3, new_dir_name='Test dir')
    assert directory.exists()

    # Delete created files
    for path in directory.iterdir():
        path.unlink()
    directory.rmdir()
