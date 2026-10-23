from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from portfolio.models import Certification

SOURCE = settings.BASE_DIR / 'content' / 'certificates'
EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.webp']


class Command(BaseCommand):
    help = (
        'Adjunta a cada certificación su archivo desde content/certificates/<categoría>/<slug>.<ext>. '
        'No toca el resto del contenido.'
    )

    def handle(self, *args, **options):
        attached, missing = [], []
        for cert in Certification.objects.all():
            source = next(
                (SOURCE / cert.category / f'{cert.slug}{ext}' for ext in EXTENSIONS
                 if (SOURCE / cert.category / f'{cert.slug}{ext}').exists()),
                None,
            )
            if source is None:
                missing.append(f'{cert.category}/{cert.slug}')
                continue
            if cert.file:
                cert.file.delete(save=False)
            with source.open('rb') as fh:
                cert.file.save(f'{cert.slug}{source.suffix}', File(fh), save=True)
            attached.append(cert.slug)

        self.stdout.write(self.style.SUCCESS(f'Adjuntados: {len(attached)}'))
        if missing:
            self.stdout.write(self.style.WARNING(
                'Sin archivo (agrégalo con ese nombre y vuelve a ejecutar):\n  '
                + '\n  '.join(missing)
            ))
