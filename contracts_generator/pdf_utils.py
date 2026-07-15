import io
import os

import fitz
from fitz import Rect

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

    def _insert_fitted_text(self, page, text, rect, fontfile, fontname, max_size=9, min_size=6):
        """Insert one line of text, reducing its size until it fits the given field."""
        text = str(text or '').strip()
        if not text:
            return

        page.insert_font(fontname=fontname, fontfile=fontfile)
        font = fitz.Font(fontfile=fontfile)
        fontsize = max_size
        while fontsize >= min_size:
            width = font.text_length(text, fontsize=fontsize)
            if width <= rect.width:
                page.insert_text(
                    fitz.Point(rect.x0, rect.y1 - 1),
                    text,
                    fontname=fontname,
                    fontfile=fontfile,
                    fontsize=fontsize,
                )
                return
            fontsize -= 0.5

        page.insert_textbox(
            rect,
            text,
            fontname=fontname,
            fontfile=fontfile,
            fontsize=min_size,
            lineheight=1,
        )

    def _insert_fitted_box(self, page, text, rect, fontfile, fontname, max_size=7, min_size=5):
        """Insert potentially multiline text into a compact form cell."""
        text = str(text or '').strip()
        if not text:
            return
        page.insert_font(fontname=fontname, fontfile=fontfile)
        fontsize = max_size
        while fontsize >= min_size:
            result = page.insert_textbox(
                rect,
                text,
                fontname=fontname,
                fontfile=fontfile,
                fontsize=fontsize,
                lineheight=1,
            )
            if result >= 0:
                return
            fontsize -= 0.5

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
        kitchen = contracts_info.get('kitchen')
        corridor = contracts_info.get('corridor')
        bathroom = contracts_info.get('bathroom')
        balcony = contracts_info.get('balcony')
        utility_room = contracts_info.get('utility_room')
        area = contracts_info.get('area')
        furniture = contracts_info.get('furniture')
        start_date = contracts_info.get('start_date').strftime('%d.%m.%Y')
        stop_date = contracts_info.get('stop_date').strftime('%d.%m.%Y')
        rent_stop_date = contracts_info.get('rent_stop_date').strftime('%d.%m.%Y')
        recipient = contracts_info.get('recipient')
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

        rent_cost = f'{int(monthly_rent) + int(extra_costs)},00 €'
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
        address_floor = f'<b>{address}, {floor}</b>'  # HTML fragment with 'address' and 'floor'.
        css = '* {font-family: sans-serif;font-size:10px;}'  # CSS font style.
        rect = (243, 386, 1000, 500)  # Rectangle for text.

        self._write_contract_data_with_html(pdf_document=document, page=0, text=address_floor, css=css, rect=rect)

        contract_data = [
            {'page': 0, 'text': landlord, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 260, 'y': 202},
            {'page': 0, 'text': renter, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 200, 'y': 284.5},
            {'page': 0, 'text': resident, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 170, 'y': 308.5},
            {'page': 0, 'text': passport, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 170, 'y': 321},
            {'page': 0, 'text': date_of_expiry, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 170, 'y': 333},
            {'page': 0, 'text': rooms, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 174, 'y': 408},
            {'page': 0, 'text': kitchen, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 229, 'y': 408},
            {'page': 0, 'text': corridor, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 275, 'y': 408},
            {'page': 0, 'text': balcony, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 329, 'y': 408},
            {'page': 0, 'text': bathroom, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 378, 'y': 408},
            {'page': 0, 'text': utility_room, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 75, 'y': 420.5},
            {'page': 0, 'text': area, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 327, 'y': 420.5},
            {'page': 0, 'text': furniture, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 419, 'y': 420.5},
            {'page': 0, 'text': landlord, 'fontdata': arial_data, 'fontsize': 10, 'x': 280, 'y': 494},
            {'page': 0, 'text': start_date, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 186, 'y': 518},
            {'page': 0, 'text': stop_date, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 261, 'y': 518},
            {'page': 0, 'text': rent_stop_date, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 71, 'y': 576.5},
            {'page': 0, 'text': recipient, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 130, 'y': 635.5},
            {'page': 0, 'text': iban, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 102, 'y': 647.5},
            {'page': 0, 'text': bic, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 95, 'y': 659},
            {'page': 0, 'text': credit_institution, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 140, 'y': 671},
            {'page': 0, 'text': purpose, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 110, 'y': 682.5},
            {'page': 0, 'text': monthly_rent, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 380, 'y': 737},
            {'page': 0, 'text': extra_costs, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 380, 'y': 759},
            {'page': 0, 'text': rent_cost, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 380, 'y': 782},
            {'page': 1, 'text': deposit, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 460, 'y': 234},
            {'page': 2, 'text': location_date, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 71, 'y': 772.5},
            {'page': 2, 'text': person_count, 'fontdata': arial_bold_data, 'fontsize': 10, 'x': 195, 'y': 163.5}
        ]
        person_data = self._get_person_position(fontdata=arial_bold_data, persons=persons)

        contract_data.extend(person_data)

        return self._write_contract_data(pdf_document=document, contract_data=contract_data)

    # Maklervertrag Verkauf contract.
    def sale_contract(self, contracts_info: dict, template_filename: str = 'sale_contract.pdf') -> bytes:
        customer = contracts_info.get('customer')
        object_address = contracts_info.get('object')
        land_register = contracts_info.get('land_register')
        length_of_time = contracts_info.get('length_of_time')
        address = contracts_info.get('address')
        location = contracts_info.get('location')
        contract_date = contracts_info.get('contract_date').strftime('%d.%m.%Y')

        location_date = f'{location}, {contract_date}'

        input_file_path = os.path.join(PATH_PDF_TEMPLATES, template_filename)

        document = fitz.open(input_file_path)

        minion_pro = 'MinionPro'
        minion_pro_bold = 'MinionProBold'

        path_minion_pro = os.path.join(PATH_FONTS, f'{minion_pro}.ttf')
        path_minion_pro_bold = os.path.join(PATH_FONTS, f'{minion_pro_bold}.otf')

        minion_pro_data = {'fontfile': path_minion_pro, 'fontname': minion_pro}
        minion_pro_bold_data = {'fontfile': path_minion_pro_bold, 'fontname': minion_pro_bold}

        # В шаблоне Alleinauftrag после добавления пункта 5 раздела
        # "Pflichten des Kunden / Обязанности Заказчика" раздел о сроке
        # договора вынесен на отдельную страницу. Из-за этого следующие
        # страницы приложения сдвинуты на одну позицию.
        is_alleinauftrag = template_filename == 'sale_all_contract.pdf'
        terms_page = 4 if is_alleinauftrag else 3
        power_page = 5 if is_alleinauftrag else 4

        if is_alleinauftrag:
            location_positions = [
                {'page': terms_page, 'x': 50, 'y': 345},
                {'page': terms_page, 'x': 308, 'y': 345},
                {'page': power_page, 'x': 141, 'y': 805},
            ]
            duration_positions = [
                {'page': 3, 'x': 272, 'y': 291},
                {'page': 3, 'x': 455, 'y': 291},
            ]
        else:
            location_positions = [
                {'page': 3, 'x': 50, 'y': 782},
                {'page': 3, 'x': 308, 'y': 782},
                {'page': 4, 'x': 141, 'y': 805},
            ]
            duration_positions = [
                {'page': 3, 'x': 272, 'y': 177.5},
                {'page': 3, 'x': 319, 'y': 191.5},
            ]

        contract_data = [
            {'page': 0, 'text': address, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 61, 'y': 274},
            {'page': 0, 'text': address, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 315, 'y': 274},
            {'page': power_page, 'text': address, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 235, 'y': 162},
        ]

        contract_data.extend(
            {'page': p['page'], 'text': location_date, 'fontsize': 12,
             'fontdata': minion_pro_bold_data, 'x': p['x'], 'y': p['y']}
            for p in location_positions
        )
        contract_data.extend(
            {'page': p['page'], 'text': length_of_time, 'fontsize': 12,
             'fontdata': minion_pro_bold_data, 'x': p['x'], 'y': p['y']}
            for p in duration_positions
        )

        customer = self._split_description_text(text=customer, length=45, max_length=100)
        object_address = self._split_description_text(text=object_address, length=45, max_length=140)
        land_register = self._split_description_text(text=land_register, length=45, max_length=100)

        # Customer.
        customer_data = []
        row_page_0 = 244
        row_page_4 = 132
        for text in customer:
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 61, 'y': row_page_0}
            )
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 315, 'y': row_page_0}
            )
            customer_data.append(
                {'page': power_page, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 235, 'y': row_page_4},
            )
            row_page_0 += 14
            row_page_4 += 14

        # Object.
        object_data = []
        row_page_0 = 547
        row_page_4 = 245
        for text in object_address:
            object_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 61, 'y': row_page_0}
            )
            object_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 315, 'y': row_page_0}
            )
            object_data.append(
                {'page': power_page, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 233, 'y': row_page_4}
            )
            row_page_0 += 14
            row_page_4 += 30

        # Land register.
        land_register_data = []
        row = 677
        for text in land_register:
            land_register_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 61, 'y': row}
            )
            land_register_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': minion_pro_bold_data, 'x': 314, 'y': row}
            )
            row += 14

        contract_data.extend(customer_data)
        contract_data.extend(object_data)
        contract_data.extend(land_register_data)

        return self._write_contract_data(pdf_document=document, contract_data=contract_data)

    # Wohnungsgeberbestätigung.
    def wg_bestaetigung(self, contracts_info: dict) -> bytes:
        input_file_path = os.path.join(PATH_PDF_TEMPLATES, 'WG_bestaetigung.pdf')
        document = fitz.open(input_file_path)
        page = document[0]

        fontname = 'Arial'
        fontfile = os.path.join(PATH_FONTS, f'{fontname}.ttf')

        fields = (
            ('provider_name', Rect(50, 97, 445, 109)),
            ('provider_street', Rect(50, 120, 445, 132)),
            ('provider_postal_code', Rect(50, 143, 126, 155)),
            ('provider_city', Rect(145, 143, 445, 155)),
            ('owner_name', Rect(50, 210, 445, 222)),
            ('owner_street', Rect(50, 233, 445, 245)),
            ('owner_postal_code', Rect(50, 256, 126, 268)),
            ('owner_city', Rect(145, 256, 445, 268)),
            ('apartment_street', Rect(50, 343, 445, 355)),
            ('apartment_additional', Rect(50, 367, 445, 379)),
            ('apartment_postal_code', Rect(50, 391, 126, 403)),
            ('apartment_city', Rect(145, 391, 445, 403)),
        )
        for field_name, rect in fields:
            self._insert_fitted_text(
                page, contracts_info.get(field_name), rect, fontfile, fontname,
            )

        move_date = contracts_info.get('move_date')
        if move_date:
            self._insert_fitted_text(
                page,
                move_date.strftime('%d.%m.%Y'),
                Rect(392, 287, 445, 300),
                fontfile,
                fontname,
                max_size=8,
            )

        checkbox_x = 126 if contracts_info.get('move_type') == 'EINZUG' else 186
        page.insert_font(fontname=fontname, fontfile=fontfile)
        page.insert_text(
            fitz.Point(checkbox_x, 300),
            'X',
            fontname=fontname,
            fontfile=fontfile,
            fontsize=8,
        )

        for row, person in enumerate((contracts_info.get('persons') or [])[:10]):
            top = 461 + (row * 17.5)
            self._insert_fitted_text(
                page,
                person.get('family_name'),
                Rect(50, top, 250, top + 12),
                fontfile,
                fontname,
                max_size=8,
            )
            self._insert_fitted_text(
                page,
                person.get('first_name'),
                Rect(270, top, 445, top + 12),
                fontfile,
                fontname,
                max_size=8,
            )

        pdf_bytes = io.BytesIO()
        document.save(pdf_bytes)
        document.close()
        return pdf_bytes.getvalue()

    # Wohnungsübergabe-Protokoll ARENDA.
    def wohnungsuebergabe_protokoll_arenda(self, contracts_info: dict) -> bytes:
        input_file_path = os.path.join(PATH_PDF_TEMPLATES, 'Wohnungsuebergabe_Protokoll_ARENDA.pdf')
        document = fitz.open(input_file_path)
        page = document[0]

        # The source file contains yellow markup explaining which areas are editable.
        # It is useful as a specification, but must not appear in the generated protocol.
        while page.first_annot:
            page.delete_annot(page.first_annot)

        fontname = 'Arial'
        fontfile = os.path.join(PATH_FONTS, f'{fontname}.ttf')
        page.insert_font(fontname=fontname, fontfile=fontfile)

        fields = (
            ('tenant_name', Rect(72, 72, 548, 83)),
            ('apartment_address', Rect(190, 108, 548, 118)),
            ('electricity_meter_number', Rect(262, 456, 376, 466)),
            ('electricity_reading', Rect(424, 456, 541, 466)),
            ('gas_meter_number', Rect(262, 503, 376, 513)),
            ('gas_reading', Rect(424, 503, 541, 513)),
            ('water_meter_number_1', Rect(262, 549, 378, 559)),
            ('water_reading_1', Rect(424, 549, 541, 559)),
            ('water_meter_number_2', Rect(262, 572, 378, 582)),
            ('water_reading_2', Rect(424, 572, 541, 582)),
            ('keys_handed_over', Rect(307, 608, 554, 620)),
            ('keys_pending', Rect(268, 630, 554, 642)),
            ('notes', Rect(218, 653, 551, 665)),
        )
        for field_name, rect in fields:
            self._insert_fitted_text(page, contracts_info.get(field_name), rect, fontfile, fontname, max_size=8)

        date_fields = (
            ('handover_date', Rect(232, 151, 298, 161)),
            ('landlord_date', Rect(105, 686, 195, 697)),
            ('tenant_date', Rect(105, 719, 195, 729)),
        )
        for field_name, rect in date_fields:
            value = contracts_info.get(field_name)
            if value:
                self._insert_fitted_text(
                    page, value.strftime('%d.%m.%Y'), rect, fontfile, fontname, max_size=8,
                )

        status_x = 354 if contracts_info.get('defect_status') == 'NONE' else 411
        page.insert_text(
            fitz.Point(status_x, 162), 'X', fontname=fontname, fontfile=fontfile, fontsize=7,
        )

        room_checkbox_baselines = (
            219.05, 243.55, 268.05, 292.60, 309.90,
            334.40, 358.85, 383.35, 407.85, 432.35,
        )
        for row, item in enumerate((contracts_info.get('inspection_rows') or [])[:10]):
            top = 201 + (row * 23.5)
            if item.get('ok'):
                page.insert_text(
                    fitz.Point(166.2, room_checkbox_baselines[row]), 'X',
                    fontname=fontname, fontfile=fontfile, fontsize=7,
                )
            self._insert_fitted_box(
                page, item.get('defects'), Rect(208, top + 2, 411, top + 22),
                fontfile, fontname,
            )
            self._insert_fitted_box(
                page, item.get('remarks'), Rect(415, top + 2, 551, top + 22),
                fontfile, fontname,
            )

        pdf_bytes = io.BytesIO()
        document.save(pdf_bytes)
        document.close()
        return pdf_bytes.getvalue()

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
        calibri_bold = 'CalibriBold'

        path_calibri = os.path.join(PATH_FONTS, f'{calibri}.ttf')
        path_calibri_bold = os.path.join(PATH_FONTS, f'{calibri_bold}.ttf')

        calibri_data = {'fontfile': path_calibri, 'fontname': calibri}
        calibri_bold_data = {'fontfile': path_calibri_bold, 'fontname': calibri_bold}

        contract_data = [
            {'page': 5, 'text': location_date, 'fontdata': calibri_bold_data, 'fontsize': 12, 'x': 51, 'y': 671},
            {'page': 5, 'text': location_date, 'fontdata': calibri_bold_data, 'fontsize': 12, 'x': 308, 'y': 671}
        ]

        customer_data = []
        row = 260
        for text in customer:
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': calibri_bold_data, 'x': 58, 'y': row}
            )
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 12, 'fontdata': calibri_bold_data, 'x': 300, 'y': row}
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
        corridor = contracts_info.get('corridor')
        balcony = contracts_info.get('balcony')
        bathroom = contracts_info.get('bathroom')
        # utility_room = contracts_info.get('utility_room')
        furniture = contracts_info.get('furniture')
        address_customer = contracts_info.get('address_customer')
        area = contracts_info.get('area')
        deposit = contracts_info.get('deposit')
        purchase_contract = contracts_info.get('purchase_contract')
        land_register = contracts_info.get('land_register')

        customer = self._split_description_text(text=customer, length=40, max_length=100)

        address_floor = f'{address}, {floor}'

        furniture_de, furniture_ru = furniture.split('$')

        area_de = f'{area} m²'
        area_ru = f'{area} м²'

        deposit_de = f'{deposit} €'
        deposit_ru = f'{deposit} €'

        input_file_path = os.path.join(PATH_PDF_TEMPLATES, 'search_contract.pdf')

        document = fitz.open(input_file_path)

        tnr = 'TimesNewRoman'
        tnr_bold = 'TimesNewRomanBold'

        path_tnr = os.path.join(PATH_FONTS, f'{tnr}.ttf')
        path_tnr_bold = os.path.join(PATH_FONTS, f'{tnr_bold}.ttf')

        tnr_data = {'fontfile': path_tnr, 'fontname': tnr}
        tnr_bold_data = {'fontfile': path_tnr_bold, 'fontname': tnr_bold}

        css = '* {font-family: sans;font-size:9px;}'

        furniture_ru = f'<b>{furniture_ru}</b> в доме'
        rect = (371, 446, 1000, 500)
        self._write_contract_data_with_html(pdf_document=document, page=0, text=furniture_ru, css=css, rect=rect)

        deposit_de = f'<b>{deposit_de}</b> pro Monat.'
        rect = (113, 495.5, 1000, 600)
        self._write_contract_data_with_html(pdf_document=document, page=0, text=deposit_de, css=css, rect=rect)
        rect = (65, 612, 1000, 650)
        self._write_contract_data_with_html(pdf_document=document, page=1, text=deposit_de, css=css, rect=rect)

        deposit_ru = f'<b>{deposit_ru}</b> в месяц.'
        rect = (422, 495.5, 1000, 600)
        self._write_contract_data_with_html(pdf_document=document, page=0, text=deposit_ru, css=css, rect=rect)
        rect = (438, 612, 1000, 650)
        self._write_contract_data_with_html(pdf_document=document, page=1, text=deposit_ru, css=css, rect=rect)

        contract_data = [
            {'page': 0, 'text': address_customer, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 92, 'y': 255},
            {'page': 0, 'text': address_customer, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 410, 'y': 255},
            {'page': 0, 'text': address_floor, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 72, 'y': 435},
            {'page': 0, 'text': address_floor, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 329, 'y': 465},
            {'page': 0, 'text': rooms, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 138, 'y': 445},
            {'page': 0, 'text': rooms, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 334, 'y': 435},
            {'page': 0, 'text': corridor, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 134, 'y': 455},
            {'page': 0, 'text': corridor, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 334, 'y': 445},
            {'page': 0, 'text': bathroom, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 185, 'y': 455},
            {'page': 0, 'text': bathroom, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 385, 'y': 445},
            {'page': 0, 'text': balcony, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 77, 'y': 465},
            {'page': 0, 'text': balcony, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 467, 'y': 445},
            {'page': 0, 'text': furniture_de, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 120, 'y': 465},
            {'page': 0, 'text': area_de, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 160, 'y': 475},
            {'page': 0, 'text': area_ru, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 402, 'y': 475},
            {'page': 0, 'text': purchase_contract, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 50, 'y': 655},
            {'page': 0, 'text': purchase_contract, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 308, 'y': 655},
            {'page': 0, 'text': land_register, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 50, 'y': 685},
            {'page': 0, 'text': land_register, 'fontdata': tnr_bold_data, 'fontsize': 10, 'x': 308, 'y': 685},
        ]

        customer_data = []
        row = 235
        for text in customer:
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 10, 'fontdata': tnr_bold_data, 'x': 72, 'y': row}
            )
            customer_data.append(
                {'page': 0, 'text': text, 'fontsize': 10, 'fontdata': tnr_bold_data, 'x': 320, 'y': row}
            )
            row += 11

        contract_data.extend(customer_data)

        return self._write_contract_data(pdf_document=document, contract_data=contract_data)
