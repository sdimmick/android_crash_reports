import os
import urlparse
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from dateutil import parser as dateparser
from models import CrashReport
from admin.models import Config, AccessToken
from pivotaltracker.api import PivotalApi

class NewCrashReportHandler(webapp2.RequestHandler):
    def post(self):
        if self.is_authorized(self.request):
            # Parse and save the crash report
            report = self.parse_crash_report(self.request)
            report.put()

            # Grab the app's base url
            url_info = urlparse.urlparse(self.request.url)
            base_url = url_info.scheme + '://' + url_info.netloc

            # Create a bug on Pivotal Tracker
            config = Config.get_app_config()
            project_id = config.pivotal_project_id
            auth_token = config.pivotal_auth_token
            pivotal_api = PivotalApi(project_id, auth_token)
            pivotal_api.createbug(report, base_url)

            # Return a response
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Report %d saved' % report.key.id())
        else:
            # No valid access token
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.set_status(401)
            self.response.write('Invalid access token')

    def is_authorized(self, request):
        # Check if there's a valid access token in the request
        custom_data = request.get('CUSTOM_DATA')
        if custom_data != None:
            # Custom data from ACRA is pretty weirdly formatted
            # e.g. 'accessToken = 390d904880974f369de5466c949cbaab 123 = abc'
            # Ugh. This is ugly.
            tokens = custom_data.rstrip('\n').replace(' = ', ' ').split(' ')
            params = {tokens[i*2]: tokens[i*2+1] for i in range(len(tokens) / 2)}
            return AccessToken.is_authorized(params['accessToken'])

    def parse_crash_report(self, request):
        report = CrashReport()

        report.android_version          = request.get('ANDROID_VERSION')
        report.app_version_code         = request.get('APP_VERSION_CODE')
        report.app_version_name         = request.get('APP_VERSION_NAME')
        report.available_mem_size       = request.get('AVAILABLE_MEM_SIZE')
        report.brand                    = request.get('BRAND')
        report.build                    = request.get('BUILD')
        report.crash_configuration      = request.get('CRASH_CONFIGURATION')
        report.device_features          = request.get('DEVICE_FEATURES')
        report.display                  = request.get('DISPLAY')
        report.environment              = request.get('ENVIRONMENT')
        report.file_path                = request.get('FILE_PATH')
        report.initial_configuration    = request.get('INITIAL_CONFIGURATION')
        report.installation_id          = request.get('INSTALLATION_ID')
        report.package_name             = request.get('PACKAGE_NAME')
        report.model                    = request.get('PHONE_MODEL')
        report.product                  = request.get('PRODUCT')
        report.report_id                = request.get('REPORT_ID')
        report.settings_secure          = request.get('SETTINGS_SECURE')
        report.settings_system          = request.get('SETTINGS_SYSTEM')
        report.shared_preferences       = request.get('SHARED_PREFERENCES')
        report.total_mem_size           = request.get('TOTAL_MEM_SIZE')

        # Coerce date strings into parseable format
        start_date = dateparser.parse(request.get('USER_APP_START_DATE'), ignoretz=True)
        crash_date = dateparser.parse(request.get('USER_CRASH_DATE'), ignoretz=True)
        report.user_app_start_date      = start_date
        report.user_crash_date          = crash_date

        # Parse stack trace / summary
        stack_trace = request.get('STACK_TRACE')
        report.stack_trace = stack_trace
        report.stack_summary = self.get_stack_summary(stack_trace, report.package_name)

        return report

    def get_stack_summary(self, stack_trace, package_name):
        lines = stack_trace.split('\n')
        summary = lines[0]
        
        for line in lines[1:]:
            if line.find(package_name) > 0:
                summary = summary + ' ' + line.strip('\t')
                break

        # Stack trace summary = first line + topmost occurance of package_name
        return summary

class CrashReportHandler(webapp2.RequestHandler):
    @login_required
    def get(self, report_id):
        report = CrashReport.get_by_id(long(report_id))

        template_values = {
            'report': report,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/crashreport.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/api/crashreport',        NewCrashReportHandler),
    ('/api/crashreport/(\d+)',  CrashReportHandler),
    ], debug=True)
