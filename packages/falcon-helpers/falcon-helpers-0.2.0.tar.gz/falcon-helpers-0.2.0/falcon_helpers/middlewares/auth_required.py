import falcon
import jwt


def _default_failed(reason):
    raise falcon.HTTPFound('/auth/login')


class AuthRequiredMiddleware:
    """Requires a cookie be set with a valid JWT or fails

    Example:
        import falcon
        from falcon_helpers.middlewares.auth_required import AuthRequiredMiddleware

        class Resource:
            auth_required = True

            def on_get(self, req, resp):
                # ...

        def when_fails_auth(reason):


        api = falcon.API(
            middleware=[
                AuthRequiredMiddleware(
                    'your-audience',
                    'a-really-great-random-string')
            ]
        )

        api.add_route('/', Resource())

    Attributes:
        audience: (string) A string audience which is passed to the JWT decoder

        secret: (string) A secret key to verify the token

        when_fails: (function) A function to execute when the authentication
            fails

        cookie_name: (string) the name of the cookie to look for

        resource_param: (string) the name of the paramater to look for on the
            resource to activate this middleware

    """

    def __init__(self, audience, secret, when_fails=None,
                 cookie_name='X-AuthToken', resource_param='auth_required'):
        self.audience = audience
        self.secret = secret
        self.failed_action = when_fails or _default_failed
        self.cookie_name = cookie_name
        self.resource_param = resource_param

    def process_resource(self, req, resp, resource, params):
        required = getattr(resource, self.resource_param, True)
        token = req.cookies.get(self.cookie_name, False)

        if not required:
            return

        if required and not token:
            self.failed_action(Exception('Missing Token'))

        try:
            results = jwt.decode(token, self.client_secret,
                                 audience=self.client_id)
        except jwt.ExpiredSignatureError as e:
            self.failed_action(e)
        except jwt.DecodeError as e:
            self.failed_action(e)

        req.context['auth_token_contents'] = results
