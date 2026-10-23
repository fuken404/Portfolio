from rest_framework import serializers

from .i18n import translated
from .models import Certification, ContactMessage, Education, Experience, Profile, Project, Skill


class TranslatedField(serializers.ReadOnlyField):
    """Expone `<campo>_<idioma>` como `<campo>`, según el idioma de la petición."""

    def __init__(self, **kwargs):
        super().__init__(source='*', **kwargs)

    def to_representation(self, obj):
        return translated(obj, self.field_name)


class ProfileSerializer(serializers.ModelSerializer):
    role = TranslatedField()
    tagline = TranslatedField()
    bio = TranslatedField()
    focus = TranslatedField()
    languages = TranslatedField()

    class Meta:
        model = Profile
        fields = ['name', 'role', 'tagline', 'bio', 'focus', 'languages', 'location',
                  'email', 'github', 'linkedin', 'available']


class SkillSerializer(serializers.ModelSerializer):
    name = TranslatedField()

    class Meta:
        model = Skill
        fields = ['id', 'name', 'slug', 'category', 'level', 'is_core']


class ProjectSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    summary = TranslatedField()
    description = TranslatedField()
    stack = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'summary', 'description', 'stack', 'year',
                  'repo_url', 'live_url', 'image', 'featured']

    def get_stack(self, obj):
        return [translated(skill, 'name') for skill in obj.skills.all()]


class ExperienceSerializer(serializers.ModelSerializer):
    position = TranslatedField()
    location = TranslatedField()
    description = TranslatedField()
    highlights = TranslatedField()

    class Meta:
        model = Experience
        fields = ['id', 'company', 'position', 'location', 'start', 'end', 'description', 'highlights']


class EducationSerializer(serializers.ModelSerializer):
    degree = TranslatedField()

    class Meta:
        model = Education
        fields = ['id', 'institution', 'degree', 'location', 'start', 'end']


class CertificationSerializer(serializers.ModelSerializer):
    name = TranslatedField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = ['id', 'name', 'issuer', 'category', 'issued', 'hours', 'credential_id',
                  'credential_url', 'file']

    def get_file(self, obj):
        # Ruta relativa (/media/...): en desarrollo Vite la redirige a Django.
        return obj.file.url if obj.file else ''


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
