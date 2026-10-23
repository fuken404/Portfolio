from django.contrib import admin

from .models import Certification, ContactMessage, Education, Experience, Profile, Project, Skill


def lang_fieldsets(general, translatable):
    """Agrupa los campos en General / Español / English."""
    return [
        (None, {'fields': general}),
        ('Español', {'fields': [f'{f}_es' for f in translatable]}),
        ('English', {
            'fields': [f'{f}_en' for f in translatable],
            'description': 'Si un campo queda vacío, la página en inglés muestra el texto en español.',
        }),
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'role_es', 'available']
    fieldsets = lang_fieldsets(
        ['name', 'location', 'email', 'github', 'linkedin', 'available'],
        ['role', 'tagline', 'bio', 'focus', 'languages'],
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name_es', 'name_en', 'category', 'level', 'is_core', 'show_in_stack', 'order']
    list_editable = ['level', 'is_core', 'show_in_stack', 'order']
    list_filter = ['category', 'is_core', 'show_in_stack']
    prepopulated_fields = {'slug': ['name_es']}
    search_fields = ['name_es', 'name_en']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title_es', 'year', 'featured', 'order']
    list_editable = ['featured', 'order']
    prepopulated_fields = {'slug': ['title_es']}
    filter_horizontal = ['skills']
    fieldsets = lang_fieldsets(
        ['slug', 'year', 'skills', 'repo_url', 'live_url', 'image', 'featured', 'order'],
        ['title', 'summary', 'description'],
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position_es', 'company', 'start', 'end']
    fieldsets = lang_fieldsets(
        ['company', 'start', 'end'],
        ['position', 'location', 'description', 'highlights'],
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree_es', 'institution', 'start', 'end']
    fieldsets = lang_fieldsets(['institution', 'location', 'start', 'end'], ['degree'])


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name_es', 'issuer', 'category', 'issued']
    list_filter = ['category', 'issuer']
    search_fields = ['name_es', 'name_en', 'issuer']
    fieldsets = lang_fieldsets(
        ['issuer', 'category', 'issued', 'hours', 'credential_id', 'credential_url'],
        ['name'],
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'lang', 'created_at', 'read']
    list_filter = ['read', 'lang']
    readonly_fields = ['name', 'email', 'message', 'lang', 'created_at']
