import xml.etree.ElementTree as XML

def bitbucket_publisher(parser, xml_parent, data):
    """yaml: bitbucket

    Example::

      publishers:
          - bitbucket:
              notify-start: true
              notify-finish: true
              override-latest-build: false
              credentials-id: <optional>

    """
    if data is None:
        data = dict()

    notifier = XML.SubElement(
        xml_parent, 'jenkins.plugins.bitbucket.BitbucketBuildStatusNotifier')
    notifier.set('plugin', 'bitbucket-build-status-notifier@1.3.0')

    for (opt, attr) in (('notify-start', 'notifyStart'),
                        ('notify-finish', 'notifyFinish'),
                        ('override-latest-build', 'overrideLatestBuild')):
        (XML.SubElement(notifier, attr)
         .text) = 'true' if data.get(opt, True) else 'false'

    if data.get('credentials-id'):
        (XML.SubElement(notifier, 'credentialsId')
         .text) = data.get('credentials-id')
