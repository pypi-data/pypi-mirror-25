import logging

from requests import Session


logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO,
                    filename='/opt/amqp-middleware/agent.log',
                    format='%(asctime)s [%(levelname)s] - '
                           '%(funcName)s: %(message)s')

log = logging.getLogger(__name__)

# A mapping between cloud provider names and the field of the corresponding
# resource ID, as it is meant to exist in the database.
PROVIDERS = {
    'azure': 'name',
    'do': 'resource_id',
    'aws': 'aws_resource_id',
    'docker': 'container_id',
    'openstack': 'external_id',
    'vcloud': 'vcloud_vapp_name',
    'vsphere': 'vsphere_server_id',
}


class CloudifyClient(object):
    """An HTTP client for Cloudify Manager's API."""

    def __init__(self, host, credentials, secure=False, ssl_enabled=False,
                 verify=True):
        """The CloudifyClient queries the Cloudify Manager's API in order to
        retrieve information on deployments and node instances.

        :param host: the Cloudify Manager's IP address.
        :param credentials: security parameters used in order to authenticate
         to a secure Cloudify Manager.
        :param secure: denotes whether the Cloudify Manager is secure.
        :param ssl_enabled: denotes whether SSL is enabled.
        :param verify: specifies whether to verify the SSL certificate.

        """
        username = credentials.get('username', '')
        password = credentials.get('password', '')
        tenant = credentials.get('tenant', '')
        if secure and not (username and password):
            raise Exception('Security is enabled, but no username:password '
                            'has been provided')
        if not tenant:
            raise Exception('No tenant specified')
        if ssl_enabled:
            cert = credentials.get('ca_certs', '')
            if not cert:
                raise Exception('SSL enabled, but path to public certificate '
                                'is missing')

        scheme = 'https' if (secure and ssl_enabled) else 'http'
        self.url = '%s://%s/api/v2.1/node-instances' % (scheme, host)
        self.session = Session()
        self.session.headers.update({'Tenant': tenant})
        if secure:
            self.session.auth = (username, password)
        if ssl_enabled:
            if secure:
                self.session.verify = cert if verify else verify
            else:
                # https://github.com/cloudify-cosmo/
                # cloudify-manager-blueprints/blob/3.4-build/
                # aws-ec2-manager-blueprint-inputs.yaml#L58
                log.warning('Ignoring SSL, since security is disabled')

        # Cached host information in the form of:
        # { host_id: ( provider, resource_id ) }
        self.resources = dict()

    def get_rid(self, event):
        """Maps the host ID (assigned by Cloudify Manager) contained in the
        event dict to the correponding cloud provider's resource ID.
        """
        deployment_id = event['deployment_id']
        host_id = event['host']

        if host_id not in self.resources:
            log.info('No cached information found for host "%s" (%s)',
                     host_id, deployment_id)

            # Query db for the node instance's runtime properties.
            runtime_properties = self.get_attributes(deployment_id, host_id)

            # Search for host information and cache it.
            for provider, rfield in PROVIDERS.iteritems():
                if rfield in runtime_properties.iterkeys():
                    rid = runtime_properties[rfield]

                    self.resources[host_id] = (provider, rid)
                    log.info('Database HIT for host "%s" (%s): %s = %s',
                             host_id, deployment_id, rfield, rid)
                    break
            else:
                log.error('Failed to find resource ID for host "%s" (%s)',
                          host_id, deployment_id)
                return

        # Inject resource ID in the event.
        provider, rid = self.resources[host_id]
        event.update({
            'provider': provider,
            'resource_id': rid
        })

    def get_attributes(self, deployment_id, host_id):
        """Queries the Cloudify Manager's API for the specified `host_id` and
        verifies that the deployment the node instance belongs to matches the
        `deployment_id` provided.

        If the query fails, this method will not raise an error, but rather
        return. In that case, the provider's resource ID will NOT be injected
        into the metric, which may cause identification issues later on.

        :param deployment_id: the deployment the node instance belongs to.
        :param host_id: the node instance's host ID.

        :return: the node instance's runtime properties.

        """
        node_instance = self.session.get('%s/%s' % (self.url, host_id))

        try:
            node_instance = node_instance.json()
            assert node_instance['deployment_id'] == deployment_id
        except ValueError as err:
            log.error('HTTP request failed for node "%s" (%s) with status '
                      'code %d: %s', host_id, deployment_id,
                      node_instance.status_code, node_instance.content)
            # Propagate the original error in case the API returned OK,
            # but decoding failed regardless.
            if node_instance.ok:
                raise
        except AssertionError as err:
            log.error('Deployment ID mismatch for host "%s" (%s)',
                      host_id, deployment_id)
        else:
            err = ''

        return node_instance['runtime_properties'] if not err else {}
