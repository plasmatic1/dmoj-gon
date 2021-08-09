from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),

    path('problem/<str:name>', views.problem_view, name='view'),
    path('problem/<str:name>/tests', views.problem_tests_view, name='view_tests'),
    path('problem/<str:name>/invocations', views.problem_invocations_view, name='view_invocations'),
    path('problem/<str:name>/package', views.problem_package_view, name='view_package'),

    # More utility views
    path('new', views.new_problem_view, name='new'),
    path('delete/<str:name>', views.wip_view, name='delete'),
    path('rename/<str:name>/<str:newname>', views.wip_view, name='rename')
]
