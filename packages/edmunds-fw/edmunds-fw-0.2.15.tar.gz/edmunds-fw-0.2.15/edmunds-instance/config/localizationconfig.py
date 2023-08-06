
APP = {

    # ------------------------------------------------------------
    # Localization
    # ------------------------------------------------------------
    #
    # Localization is configured here.
    #
    # Location Drivers:
    # from edmunds.localization.location.drivers.googleappengine import GoogleAppEngine
    # from edmunds.localization.location.drivers.maxmindcitydatabase import MaxMindCityDatabase
    # from edmunds.localization.location.drivers.maxmindenterprisedatabase import MaxMindEnterpriseDatabase
    # from edmunds.localization.location.drivers.maxmindwebservice import MaxMindWebService
    #
    # Translations Drivers:
    # from edmunds.localization.translations.drivers.configtranslator import ConfigTranslator
    #

    'localization':
    {
        'enabled': False,

        'locale':
        {
            'fallback': 'en_US',
            'supported': ['en_US', 'en', 'nl_BE', 'nl'],
        },

        'location':
        {
            'enabled': False,
            'instances':
            [
                #
            ],
        },

        'translations':
        {
            'enabled': False,
            'instances':
            [
                #
            ],
        },
    },

}
