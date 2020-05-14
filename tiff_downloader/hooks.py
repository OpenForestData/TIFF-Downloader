import falcon


def required_params(*required_params):
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
