"""sale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import viewsets

router = DefaultRouter()
router.register('branch', viewset=viewsets.BranchViewSet)
router.register('city', viewset=viewsets.CityViewSet)
router.register('customer', viewset=viewsets.CustomerViewSet)
router.register('department', viewset=viewsets.DepartmentViewSet)
router.register('district', viewset=viewsets.DistrictViewSet)
router.register('employee', viewset=viewsets.EmployeeViewSet)
router.register('marital_status', viewset=viewsets.MaritalStatusViewSet)
router.register('product', viewset=viewsets.ProductViewSet)
router.register('product_group', viewset=viewsets.ProductGroupViewSet)
router.register('sale', viewset=viewsets.SaleViewSet)
router.register('sale_item', viewset=viewsets.SaleItemiewSet)
router.register('state', viewset=viewsets.StateViewSet)
router.register('supplier', viewset=viewsets.SuppplierViewSet)
router.register('zone', viewset=viewsets.ZoneViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sale/api/', include(router.urls)),
]
