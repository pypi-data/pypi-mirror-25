import csv
import io
import shutil
import tempfile
import zipfile

import requests
from django.core.management.base import BaseCommand

from ...models import PostalCode


class Command(BaseCommand):
    help = 'Updates postalcodes from latest GeoNames database for specified countries. Can be re-run as needed.'
    base_url = 'http://download.geonames.org/export/zip/%s.zip'
    fieldnames = (
        'country_code',
        'postal_code',
        'place_name',
        'admin_name1',
        'admin_code1',
        'admin_name2',
        'admin_code2',
        'admin_name3',
        'admin_code3',
        # ignore these fields:
        # 'latitude',
        # 'longitude',
        # 'accuracy',
    )
    delimiter = '\t'

    def add_arguments(self, parser):
        parser.add_argument('country', nargs='+', type=str)

    def handle(self, *args, **options):
        for country in options['country']:
            country = country.upper()
            url = self.base_url % country
            self.stdout.write('Downloading and extracting %s...' % url)
            response = requests.get(url)
            zipdata = zipfile.ZipFile(io.BytesIO(response.content))
            tmpdir = tempfile.mkdtemp()
            tmpfile = zipdata.extract('%s.txt' % country, path=tmpdir)
            self.stdout.write('Reading and updating postal codes...')
            seen_postal_codes = []
            for row in csv.DictReader(open(tmpfile), fieldnames=self.fieldnames, delimiter=self.delimiter):
                row.pop(None)  # remove extra fields (latitude, longitude, accuracy)
                if row['postal_code'] is None or row['postal_code'] in seen_postal_codes:
                    self.stdout.write('Skipping null or already-seen postal code "%s"' % row)
                    continue
                seen_postal_codes.append(row['postal_code'])
                postal_code, created = PostalCode.objects.get_or_create(
                    country_code=row.pop('country_code'),
                    postal_code=row.pop('postal_code'),
                    defaults=row,
                )
                if not created and any([getattr(postal_code, k) != v for k, v in row.items()]):
                    self.stdout.write('Postal code "%s" is out of date; updating.' % postal_code)
                    PostalCode.objects.filter(pk=postal_code.pk).update(**row)
            shutil.rmtree(tmpdir)
            self.stdout.write('Successfully updated postal codes for %s' % country)
