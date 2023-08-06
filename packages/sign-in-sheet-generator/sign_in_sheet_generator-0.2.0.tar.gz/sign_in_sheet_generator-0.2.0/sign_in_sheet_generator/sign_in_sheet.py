from fpdf import FPDF

class SignInSheet:
    LIST_COLUMN_Y_START = 40
    LIST_COLUMN_Y_STOP = 275

    LIST_COLUMN_1_X = 40
    LIST_COLUMN_2_X = 120

    LIST_ENTRY_FONT_SIZE = 10

    def __init__(self, page_title=None, page_subtitle=None, names=None, output_filepath=None):
        self.page_title = page_title
        self.page_subtitle = page_subtitle
        self.output_filepath = output_filepath if output_filepath else "sign_in_sheet.pdf"

        self.names = names if names is not None else []
        self.pdf = None

    def generate(self):
        try:
            self.pdf = FPDF()
            self.add_page()

            current_x = self.LIST_COLUMN_1_X
            current_y = self.LIST_COLUMN_Y_START

            for name in sorted(self.names):
                self.pdf.set_font('Arial', size=self.LIST_ENTRY_FONT_SIZE)
                self.pdf.rect(current_x - 5, current_y-2.5, w=3, h=3)
                self.pdf.text(current_x, current_y, name)
                current_y += 6
                if current_y > self.LIST_COLUMN_Y_STOP:
                    current_y = self.LIST_COLUMN_Y_START
                    if current_x == self.LIST_COLUMN_1_X:
                        current_x = self.LIST_COLUMN_2_X
                    else:
                        current_x = self.LIST_COLUMN_1_X
                        self.add_page()


            self.pdf.output(self.output_filepath, 'F')
        finally:
            self.pdf = None

    def add_page(self):
        self.pdf.add_page()
        self.generate_headers()

    def generate_headers(self):
        if self.page_title:
            self.pdf.set_font('Arial', 'B', 16)
            self.pdf.cell(0, txt=self.page_title, h=10, ln=1, align='C')
        if self.page_subtitle:
            self.pdf.set_font('Arial', 'B', 14)
            self.pdf.cell(0, txt=self.page_subtitle, h=10, ln=1, align='C')
