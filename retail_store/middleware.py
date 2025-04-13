# from django.shortcuts import redirect

# class ForceUpdateMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated and request.user.first_login:
#             return redirect('update_credentials')
#         return self.get_response(request)
