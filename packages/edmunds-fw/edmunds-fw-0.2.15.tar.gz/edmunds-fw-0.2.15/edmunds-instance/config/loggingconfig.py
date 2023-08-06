
from edmunds.gae.runtimeenvironment import RuntimeEnvironment as GaeRuntimeEnvironment
if GaeRuntimeEnvironment().is_gae():
    from edmunds.log.drivers.googleappengine import GoogleAppEngine as LogDriver
else:
    from edmunds.log.drivers.file import File as LogDriver


APP = {

    # ------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------
    #
    # Logging is configured here.
    # Drivers:
    # from edmunds.log.drivers.file import File
    # from edmunds.log.drivers.stream import Stream
    # from edmunds.log.drivers.syslog import SysLog
    # from edmunds.log.drivers.timedfile import TimedFile
    #

    'log':
    {
        'enabled': True,
        'instances':
        [
            {
                'name': 'file',
                'driver': LogDriver,
            },
        ],
    },

}
