import trafaret as T

CONFIG = T.Dict({
    T.Key('i18n'):
        T.Dict({
            'base_route': T.String(),
            'default_local_name': T.String(),
            'colander': T.Bool(),
        }),
})
