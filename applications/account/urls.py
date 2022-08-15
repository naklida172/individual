from django.urls import path

from applications.account.views import RegisterApiView, ActivationView, LoginApiView, ForgotPasswordView, \
    ForgotPasswordComplete, ChangePasswordView

urlpatterns = [

    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_confirm/', ForgotPasswordComplete.as_view()),

]
