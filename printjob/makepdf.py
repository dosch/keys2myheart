from fpdf import FPDF
import qrcode

# Sample revocation certificate (comment line removed)
REVDATA = """-----BEGIN PGP PUBLIC KEY BLOCK-----
iQIfBCABCAAJBQJVRfVlAh0AAAoJEEu3ZcdGhrVcd1cP+QGNaIhNtJts6f7GLLDT
CMewIqmAZojG/WpaDSK/OM+clTv74KTpFlyzomulKdA1fBb7OfJqFMIES/lMtYWN
SGkDQe2VZ4W4o6F34dv+x9lSTUp5pSB1D1b2k5yn9N/mrVhyHDSj2KJtE2aYSEI3
9jr+cDx1wIdJdkv9glXjup0N/J0xMgSUtAQX4D1dNlQAlSs4669RFVWmrHuegnaA
EpOGvXeJWJOx+frP3CD9hVO8Uj3w4Y/Dk6X6hvoKQ76TN08AK54w9G5M1K2wbMN7
a7vz+UBmllvdRZNk6sZVWuFmh5VWiiDAoQPDrS5pHJ5E7Zlj+EghoCrbFht2aEad
ZduzrT7aUK3q7A80ohxz6uRHro5L/4JJtWG7S9M21nVNkWSFNOc/oOlk2zH7bd4c
WglvSiB4CzxPU86TGB++TPqmVKOHWAwPRaKhDEx0arne1yuJU6EhAlNewhQdAPfT
5TPfq1kdYl8HX5wMmN3mEs6e6LteuVZMv3Kf6AEbOptSxOZDRb7gPECFkyfoLv6x
ad/nQonC3B9Y0H5HLW2O4F8AMEn0TQCa4p2PD0Z06XGaDfzFHFLUTs/wTafZGDgr
2bjEWSf1Sd0xDUO0mIxublp39S1nx5UluLP9DIA8cYdjFbQbpBngwoK8ySLTMtBg
ay8nhKjdNwOE7AZJtVozmOTp
=3Yrt
-----END PGP PUBLIC KEY BLOCK-----"""


# for docu see: https://code.google.com/p/pyfpdf/wiki/FPDF
class PDF(FPDF):
        def header(self):
                # Logo
                self.image('qr_code.png', 1, 1, 39)
                # Arial bold 15
                self.set_font('Arial','B',15)
                # Move to the right
                self.cell(80)
                # Title
                self.cell(30,10,'Title',1,0,'C')
                # Line break
                self.ln(20)

        # Page footer
        def footer(self):
                # Position at 1.5 cm from bottom
                self.set_y(-15)
                # Arial italic 8
                self.set_font('Arial','I',8)
                # Page number
                #this.cell(0,10,'Page '+str(this.PageNo())+'/{nb}',0,0,'C')

def make_qr_code():
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        qr.add_data(REVDATA)
        qr.make(fit=True)

        img = qr.make_image()
        img.save("qr_code.png")

def test_pdf_gen():
        #pdf = PDF('L', 'mm',(88,41))  # DYMO label: landscape, 88x41mm
        pdf = PDF('L', 'mm',(41,88))  # DYMO label: landscape, 88x41mm
        #pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_y(2.8)
        #pdf.set_xy(40, 4)

        x_pos = 76
        # arial bold, 12
        pdf.set_font('Arial', 'B', 9.6)
        # w, h, txt, border, line, align
        pdf.cell(x_pos, 4, 'Franklin Delano Roosevelt', 0, 1, 'R')

        pdf.set_font('Arial', '', 7)
        pdf.cell(x_pos, 4, 'Franklin.Roosevelt@whitehouse.gov.us', 0, 1, 'R')

        #pdf.set_y(30)
        pdf.ln(6)
        pdf.set_font('Arial', 'U', 9)
        pdf.cell(x_pos, 4, 'www.key2myheart.nl', 0, 0, 'R')

        # write out
        pdf.output('test.pdf','F')


def main():
        make_qr_code()
        test_pdf_gen()


if __name__ == "__main__":
        main()
