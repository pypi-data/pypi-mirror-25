import general_exceptions
try:
    import cPickle as pickle
except:
    import pickle


def get_application_settings(application_name, redis):
        # TODO: Add settings validation
        if not application_name:
            raise general_exceptions.Register_NoApplicationName('Can\'t set application settings: No application name')
        try:
            application_settings = pickle.loads(redis.get('redongo_{0}'.format(application_name)))
            fields_to_validate = [
                'mongo_host',
                'mongo_port',
                'mongo_database',
                'mongo_collection',
                'mongo_user',
                'mongo_password',
                'bulk_size',
                'bulk_expiration',
                'serializer_type',
                # 'transaction_expiration',  # TODO: Reactivate after 0.4.0
            ]

            for f in fields_to_validate:
                if not application_settings.get(f, None):
                    raise general_exceptions.ApplicationSettingsError('No {0} value in {1} application settings'.format(f, application_name))

            return application_settings
        except TypeError:
            raise general_exceptions.ApplicationSettingsError('Not existing conf for application {0}'.format(application_name))
        except ValueError:
            raise general_exceptions.ApplicationSettingsError('Invalid existing conf for application {0}'.format(application_name))


def replace_reserved_keys(obj):
    """
    Recursivly goes through the dictionnary obj and replaces keys with a convert function.
    """
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.iteritems():
            new[transform_reserved_key(k)] = replace_reserved_keys(v)
    elif isinstance(obj, list):
        new = []
        for v in obj:
            new.append(replace_reserved_keys(v))
    else:
        return obj
    return new


def transform_reserved_key(k):
    if k == 'language':
        return 'language|original'
    return k
