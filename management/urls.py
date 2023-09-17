from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.DetailManagementContract.as_view(), name='m_home'),
    path('contracts/', views.DetailManagementContract.as_view(), name='m_contract'),
    path('contracts/<int:pk>/', views.DetailManagementContract.as_view(), name='m_contract_detailed'),
    path('drafts/', views.DetailManagementDraft.as_view(), name='m_draft'),
    path('drafts/<int:pk>/', views.DetailManagementDraft.as_view(), name='m_draft_detailed'),
    path('drafts/<int:pk>/restore', views.finish, name='m_drafts_restore'),
    path('drafts/<int:pk>/finish', views.finish, name='m_drafts_finish'),
    path('drafts/<int:pk>/reportdraft', views.report_draft, name='m_drafts_report'),  # TODO
    path('stats/', views.DetailStats.as_view(), name='m_stats'),
    path('stats/report', views.report_all, name='m_report'),
    path('history/', views.DetailHistory.as_view(), name='m_history')
]


#28