from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ModelBase(models.Model):
    id = models.AutoField(
        db_column='id',
        null=False,
        primary_key=True,
        verbose_name=_('Code')
    )
    created_at = models.DateTimeField(
        db_column='created_at',
        null=False,
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    modified_at = models.DateTimeField(
        db_column='modified_at',
        null=False,
        auto_now=True,
        verbose_name=_('Modified at')
    )
    active = models.BooleanField(
        db_column='active',
        null=False,
        default=True,
        verbose_name=_('Active')
    )

    class Meta:
        abstract = True
        managed = True


class Zone(ModelBase):
    name = models.CharField(
        max_length=32,
        null=False,
        unique=True
    )

    class Meta:
        db_table = 'zone'


class State(ModelBase):
    name = models.CharField(
        max_length=56,
        null=False,
        unique=True
    )
    abbreviation = models.CharField(
        max_length=2,
        null=False,
        unique=False
    )

    class Meta:
        db_table = 'state'


class City(ModelBase):
    state = models.ForeignKey(
        to='State',
        on_delete=models.DO_NOTHING,
        db_column='id_state',
        null=False
    )
    name = models.CharField(
        max_length=56,
        null=False
    )

    class Meta:
        db_table = 'city'
        unique_together = [
            ['state', 'name']
        ]


class District(ModelBase):
    state = models.ForeignKey(
        to='State',
        on_delete=models.DO_NOTHING,
        db_column='id_state',
        null=False
    )
    city = models.ForeignKey(
        to='City',
        on_delete=models.DO_NOTHING,
        db_column='id_city',
        null=False
    )
    name = models.CharField(
        max_length=64,
        null=False
    )

    class Meta:
        db_table = 'district'


class MaritalStatus(ModelBase):
    description = models.CharField(
        max_length=36,
        null=False,
        unique=True
    )

    class Meta:
        db_table = 'marital_status'


class Customer(ModelBase):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False
    )
    name = models.CharField(
        max_length=64,
        null=False
    )
    monthly_income = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        null=False
    )

    class Meta:
        db_table = 'customer'


class Department(ModelBase):
    name = models.CharField(
        max_length=56,
        null=False,
        unique=True
    )

    class Meta:
        db_table = 'department'


class Branch(ModelBase):
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )
    name = models.CharField(
        max_length=64,
        null=False
    )

    class Meta:
        db_table = 'branch'


class Supplier(ModelBase):
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )
    name = models.CharField(
        max_length=56,
        null=False
    )
    legal_document = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )

    class Meta:
        db_table = 'supplier'


class Employee(AbstractBaseUser, PermissionsMixin):
    department = models.ForeignKey(
        to='Department',
        on_delete=models.DO_NOTHING,
        db_column='id_department',
        null=False
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False
    )
    manager = models.ForeignKey(
        to='Employee',
        on_delete=models.DO_NOTHING,
        db_column='id_manager',
        null=True
    )
    name = models.CharField(
        max_length=56,
        null=False
    )
    salary = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False
    )
    login = models.CharField(
        max_length=56,
        null=False,
        unique=True
    )
    password = models.CharField(
        max_length=256,
        null=False
    )
    admission_date = models.DateField(
        null=True
    )
    birth_date = models.DateField(
        null=False
    )
    is_superuser = models.BooleanField(
        null=True,
        default=False
    )
    is_staff = models.BooleanField(
        null=True,
        default=False
    )

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'employee'


class ProductGroup(ModelBase):
    description = models.CharField(
        max_length=40,
        null=False,
        unique=True
    )
    percentage_comission = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False
    )
    percentage_gain = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False
    )

    class Meta:
        db_table = 'product_group'


class Product(ModelBase):
    product_group = models.ForeignKey(
        to='ProductGroup',
        on_delete=models.DO_NOTHING,
        db_column='id_product_group',
        null=False
    )
    supplier = models.ForeignKey(
        to='Supplier',
        on_delete=models.DO_NOTHING,
        db_column='id_supplier',
        null=False
    )
    name = models.CharField(
        max_length=256,
        null=False
    )
    cost_price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False
    )
    sale_price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False
    )

    class Meta:
        db_table = 'product'


class Sale(ModelBase):
    branch = models.ForeignKey(
        to='Branch',
        on_delete=models.DO_NOTHING,
        db_column='id_branch',
        null=False
    )
    customer = models.ForeignKey(
        to='Customer',
        on_delete=models.DO_NOTHING,
        db_column='id_customer',
        null=False
    )
    date = models.DateTimeField(
        null=False,
        auto_now_add=True
    )
    total = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False,
        default=0.00
    )

    class Meta:
        db_table = 'sale'


class SaleItem(ModelBase):
    sale = models.ForeignKey(
        to='Sale',
        on_delete=models.DO_NOTHING,
        db_column='id_sale',
        null=False
    )
    product = models.ForeignKey(
        to='Product',
        on_delete=models.DO_NOTHING,
        db_column='id_product',
        null=False
    )
    quantity = models.DecimalField(
        max_digits=16,
        decimal_places=3,
        null=False
    )
    subtotal = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False,
        default=0.00
    )

    class Meta:
        db_table = 'sale_item'
