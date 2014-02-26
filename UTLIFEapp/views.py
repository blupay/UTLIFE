# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader

from models import *



from datetime import date

import datetime, random

def check_balance_function(request,tid,accNum,ls):
	try:
		if accNum == "":
			return HttpResponseForbidden("Forbidden!!, No Account Number!!")

		customer = Customer.objects.get(account_number=accNum)
		tID = Terminal.objects.get(terminal_serial_no=tid)
                col = Collector.objects.get(terminalID=tID)
		try:
			pwdBy = PoweredBy.objects.get(pk=1)
                except PoweredBy.DoesNotExist:	
			pwdBy ="Blupay GH"
		if ls == '0':
			try:
				loan = Loans.objects.get(customer_name = customer,status='PENDING')
			except Loans.DoesNotExist:
				return HttpResponseForbidden("Forbidden!!, Loan Account does not exist!!")
			
			response = HttpResponse('UT-LIFE LOAN BALANCE\n*************************\n\nName: '+customer.fullname+'\nAcc_No: *******'+accNum[4:]+'\nLoan Balance: GHS '+ str(loan.amtLeftToPay)+'\nLast Payment: '+str(loan.date_updated.strftime("%b %d,%Y"))+'\nCollector: '+str(col.fullname)+'\nDate: '+str(datetime.datetime.now().strftime("%b %d,%Y,%I:%M %p"))+'\n\n*************************\nPwd by '+pwdBy.poweredByName+'\n\n\n')
			response['Content-Length'] = str(len(response.content))
                	response['Content-Type']  = 'text/plain; charset=utf-8'
                	return response

		elif ls == '1':
			try:
				saving = Savings.objects.get(customer_name = customer)
			except Savings.DoesNotExist:
				return HttpResponseForbidden("Forbidden!!, Savings Account does not exist!!")	  		
			response = HttpResponse('UT-LIFE SAVINGS BALANCE\n*************************\n\nName: '+customer.fullname+'\nAcc_No: *******'+accNum[4:]+'\nSavings Balance: GHS '+ str(saving.savingsAmount)+'\nLast Payment: '+str(saving.date_updated.strftime("%b %d,%Y"))+'\nCollector: '+str(col.fullname)+'\nDate: '+str(datetime.datetime.now().strftime("%b %d,%Y,%I:%M %p"))+'\n\n*************************\nPwd by '+pwdBy.poweredByName+'\n\n\n')
			response['Content-Length'] = str(len(response.content))
                	response['Content-Type']  = 'text/plain; charset=utf-8'
                	return response
		
	except Customer.DoesNotExist:
		response = HttpResponseForbidden("Forbidden!!, Customer does not exist!!")	
		response['Content-Length'] = str(len(response.content))
               	response['Content-Type']  = 'text/plain; charset=utf-8'
		return response                	
   	
		 	  		 
	except Terminal.DoesNotExist:
		response = HttpResponseForbidden("Forbidden!!, Terminal does not exist!!")	
		response['Content-Length'] = str(len(response.content))
               	response['Content-Type']  = 'text/plain; charset=utf-8'
		return response   
  
	except Collector.DoesNotExist:	
		response = HttpResponseForbidden("Forbidden!!, Collector does not exist!!")	
		response['Content-Length'] = str(len(response.content))
               	response['Content-Type']  = 'text/plain; charset=utf-8'
		return response     





def get_post_function(request,tidAmt,ls,accNum):
	#amt=500.0
	#accNum='0123456789'
	#ls=1
	tid = tidAmt[:18]
        amt = float(tidAmt[18:])
	try:
		
		#response = HttpResponseForbidden("GALORE GALORE GALORE")	
		#response['Content-Length'] = str(len(response.content))
               	#response['Content-Type']  = 'text/plain; charset=utf-8'
		#return response
		if accNum == "":
			return HttpResponseForbidden("Forbidden!!, No Account Number!!")             	
   	
		trans_id_gen = str(random.randint(0,9)) +str(random.randint(100,999)) + str(random.randint(100,999)) + str(random.randint(100,999))
		customer = Customer.objects.get(account_number=accNum)
		tID = Terminal.objects.get(terminal_serial_no=tid)
                col = Collector.objects.get(terminalID=tID)
		if ls == '0':
			try:
				loan = Loans.objects.get(customer_name = customer,status='PENDING')
			except Loans.DoesNotExist:
				return HttpResponseForbidden("Forbidden!!, Loan Account does not exist!!")
			loan.amountPaid = float(loan.amountPaid) + float(amt)
			trans_type = 'Loan'
			
			loan.save()
		elif ls == '1':
			try:
				saving = Savings.objects.get(customer_name = customer)
			except Savings.DoesNotExist:
				return HttpResponseForbidden("Forbidden!!, Savings Account does not exist!!")	  	
			savings_balance = float(saving.savingsAmount) + float(amt)
			trans_type = 'Savings'
			saving.savingsAmount = savings_balance
			saving.save()

		
		else:
			return HttpResponseForbidden("You do not have permission!!")


		trans = Transaction(transaction_type=trans_type,paymentAmount = float(amt),transaction_id = trans_id_gen,customer_name=customer, collector_name=col)
		trans.save()
                try:
			pwdBy = PoweredBy.objects.get(pk=1)
                except PoweredBy.DoesNotExist:	
			pwdBy ="Blupay GH"
		if trans_type == 'Loan':
			response = HttpResponse('UT-LIFE LOAN E-RECEIPT\n*************************\n\nTranx ID: '+trans_id_gen+'\nName: '+customer.fullname+'\nAcc_No: *******'+accNum[4:]+'\nLoan Amount: GHS '+str(loan.amountToPay)+'\nAmount Paid: GHS '+str(amt)+'\nLoan Balance: GHS '+ str(loan.amtLeftToPay)+'\nCollector: '+str(col.fullname)+'\nDate: '+str(datetime.datetime.now().strftime("%b %d,%Y,%I:%M %p"))+'\n\n*************************\nPwd by '+pwdBy.poweredByName+'\n\n')
			response['Content-Length'] = str(len(response.content))
                	response['Content-Type']  = 'text/plain; charset=utf-8'
                	return response

		elif trans_type == 'Savings':
			response = HttpResponse('UT-LIFE SAVINGS E-RECEIPT\n*************************\n\nTranx ID: '+trans_id_gen+'\nName: '+customer.fullname+'\nAcc_No: *******'+accNum[4:]+'\nAmount: GHS '+str(amt)+'\nSavings Balance: GHS '+ str(saving.savingsAmount)+'\nCollector: '+str(col.fullname)+'\nDate: '+str(datetime.datetime.now().strftime("%b %d,%Y,%I:%M %p"))+'\n\n*************************\nPwd by '+pwdBy.poweredByName+'\n\n\n')
			response['Content-Length'] = str(len(response.content))
                	response['Content-Type']  = 'text/plain; charset=utf-8'
                	return response
		
		
	except Customer.DoesNotExist:
		response = HttpResponseForbidden("Forbidden!!, Customer does not exist!!")	
		response['Content-Length'] = str(len(response.content))
               	response['Content-Type']  = 'text/plain; charset=utf-8'
		return response                	
   	
		 	  		 
	except Terminal.DoesNotExist:
		response = HttpResponseForbidden("Forbidden!!, Terminal does not exist!!")	
		response['Content-Length'] = str(len(response.content))
               	response['Content-Type']  = 'text/plain; charset=utf-8'
		return response   
  
	except Collector.DoesNotExist:	
		response = HttpResponseForbidden("Forbidden!!, Collector does not exist!!")	
		response['Content-Length'] = str(len(response.content))
               	response['Content-Type']  = 'text/plain; charset=utf-8'
		return response     

