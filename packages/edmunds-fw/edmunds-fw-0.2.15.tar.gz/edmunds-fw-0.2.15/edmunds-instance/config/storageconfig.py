
from edmunds.gae.runtimeenvironment import RuntimeEnvironment as GaeRuntimeEnvironment
if GaeRuntimeEnvironment().is_gae():
    from edmunds.storage.drivers.googlecloudstorage import GoogleCloudStorage as StorageDriver
else:
    from edmunds.storage.drivers.file import File as StorageDriver


APP = {

    # ------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------
    #
    # Storage is configured here.
    #

    'storage':
    {
        'instances':
        [
            {
                'name': 'file',
                'driver': StorageDriver,
            },
        ],
    },

}
