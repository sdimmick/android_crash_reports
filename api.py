import os
import urlparse
import webapp2
from dateutil import parser as dateparser
from models import CrashReport
from pivotaltracker.api import PivotalApi

pivotal_api = PivotalApi(os.environ['PIVOTAL_PROJECT_ID'], os.environ['PIVOTAL_AUTH_TOKEN'])

class CrashReportHandler(webapp2.RequestHandler):
    def post(self):
        report = CrashReport()

        report.android_version          = self.request.get('ANDROID_VERSION')
        report.app_version_code         = self.request.get('APP_VERSION_CODE')
        report.app_version_name         = self.request.get('APP_VERSION_NAME')
        report.available_mem_size       = self.request.get('AVAILABLE_MEM_SIZE')
        report.brand                    = self.request.get('BRAND')
        report.build                    = self.request.get('BUILD')
        report.crash_configuration      = self.request.get('CRASH_CONFIGURATION')
        report.device_features          = self.request.get('DEVICE_FEATURES')
        report.display                  = self.request.get('DISPLAY')
        report.environment              = self.request.get('ENVIRONMENT')
        report.file_path                = self.request.get('FILE_PATH')
        report.initial_configuration    = self.request.get('INITIAL_CONFIGURATION')
        report.installation_id          = self.request.get('INSTALLATION_ID')
        report.package_name             = self.request.get('PACKAGE_NAME')
        report.model                    = self.request.get('PHONE_MODEL')
        report.product                  = self.request.get('PRODUCT')
        report.report_id                = self.request.get('REPORT_ID')
        report.settings_secure          = self.request.get('SETTINGS_SECURE')
        report.settings_system          = self.request.get('SETTINGS_SYSTEM')
        report.shared_preferences       = self.request.get('SHARED_PREFERENCES')
        report.total_mem_size           = self.request.get('TOTAL_MEM_SIZE')

        start_date = dateparser.parse(self.request.get('USER_APP_START_DATE'), ignoretz=True)
        crash_date = dateparser.parse(self.request.get('USER_CRASH_DATE'), ignoretz=True)

        report.user_app_start_date      = start_date
        report.user_crash_date          = crash_date

        stack_trace = self.request.get('STACK_TRACE')
        report.stack_trace = stack_trace
        report.stack_summary = stack_trace.split('\n')[0]

        report.put()

        url_info = urlparse.urlparse(self.request.url)
        base_url = url_info.scheme + '://' + url_info.netloc
        print base_url
        pivotal_api.createbug(report, base_url)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('sweet')

    def get(self):
        print urlparse.urlparse(self.request.url)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, webapp2 World!')

application = webapp2.WSGIApplication([
    ('/api/crashreport', CrashReportHandler),
    ], debug=True)
