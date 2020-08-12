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
            pg_num (int): page number to be split at. The specified page will
                          be the first page of the second PDF document.
            filenames (list, optional): specify file names. Defaults to
                                        ['first_part', 'second_part'].

        """
        if pg_num <= 1:
            raise ValueError('The input number will return the PDF '
                             'document as it is right now.')

        pg_num -= 1

        # Define paths for a directory and two PDF files.
        new_dir = self.path_to_file.parent / 'Single Split PDFs'
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

        return part_one, part_two

    def multi_split(self, *pg_nums, filenames=[],
                    new_dir_name='Multi Split PDFs'):
        """The function takes a series of page numbers that are used to split
        the provided PDF document. The page numbers provided will be the first
        page of a new PDF document.

        Args:
            filenames (list, optional): Names of the files that are split.
                                        Defaults to [].
            new_dir_name (str or PosixPath object): path to the new or
                                                    existing directory the
                                                    split PDFs are to be saved.

        Returns:
            new_dir (PosixPath object): path to the newly created directory.
            filenames (list): names of all the files created in the directory.

        Raises:
            ValueError: if page numbers entered are out of range.
            ValueError: if number of filenames provided are greater

        Example:
            * PDF document = 20 pages.
            multi_split(3, 8, 10, filenames=['part1.pdf',
                                             'part2.pdf',
                                             'part3.pdf',
                                             'part4.pdf'])

            * Four (4) PDF documents created:
             - part1.pdf -> pages 1 to 2, included.
             - part2.pdf -> pages 3 to 7, included.
             - part3.pdf -> pages 8 to 9, included.
             - part4.pdf -> pages 10 to 20, included.
        """
        doc_pages = self.pdf_file.getNumPages()

        # Process input page numbers
        if min(pg_nums) <= 1 or max(pg_nums) >= doc_pages:
            raise ValueError('One of the page number entered is not within '
                             'the range of available pages.')

        pages = [pg - 1 for pg in pg_nums]
        pages.append(0)
        pages.append(doc_pages)
        pages.sort()

        # Process input filenames
        if len(filenames) >= len(pages):
            raise ValueError('The number of filenames input are greater the '
                             'PDF documents to be created.')

        # Add missing filenames
        if len(filenames) < len(pages) - 1:
            for i in range(len(filenames)+1, len(pages)):
                filenames.append(f'part_{i}.pdf')

        # Fix extension
        for i, name in enumerate(filenames):
            if name[-4:] != '.pdf':
                filenames[i] = f'{name}.pdf'

        # Create directory
        new_dir = self.path_to_file.parent / new_dir_name

        if new_dir.name == 'Multi Split PDFs':
            dir_num = 1
            while new_dir.exists():
                new_dir = new_dir.parent / f'Multi Split PDFs ({dir_num})'
                dir_num += 1

        new_dir.mkdir(exist_ok=True)

        # Write pages
        for i, name in enumerate(filenames):
            writer = PdfFileWriter()
            first_pg = pages[i]
            last_pg = pages[i + 1]

            for page in self.pdf_file.pages[first_pg:last_pg]:
                writer.addPage(page)

            new_file = new_dir / name
            with new_file.open('wb') as out_pdf:
                writer.write(out_pdf)

        return new_dir, filenames
