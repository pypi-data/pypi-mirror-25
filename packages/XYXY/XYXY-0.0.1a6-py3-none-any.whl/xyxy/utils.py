def split_keys(features,labels,data_type='dict'):

    if data_type == 'dict' or data_type == dict:

        if type(features) == str:
            features = [features]
        if type(labels) == str:
            labels = [labels]

        def _split(x):
            return [
                {key: obj[key] for key in features}
                for obj in x
            ],[
                {key: obj[key] for key in labels}
                for obj in x
            ]

        return _split

    if data_type == 'list' or data_type == list:

        if type(features) == str:
            get_features = lambda x: x[features]
        else:
            get_features = lambda x: [x[key] for key in features]

        if type(labels) == str:
            get_labels = lambda x: x[labels]
        else:
            get_labels = lambda x: [x[key] for key in labels]

        def _split(x):
            return [
                       get_features(obj)
                       for obj in x
                   ], [
                       get_labels(obj)
                       for obj in x
                   ]

        return _split
