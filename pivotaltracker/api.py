import os
import urllib2

PIVOTAL_STORY_XML = '''
    <story>
        <story_type>bug</story_type>
        <name>Fix: %s</name>
        <description>%s</description>
    </story>'''

PIVOTAL_STORY_URL = 'http://www.pivotaltracker.com/services/v3/projects/%s/stories'

class PivotalApi:
    def __init__(self, project_id, auth_token):
        self.project_id = project_id
        self.auth_token = auth_token

    def createbug(self, report, base_url):
        print self.project_id
        print self.auth_token

        report_url = base_url + '/api/crashreport/' + str(report.key.id())
        xml = PIVOTAL_STORY_XML % (report.stack_summary, report_url)
        create_story_url = PIVOTAL_STORY_URL % self.project_id

        req = urllib2.Request(url=create_story_url,
            data=xml,
            headers={
                'Content-Type': 'application/xml',
                'X-TrackerToken': self.auth_token
            })

        urllib2.urlopen(req)
