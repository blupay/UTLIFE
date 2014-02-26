from models import *
from model_report.report import reports, ReportAdmin
from django.utils.translation import ugettext_lazy as _
from model_report.utils import (usd_format, avg_column, sum_column, count_column)

def amount_format(value,instance):
      rvalue = int(value)
      return _('%s' %rvalue)
      
def sch_format(value,instance):
      return _('%s' %value)

def school_label(report, field):
    return _("Schools")
    
def customer_label(report, field):
    return _("Customer")

def collector_label(report, field):
    return _("Collector")
    
def supervisor_label(report, field):
    return _("Supervisor")
    
def filter_school(report, values):
    return _('%s' %values)
    
    
class Trans_Report(ReportAdmin):
	title=('Transactions')
	model= Transaction
	fields = ['transaction_id','transaction_type','paymentAmount','collector_name__supervisor__full_name','collector_name__fullname','customer_name__fullname','date_created',]
	list_order_by = ('-date_created',)
	list_group_by = ('date_created','collector_name__supervisor__full_name','collector_name__fullname',)
	list_filter = ('date_created','collector_name__supervisor__full_name','collector_name__fullname',)

	type = 'chart'

	group_totals = {
        'paymentAmount': sum_column,
	
	}
	report_totals={
	'paymentAmount':sum_column,
	}
	
	override_field_formats = {
        #'studentID__schoolID__schoolName':sch_format,	
	}
	override_field_labels ={
	#'studentID__schoolID__schoolName':school_label,
	'collector_name__supervisor__full_name':supervisor_label,
	'collector_name__fullname':collector_label,
	'customer_name__fullname':customer_label,
	}
	override_field_filter_values = {
        #'studentID__schoolID__schoolName': filter_school
    	}
    	override_field_choices = {
        #'studentID__schoolID__schoolName': filter_school
      	}
	
	list_serie_fields = ('paymentAmount',)

	chart_types = ('pie', 'column', 'line')

reports.register('transactions-report',Trans_Report)



