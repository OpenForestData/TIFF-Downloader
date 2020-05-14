import falcon


def required_params(*required_params):
    """
    Decorator for .on_get() methods that makes given query parameters obligatory.

    Parameters
    ----------
    required_params: list of params that have to be included in request query

    Returns
    -------
    Decorated function

    """

    def hook(req, resp, resource, params):
        missing_params = []
        for required_param in required_params:
            if required_param not in req.params:
                missing_params.append(required_param)
        if missing_params:
            msg = f'Missing query params: {", ".join(missing_params)}'
            raise falcon.HTTPBadRequest(
                'Missing query params.', msg)

    return hook
