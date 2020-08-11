"""The module splits a PDF into two different PDFs at
a specified page number."""


from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter


class PdfSplitter:
    """The class manages splitting of PDFs files.

    Attributes:
        pdf_file (PdfFileReader Object): the file object is used to read the
        PDF document.
        path_to_file (PosixPath object): defines the location to the PDF
        document.
    """

    def __init__(self, path_to_file):
        """Instantiate the class.

        Args:
            path_to_file (str or PosixPath object): location of the PDF
            document.
        """
        if type(path_to_file) == str:
            path_to_file = Path(path_to_file)

        # Defining the possible errors.
        if not path_to_file.exists():
            raise FileExistsError('No file exists at the path input.')
        elif not path_to_file.is_file:
            raise TypeError('The path entered does not contain any file.')
        elif not path_to_file.suffix == '.pdf':
            raise TypeError('Location of a PDF document not specified.')

        self.path_to_file = path_to_file
        self.pdf_file = PdfFileReader(str(path_to_file))

    def single_split(self, pg_num, filenames=['part_1.pdf', 'part_2.pdf']):
        """Split the PDF document into two separate files.

        Args:
            pg_num (int): page number to be split at.
            The specified page will be part of the second PDF document.
            filenames (list, optional): specify file names.
            Defaults to ['first_part', 'second_part'].

        """
        if pg_num <= 1:
            raise ValueError('The input number will return the PDF '
                             'document as it is right now.')

        pg_num -= 1

        # Define paths for a directory and two PDF files.
        new_dir = self.path_to_file.parent / 'Split PDFs'
        part_one = new_dir / filenames[0]
        part_two = new_dir / filenames[1]

        # Adjust filenames if default and exists.
        if new_dir.exists():
            p1_name = 'part_1({}).pdf'
            p2_name = 'part_2({}).pdf'
            num = 1
            while part_one.exists() or part_two.exists():
                part_one = new_dir / p1_name.format(num)
                part_two = new_dir / p2_name.format(num)
                num += 1

        # Create a new directory to store the split PDFs.
        new_dir.mkdir(exist_ok=True)

        # Create PDF pages.
        pdf_writer_1 = PdfFileWriter()
        pdf_writer_2 = PdfFileWriter()

        for page in self.pdf_file.pages[:pg_num]:
            pdf_writer_1.addPage(page)

        for page in self.pdf_file.pages[pg_num:]:
            pdf_writer_2.addPage(page)

        # Save PDF files.
        with part_one.open(mode='wb') as out_pdf:
            pdf_writer_1.write(out_pdf)

        with part_two.open(mode='wb') as out_pdf:
            pdf_writer_2.write(out_pdf)
