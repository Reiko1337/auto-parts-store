class Session:
    """Сессия"""

    def __init__(self, request):
        self.request = request
        self.session = request.session

    def save(self):
        self.session.modified = True
