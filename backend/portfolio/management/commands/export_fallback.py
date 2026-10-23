import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from portfolio.models import Certification, Education, Experience, Profile, Skill
from portfolio.serializers import (
    CertificationSerializer,
    EducationSerializer,
    ExperienceSerializer,
    ProfileSerializer,
    ProjectSerializer,
    SkillSerializer,
)
from portfolio.views import projects_queryset

OUTPUT = settings.BASE_DIR.parent / 'frontend' / 'src' / 'data' / 'fallback.json'


class Command(BaseCommand):
    # Ejecútalo contra la base de producción (o arma el JSON desde la API pública)
    # para que las URLs de certificados apunten a Blob Storage y no a /media local.
    help = 'Exporta el contenido (ES + EN) al respaldo local del frontend, con la misma forma que la API.'

    def handle(self, *args, **options):
        data = {}
        for lang, _ in settings.LANGUAGES:
            with translation.override(lang):
                data[lang] = {
                    'profile': ProfileSerializer(Profile.objects.first()).data,
                    'skills': SkillSerializer(Skill.objects.filter(show_in_stack=True), many=True).data,
                    'projects': ProjectSerializer(projects_queryset(), many=True).data,
                    'experience': ExperienceSerializer(Experience.objects.all(), many=True).data,
                    'education': EducationSerializer(Education.objects.all(), many=True).data,
                    'certifications': CertificationSerializer(Certification.objects.all(), many=True).data,
                }
        OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f'Respaldo escrito en {OUTPUT.relative_to(settings.BASE_DIR.parent)}'))
