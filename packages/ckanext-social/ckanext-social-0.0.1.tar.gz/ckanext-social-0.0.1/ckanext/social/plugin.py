import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class SocialPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'social')

    def get_helpers(self):
        """
        All functions, not starting with __ in the ckanext.social.helpers
        module will be loaded and made available as helpers to the
        templates.
        """
        from ckanext.social.helpers import helpers
        from inspect import getmembers, isfunction

        helper_dict = {}

        funcs = [o for o in getmembers(helpers, isfunction)]
        return dict([(f[0],f[1],) for f in funcs if not f[0].startswith('__')])