from app.web.app import View


class AdminLoginView(View):
    async def post(self):
        raise NotImplementedError


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
