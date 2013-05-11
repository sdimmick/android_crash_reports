import os
import webapp2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models import CrashReport, CrashReportGroup
from utils.decorators import cached

webapp.template.register_template_library('crashreports.templatefilters')

class CrashReportListHandler(webapp2.RequestHandler):
    def get(self):
        # Build a dictionary of crash reports as {report.package_name: report}
        query = CrashReportGroup.query()
        pairs = query.map(lambda x: (x.package_name, x.report_count()))
        reports = {k: v for (k, v) in pairs}

        template_values = {
            'reports': reports,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/package_list.html')
        return self.response.write(template.render(path, template_values))

class CrashReporsForPackageHandler(webapp2.RequestHandler):
    def get(self, package_name):
        reports = CrashReport.for_package(package_name)

        template_values = {
            'reports': reports,
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/list.html')
        return self.response.write(template.render(path, template_values))

class CrashReportHandler(webapp2.RequestHandler):
    def get(self, package_name, report_id):
        group = CrashReportGroup.get_group(package_name)
        report = CrashReport.get_by_id(long(report_id), parent=group.key)

        template_values = {
            'report': report,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/crashreport.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/reports/all',                    CrashReportListHandler),
    ('/reports/package/(.*)/id/(\d+)',  CrashReportHandler),
    ('/reports/package/(.*)',           CrashReporsForPackageHandler),
    ], debug=True)
