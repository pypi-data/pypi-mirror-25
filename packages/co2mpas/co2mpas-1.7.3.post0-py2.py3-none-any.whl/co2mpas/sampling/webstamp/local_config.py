# Local-settings GIT-INGORED!
#
# Note: Don't *ever* do this in a real app. A secret key should not have a
#       default, rather the app should fail if it is missing. For the sample
#       application, one is provided for convenience.
SECRET_KEY = 'dev key'
#SENTRY_DSN = 'https://fb06617d61fd4d99a9ef7a48bee84396:ea59f993a95143fb9c9a7534f5be52f9@sentry.io/226557'

#WTF_CSRF_ENABLED = True
DEFAULT_STAMP_RECIPIENTS = [
    'JRC-CO2MPAS@ec.europa.eu',
    'CLIMA-LDV-CO2-CORRELATION@ec.europa.eu']

CHECK_SIGNING_KEY_SCRIPT = 'check_key'

MAIL_CLI_ARGS = [
    'cmd',
    '/C',
    'echo {subject}',
]

TRAITLETS_CONFIG = {
    'GpgSpec': {
        #'allow_test_key': True,
    },
    'StamperAuthSpec': {
        'master_key': 'CBBB52FF',
    },
    'SigChain': {
        'read_only_files': True,
    }
}
