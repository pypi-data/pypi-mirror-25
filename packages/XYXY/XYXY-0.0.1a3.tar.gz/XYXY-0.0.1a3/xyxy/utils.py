def split_keys(features,labels):
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
