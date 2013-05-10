import os
import webapp2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models import CrashReport

webapp.template.register_template_library('crashreports.templatefilters')

class CrashReportListHandler(webapp2.RequestHandler):
    def get(self):
        # Build a dictionary of crash reports as {report.package_name: report}
        query = CrashReport.query()
        reports = {}
        for k, v in query.map(lambda x: (x.package_name, x)):
            if reports.has_key(k):
                reports[k].append(v)
            else:
                reports[k] = [v]

        template_values = {
            'reports': reports,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/package_list.html')
        self.response.out.write(template.render(path, template_values))

class CrashReporsForPackageHandler(webapp2.RequestHandler):
    def get(self, package_name):
        reports = CrashReport.for_package(package_name)

        template_values = {
            'reports': reports,
        }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/list.html')
        self.response.out.write(template.render(path, template_values))

class CrashReportHandler(webapp2.RequestHandler):
    def get(self, report_id):
        report = CrashReport.get_by_id(long(report_id))

        template_values = {
            'report': report,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/crashreport.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/reports/all',            CrashReportListHandler),
    ('/reports/package/(.*)',   CrashReporsForPackageHandler),
    ('/reports/(\d+)',          CrashReportHandler),
    ], debug=True)
