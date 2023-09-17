from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.DetailContract.as_view(), name='home'),
    path('contracts/', views.DetailContract.as_view(), name='contract'),
    path('contracts/<int:pk>/', views.DetailContract.as_view(), name='contract_detailed'),
    path('contracts/<int:pk>/draft', views.create_draft, name='contract_draft_create'),
    path('drafts', views.DetailDraft.as_view(), name='drafts'),
    path('drafts/<int:pk>/', views.DetailDraft.as_view(), name='drafts_detailed'),
    path('drafts/<int:pk>/<int:update>', views.DetailDraft.as_view(), name='drafts_update_view'),
    path('drafts/<int:pk>/item/<int:ipk>/satisfy', views.satisfy, name='drafts_item_satisfy'),  # DOne
    path('drafts/<int:pk>/item/<int:ipk>/check', views.DetailDraft.as_view(), name='drafts_item_check'),  # done
    path('drafts/<int:pk>/item/<int:ipk>/order/', views.DetailItemSupplier.as_view(), name='drafts_item_order'),  # done
    path('drafts/<int:pk>/item/<int:ipk>/order/<int:sid>/supplier/', views.DetailItemSupplier.as_view(), name='drafts_item_order_supplier'), #done
    path('drafts/<int:pk>/finish', views.finish, name='drafts_finish'),  # done
    path('drafts/<int:pk>/satisfyall', views.satisfy_all_possible, name='drafts_satisfy_all'),  # done
    path('drafts/<int:pk>/restore', views.finish, name='drafts_restore'),  # done
    path('drafts/<int:pk>/update/', views.update_for, name='drafts_update'),
    path('drafts/<int:pk>/report', views.report, name='drafts_report'),  # TODO
    path('drafts/<int:pk>/delete', views.delete_draft, name='drafts_delete_this'),
    path('suppliers/', views.DetailSupplier.as_view(), name='suppliers'),
    path('suppliers/<int:pk>/', views.DetailSupplier.as_view(), name='suppliers_detailed'),
    path('sometest/', views.some_test_view, name='sometest')
]
