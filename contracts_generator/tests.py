from datetime import date

import fitz
from django.test import SimpleTestCase

from contracts_generator.forms import (
    WGBestaetigungAdminForm,
    WohnungsuebergabeProtokollArendaAdminForm,
)
from contracts_generator.pdf_utils import PDFWriter


class SaleAllContractPdfTests(SimpleTestCase):
    def test_clause_five_and_shifted_dynamic_fields(self):
        pdf = PDFWriter().sale_contract(
            {
                'customer': 'Maximilian Alexander Mustermann, Musterstraße 123, 10115 Berlin',
                'object': 'Wohnung mit Stellplatz, Beispielstraße 125, 10707 Berlin',
                'land_register': 'Berlin-Wilmersdorf, Blatt 123456',
                'length_of_time': 12,
                'address': 'Musterstraße 123, 10115 Berlin',
                'location': 'Berlin',
                'contract_date': date(2026, 7, 15),
            },
            template_filename='sale_all_contract.pdf',
        )

        document = fitz.open(stream=pdf, filetype='pdf')
        self.assertEqual(len(document), 7)

        duties_text = document[3].get_text()
        self.assertIn('Findet sich ein konkreter Käufer', duties_text)
        self.assertIn('В случае наличия конкретного покупателя', duties_text)

        duties_text = document[3].get_text()
        self.assertIn('Vertragsdauer und Kündigung', duties_text)
        self.assertIn('Срок действия договора и расторжения', duties_text)
        self.assertIn('12', duties_text)

        section_two_blocks = document[2].get_text('blocks')
        de_subitem_two = next(b for b in section_two_blocks if '2. Alle Tatsachen' in b[4])
        ru_subitem_two = next(b for b in section_two_blocks if '2. Все факты' in b[4])
        self.assertAlmostEqual(de_subitem_two[1], ru_subitem_two[1], delta=1)

        page_four_blocks = document[3].get_text('blocks')
        clause_five = next(b for b in page_four_blocks if '5. Findet sich' in b[4])
        section_four = next(b for b in page_four_blocks if '4. Vertragsdauer' in b[4])
        self.assertLess(section_four[1] - clause_five[3], 20)

        terms_text = document[4].get_text()
        self.assertIn('Vertragssprache und geltendes Recht', terms_text)
        self.assertIn('Легитимность', terms_text)
        self.assertIn('Berlin, 15.07.2026', terms_text)
        self.assertNotIn('Musterstraße 123', terms_text)

        power_text = document[5].get_text()
        self.assertIn('Musterstraße 123', power_text)
        self.assertIn('Wohnung mit Stellplatz', power_text)
        document.close()


class WGBestaetigungTests(SimpleTestCase):
    form_data = {
        'provider_name': 'Max Mustermann GmbH',
        'provider_street': 'Lange Musterstraße 123',
        'provider_postal_code': '10115',
        'provider_city': 'Berlin',
        'owner_name': 'Erika Mustermann',
        'owner_street': 'Eigentümerstraße 7',
        'owner_postal_code': '10707',
        'owner_city': 'Berlin',
        'move_type': 'EINZUG',
        'move_date': '2026-07-15',
        'apartment_street': 'Wohnungsstraße 42',
        'apartment_additional': 'Wohnung 12, 3. OG rechts',
        'apartment_postal_code': '10999',
        'apartment_city': 'Berlin',
        'person_1_family_name': 'Mustermann',
        'person_1_first_name': 'Max',
        'person_2_family_name': 'Mustermann',
        'person_2_first_name': 'Anna',
    }

    def test_admin_form_collects_person_rows(self):
        form = WGBestaetigungAdminForm(data=self.form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data['persons'],
            [
                {'family_name': 'Mustermann', 'first_name': 'Max'},
                {'family_name': 'Mustermann', 'first_name': 'Anna'},
            ],
        )

    def test_pdf_contains_form_values(self):
        pdf = PDFWriter().wg_bestaetigung({
            **self.form_data,
            'move_date': date(2026, 7, 15),
            'persons': [
                {'family_name': 'Mustermann', 'first_name': 'Max'},
                {'family_name': 'Mustermann', 'first_name': 'Anna'},
            ],
        })
        document = fitz.open(stream=pdf, filetype='pdf')
        text = document[0].get_text().replace('\xa0', ' ')
        self.assertIn('Max Mustermann GmbH', text)
        self.assertIn('Wohnungsstraße 42', text)
        self.assertIn('15.07.2026', text)
        self.assertIn('Anna', text)
        document.close()


class WohnungsuebergabeProtokollArendaTests(SimpleTestCase):
    def test_form_and_generated_pdf(self):
        form_data = {
            'tenant_name': 'Max Mustermann',
            'apartment_address': 'Musterstraße 1, Berlin',
            'handover_date': '2026-07-15',
            'defect_status': 'DEFECTS',
            'landlord_date': '2026-07-15',
            'tenant_date': '2026-07-15',
            'room_1_ok': 'on',
            'room_2_defects': 'Kratzer an der Wand',
            'room_2_remarks': 'Foto 1',
        }
        form = WohnungsuebergabeProtokollArendaAdminForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.cleaned_data['inspection_rows'][0]['ok'])
        self.assertEqual(form.cleaned_data['inspection_rows'][1]['defects'], 'Kratzer an der Wand')

        pdf = PDFWriter().wohnungsuebergabe_protokoll_arenda(form.cleaned_data)
        document = fitz.open(stream=pdf, filetype='pdf')
        text = document[0].get_text().replace('\xa0', ' ')
        self.assertIn('Max Mustermann', text)
        self.assertIn('15.07.2026', text)
        self.assertIn('Kratzer an der Wand', text)
        self.assertIsNone(document[0].first_annot)
        document.close()
