from django.contrib import admin
from .models import School, SchoolMember, Campaign


class SchoolMemberInline(admin.TabularInline):
    model = SchoolMember
    extra = 1


class CampaignInline(admin.TabularInline):
    model = Campaign
    extra = 0


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'school_type', 'is_verified', 'min_quorum', 'created_at')
    list_filter = ('school_type', 'is_verified', 'state')
    search_fields = ('name', 'city', 'inep_code')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SchoolMemberInline, CampaignInline]


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'start_date', 'end_date', 'is_active', 'min_quorum')
    list_filter = ('is_active', 'school')
    search_fields = ('title', 'school__name')


@admin.register(SchoolMember)
class SchoolMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'role', 'is_primary_contact', 'created_at')
    list_filter = ('role', 'is_primary_contact')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'school__name')
