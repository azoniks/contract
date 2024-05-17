import io
import os

from fitz import fitz, Rect

from contracts.settings import PATH_PDF_TEMPLATES, PATH_FONTS


class PDFWriter:
    """ Interact with PDF documents. """

    def __init__(self) -> None:
        pass

    def _write_contract_data(self, pdf_document: fitz, contract_data: list) -> bytes:
        """ Insert text into a PDF document and return a ByteIO object. """

        pdf_bytes = io.BytesIO()

        for data in contract_data:
            page = data['page']
            text = data['text']
            fontfile = data['fontdata']['fontfile']
            fontname = data['fontdata']['fontname']
            fontsize = data['fontsize']
            x = data['x']
            y = data['y']

            page = pdf_document[page]
            page.clean_contents()
            page.insert_font(fontname=fontname, fontfile=fontfile)
            point = fitz.Point(x=x, y=y)
            page.insert_text(point=point, text=str(text), fontfile=fontfile, fontname=fontname, fontsize=fontsize)

        pdf_document.save(pdf_bytes)
        pdf_document.close()

        return pdf_bytes.getvalue()

    def _write_contract_data_with_html(self, pdf_document: fitz, page: int, text: str, css: str, rect: tuple):
        """ Inserting data using an HTML fragment. """
        page = pdf_document[page]
        page.insert_htmlbox(Rect(rect), text=text, css=css)

    def _get_person_position(self, fontdata: dict, persons: list) -> list[dict]:
        """ Calculate the person's position on page 3 of 'rent_contract.pdf'. """
        person_data = []
        persons_count = 70 / len(persons)
        position = 169 + (persons_count / 2)

        for i, person in enumerate(persons):
            person = f'{i + 1}) {person.strip()}'
            person_data.append(
                {'page': 2, 'text': person, 'fontdata': fontdata, 'fontsize': 10, 'x': 71, 'y': position}
            )
            position += persons_count
        return person_data

    def _split_description_text(self, text: str, length: int, max_length: int) -> list[str]:
        """
        Splitting text, calculating string length, determining the position to start a new line.
        Used in 'sale_contract.pdf
        """
        result = []
        if len(text) > max_length:
            index = text.rfind(' ', 0, max_length)
            text = text[:index].strip()

        while len(text) >= length:
            index = text.rfind(' ', 0, length)
            result.append(text[:index].strip())
            text = text[index:]
        else:
            result.append(text.strip())
        return result

    # Mietvertrag Stallschreiberstr contract.
    def rent_contract(self, contracts_info: dict) -> bytes:
        landlord = contracts_info.get('landlord')
        renter = contracts_info.get('renter')
        resident = contracts_info.get('resident')
        passport = contracts_info.get('passport')
        date_of_expiry = contracts_info.get('date_of_expiry').strftime('%d.%m.%Y')
        address = contracts_info.get('address')
        floor = contracts_info.get('floor')
        rooms = contracts_info.get('rooms')
        balcony = contracts_info.get('balcony')
        area = contracts_info.get('area')
        start_date = contracts_info.get('start_date').strftime('%d.%m.%Y')
        stop_date = contracts_info.get('stop_date').strftime('%d.%m.%Y')
        iban = contracts_info.get('iban')
        bic = contracts_info.get('bic')
        credit_institution = contracts_info.get('credit_institution')
        purpose = contracts_info.get('purpose')
        monthly_rent = contracts_info.get('monthly_rent')
        extra_costs = contracts_info.get('extra_costs')
        deposit = contracts_info.get('deposit')
        persons = contracts_info.get('persons')
        location = contracts_info.get('location')
        contract_date = contracts_info.get('contract_date').strftime('%d.%m.%Y')

        rent_cost = f'{monthly_rent + extra_costs},00 €'
        monthly_rent = f'{monthly_rent},00 €'
        extra_costs = f'{extra_costs},00 €'
        deposit = f'{deposit},00 €'
        area = f'{area} m²'
        persons = [person for person in persons.split(',') if person]
        person_count = str(len(persons))
        location_date = f'{location}, {contract_date}'

        input_file_path = os.path.join(PATH_PDF_TEMPLATES, 'rent_contract.pdf')

        document = fitz.open(input_file_path)

        arial = 'Arial'
        arial_bold = 'ArialBold'

        path_calibri = os.path.join(PATH_FONTS, f'{arial}.ttf')
        path_calibri_bold = os.path.join(PATH_FONTS, f'{arial_bold}.ttf')

        arial_data = {'fontfile': path_calibri, 'fontname': arial}
        arial_bold_data = {'fontfile': path_calibri_bold, 'fontname': arial_bold}

        # The next four rows are for inserting text with both bold and normal font styles.
        address_floor = f'<b>{address}</b>, {floor}'  # HTML fragment with 'address' and 'floor'.
        css = '* {font-family: sans-serif;font-size:10px;}'  # CSS font style.
        rect = (243, 416.7, 1000, 500)  # Rectangle for text.

        self._write_contract_data_with_html(pdf_document=document, page=0, text=address_floor, css=css, rect=rect)

        contract_data = [
            {'page': 0, 'text': landlord, 'fontdata': arial_data, 'fontsize': 10, 'x': 260, 'y': 229},
            {'page': 0, 'text': renter, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 200, 'y': 312.5},
            {'page': 0, 'text': resident, 'fontdata': arial_data, 'fontsize': 10, 'x': 170, 'y': 336.5},
            {'page': 0, 'text': passport, 'fontdata': arial_data, 'fontsize': 10, 'x': 170, 'y': 349},
            {'page': 0, 'text': date_of_expiry, 'fontdata': arial_data, 'fontsize': 10, 'x': 170, 'y': 361},
            {'page': 0, 'text': rooms, 'fontdata': arial_data, 'fontsize': 10, 'x': 173, 'y': 439},
            {'page': 0, 'text': balcony, 'fontdata': arial_data, 'fontsize': 10, 'x': 380, 'y': 439},
            {'page': 0, 'text': area, 'fontdata': arial_data, 'fontsize': 10, 'x': 327, 'y': 451},
            {'page': 0, 'text': start_date, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 344, 'y': 536.5},
            {'page': 0, 'text': stop_date, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 422, 'y': 536.5},
            {'page': 0, 'text': renter, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 130, 'y': 664.5},
            {'page': 0, 'text': iban, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 102, 'y': 676},
            {'page': 0, 'text': bic, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 95, 'y': 688},
            {'page': 0, 'text': credit_institution, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 140, 'y': 700.1},
            {'page': 0, 'text': purpose, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 110, 'y': 711.5},
            {'page': 0, 'text': monthly_rent, 'fontdata': arial_data, 'fontsize': 10, 'x': 380, 'y': 765},
            {'page': 0, 'text': extra_costs, 'fontdata': arial_data, 'fontsize': 10, 'x': 380, 'y': 787},
            {'page': 0, 'text': rent_cost, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 380, 'y': 810},
            {'page': 1, 'text': deposit, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 460, 'y': 233.5},
            {'page': 2, 'text': location_date, 'fontdata': arial_data, 'fontsize': 10, 'x': 71, 'y': 772.5},
            {'page': 2, 'text': person_count, 'fontdata': arial_data, 'fontsize': 10, 'x': 195, 'y': 163.5}
        ]
        person_data = self._get_person_position(fontdata=arial_bold_data, persons=persons)

        contract_data.extend(person_data)

        return self._write_contract_data(pdf_document=document, contract_data=contract_data)

    # Maklervertrag Verkauf contract.
    def sale_contract(self, contracts_info: dict) -> bytes:
        customer = contracts_info.get('customer')
        object = contracts_info.get('object')
        land_register = contracts_info.get('land_register')
        length_of_time = contracts_info.get('length_of_time')
        address = contracts_info.get('address')
        position = contracts_info.get('position')
        location = contracts_info.get('location')
        contract_date = contracts_info.get('contract_date').strftime('%d.%m.%Y')

        location_date = f'{location}, {contract_date}'

        customer_text = self._split_description_text(text=customer, length=45, max_length=100)
        object = self._split_description_text(text=object, length=45, max_length=140)
        land_register = self._split_description_text(text=land_register, length=45, max_length=100)
        position = self._split_description_text(text=position, length=45, max_length=80)

        input_file_path = os.path.join(PATH_PDF_TEMPLATES, 'sale_contract.pdf')

        document = fitz.open(input_file_path)

        minion_pro = 'MinionPro'
        minion_pro_bold = 'MinionPro'

        path_minion_pro = os.path.join(PATH_FONTS, f'{minion_pro}.ttf')
        path_minion_pro_bold = os.path.join(PATH_FONTS, f'{minion_pro_bold}.ttf')

        minion_pro_data = {'fontfile': path_minion_pro, 'fontname': minion_pro}
        minion_pro_bold_data = {'fontfile': path_minion_pro_bold, 'fontname': minion_pro_bold}

        contract_data = [
            {'page': 4, 'text': customer, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 235, 'y': 132},
            {'page': 3, 'text': location_date, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 50, 'y': 782},
            {'page': 3, 'text': location_date, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 308, 'y': 782},
            {'page': 4, 'text': location_date, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 141, 'y': 805},
            {'page': 3, 'text': length_of_time, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 272, 'y': 139},
            {'page': 3, 'text': length_of_time, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 322, 'y': 153.5},
            {'page': 4, 'text': address, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 235, 'y': 162},
        ]

        # Customer.
        customer_data = []
        row = 244
        for text in customer_text:
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 61, 'y': row}
            )
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 315, 'y': row}
            )
            row += 14

        # Object.
        object_data = []
        row = 547
        for text in object:
            object_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 61, 'y': row}
            )
            object_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 315, 'y': row}
            )
            row += 14

        # Land register.
        land_register_data = []
        row = 677
        for text in land_register:
            land_register_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 61, 'y': row}
            )
            land_register_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 314, 'y': row}
            )
            row += 14

        # Building position
        position_data = []
        row = 245
        for text in position:
            position_data.append(
                {'page': 4, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_data, 'x': 233, 'y': row}
            )
            row += 29

        contract_data.extend(customer_data)
        contract_data.extend(object_data)
        contract_data.extend(land_register_data)
        contract_data.extend(position_data)

        return self._write_contract_data(pdf_document=document, contract_data=contract_data)

    # Makler Suchauftrag Vorlage contract.
    def broker_search(self, contracts_info: dict) -> bytes:
        customer = contracts_info.get('customer')
        location = contracts_info.get('location')
        contract_date = contracts_info.get('contract_date').strftime('%d.%m.%Y')

        customer = self._split_description_text(text=customer, length=40, max_length=100)

        location_date = f'{location}, {contract_date}'

        input_file_path = os.path.join(PATH_PDF_TEMPLATES, 'broker_search.pdf')

        document = fitz.open(input_file_path)

        calibri = 'Calibri'

        path_calibri = os.path.join(PATH_FONTS, f'{calibri}.ttf')

        calibri_data = {'fontfile': path_calibri, 'fontname': calibri}

        contract_data = [
            {'page': 5, 'text': location_date, 'fontdata': calibri_data, 'fontsize': 12, 'x': 51, 'y': 671},
            {'page': 5, 'text': location_date, 'fontdata': calibri_data, 'fontsize': 12, 'x': 308, 'y': 671}
        ]

        customer_data = []
        row = 260
        for text in customer:
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': calibri_data, 'x': 58, 'y': row}
            )
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': calibri_data, 'x': 300, 'y': row}
            )
            row += 14

        contract_data.extend(customer_data)

        return self._write_contract_data(pdf_document=document, contract_data=contract_data)

    # Mietersuche Vertrag contract.
    def search_contract(self, contracts_info: dict):
        customer = contracts_info.get('customer')
        address = contracts_info.get('address')
        floor = contracts_info.get('floor')
        rooms = contracts_info.get('rooms')
        balcony = contracts_info.get('balcony')
        address_customer = contracts_info.get('address_customer')
        area = contracts_info.get('area')
        deposit = contracts_info.get('deposit')
        purchase_contract = contracts_info.get('purchase_contract')
        land_register = contracts_info.get('land_register')

        customer = self._split_description_text(text=customer, length=40, max_length=100)

        address_floor = f'{address}, {floor}'

        area_de = f'{area} m²'
        area_ru = f'{area} м²'

        deposit_de = f'{deposit} € pro Monat.'
        deposit_ru = f'{deposit} € в месяц.'

        input_file_path = os.path.join(PATH_PDF_TEMPLATES, 'search_contract.pdf')

        document = fitz.open(input_file_path)

        tnr = 'TimesNewRoman'
        tnr_bold = 'TimesNewRomanBolt'

        path_tnr = os.path.join(PATH_FONTS, f'{tnr}.ttf')
        path_tnr_bold = os.path.join(PATH_FONTS, f'{tnr_bold}.ttf')

        tnr_data = {'fontfile': path_tnr, 'fontname': tnr}
        tnr_bold_data = {'fontfile': path_tnr_bold, 'fontname': tnr_bold}

        contract_data = [
            {'page': 0, 'text': address_customer, 'fontdata': tnr_data, 'fontsize': 10, 'x': 82, 'y': 244.5},
            {'page': 0, 'text': address_customer, 'fontdata': tnr_data, 'fontsize': 10, 'x': 360, 'y': 245},
            {'page': 0, 'text': address_floor, 'fontdata': tnr_data, 'fontsize': 10, 'x': 72, 'y': 426},
            {'page': 0, 'text': address_floor, 'fontdata': tnr_data, 'fontsize': 10, 'x': 329, 'y': 465},
            {'page': 0, 'text': rooms, 'fontdata': tnr_data, 'fontsize': 10, 'x': 132, 'y': 435.5},
            {'page': 0, 'text': rooms, 'fontdata': tnr_data, 'fontsize': 10, 'x': 329, 'y': 425.5},
            {'page': 0, 'text': balcony, 'fontdata': tnr_data, 'fontsize': 10, 'x': 76, 'y': 455.5},
            {'page': 0, 'text': balcony, 'fontdata': tnr_data, 'fontsize': 10, 'x': 467, 'y': 435.5},
            {'page': 0, 'text': area_de, 'fontdata': tnr_data, 'fontsize': 10, 'x': 87, 'y': 475.5},
            {'page': 0, 'text': area_ru, 'fontdata': tnr_data, 'fontsize': 10, 'x': 402, 'y': 475.5},
            {'page': 0, 'text': deposit_de, 'fontdata': tnr_data, 'fontsize': 10, 'x': 116, 'y': 505.5},
            {'page': 0, 'text': deposit_ru, 'fontdata': tnr_data, 'fontsize': 10, 'x': 422, 'y': 505.5},
            {'page': 0, 'text': purchase_contract, 'fontdata': tnr_data, 'fontsize': 10, 'x': 50, 'y': 664.5},
            {'page': 0, 'text': purchase_contract, 'fontdata': tnr_data, 'fontsize': 10, 'x': 308, 'y': 665.5},
            {'page': 0, 'text': land_register, 'fontdata': tnr_data, 'fontsize': 10, 'x': 50, 'y': 694.5},
            {'page': 0, 'text': land_register, 'fontdata': tnr_data, 'fontsize': 10, 'x': 308, 'y': 695.5},
            {'page': 1, 'text': deposit_de, 'fontdata': tnr_data, 'fontsize': 10, 'x': 68, 'y': 621},
            {'page': 1, 'text': deposit_ru, 'fontdata': tnr_data, 'fontsize': 10, 'x': 438, 'y': 620.5}
        ]

        customer_data = []
        row = 214.5
        for text in customer:
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 10, 'fontdata': tnr_data, 'x': 72, 'y': row}
            )
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 10, 'fontdata': tnr_data, 'x': 320, 'y': row}
            )
            row += 11

        contract_data.extend(customer_data)

        return self._write_contract_data(pdf_document=document, contract_data=contract_data)
