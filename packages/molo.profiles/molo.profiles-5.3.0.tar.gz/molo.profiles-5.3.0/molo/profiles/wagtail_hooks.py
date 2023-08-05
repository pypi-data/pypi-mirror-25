from molo.profiles.admin import FrontendUsersModelAdmin
from molo.profiles.models import UserProfilesSettings
from wagtail.contrib.modeladmin.options import modeladmin_register
from wagtail.wagtailadmin.site_summary import SummaryItem
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Site


class ProfileWarningMessagee(SummaryItem):
    order = 100
    template = 'admin/profile_warning_message.html'


@hooks.register('construct_homepage_panels')
def profile_warning_message(request, panels):
    site = Site.objects.get(is_default_site=True)
    profile_settings = UserProfilesSettings.for_site(site)
    if not profile_settings.country_code and \
            profile_settings.show_mobile_number_field:
        panels[:] = [ProfileWarningMessagee(request)]


modeladmin_register(FrontendUsersModelAdmin)
