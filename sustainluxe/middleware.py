import logging

logger = logging.getLogger(__name__)

# teminal answer from request


class LogImageRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/media/') or request.path.endswith(
            ('.png', '.jpg', '.jpeg', '.gif')
        ):
            logger.info(
                f"img request: {request.path} - Status: {response.status_code}"
            )

        return response
