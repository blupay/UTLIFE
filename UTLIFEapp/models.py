from django.contrib import admin
from django.db import models
from countries.models import Country



from django.utils.timezone import now
from datetime import date,time
import datetime,random

class Supervisor(models.Model):
	full_name = models.CharField(max_length = 50, help_text = "Enter full name of the Supervisor")
	mobile = models.CharField(max_length=10, unique=True)
	area  = models.CharField(max_length = 40, blank =True,null = True)
	date_added = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s" %(self.full_name)

class PoweredBy(models.Model):
	poweredByName = models.CharField(max_length=20,unique=True)
	date_added = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return "%s" %(self.poweredByName)


class Terminal(models.Model):
	terminal_id = models.CharField(max_length=5)
	terminal_serial_no = models.CharField(unique=True,max_length = 20)
        #inUse = models.BooleanField(blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)

	def termID(self):
		if self.terminal_id == "":
			id_gen = random.randint(100,999)
                    
                	self.terminal_id = "TM%s"%(id_gen)
			print "TM%s"%(id_gen)
                else:
                     return self.terminal_id
                 
           	


	def __unicode__(self):
		return "%s" %(self.terminal_serial_no)
	
	def save(self,*args,**kwargs):
                self.termID()
                super(Terminal,self).save(*args, **kwargs)
                return True  	

class Collector(models.Model):
	collector_ID = models.CharField(max_length = 9, null = True)
        supervisor  =  models.ForeignKey(Supervisor,related_name="superVisor")
	fullname = models.CharField(max_length=20, null = False)
        terminalID      =  models.ForeignKey(Terminal,unique=True, related_name="terminalNo")
	phone_number = models.CharField(max_length=10, unique=True)
	dateOfBirth  = models.DateField()
        age          = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
        gender = models.CharField(max_length=6, choices = (("Male", "Male"), 
                                                    ("Female", "Female")
                                                   ))
	Nationality      =  models.ForeignKey(Country,default = "GH")
        
	residential_address = models.TextField(max_length=100)
	contact_Of_Next_Of_Kin = models.TextField("Contact-N.O.K",help_text ="Please enter contact details of Next of Kin",max_length = 60,blank =True,null = True)
	
	date_added = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)

	def collectorID(self):
		if self.collector_ID == None:
			id_gen = random.randint(100,800)
                	id_gen1 = random.randint(900,999) 
                	self.collector_ID = "%s%s%s" %(self.fullname[:3].upper(),id_gen,id_gen1)
                else:
                     return self.collector_ID
                 
           

	def __unicode__(self):
              return "%s-%s" %(self.collector_ID,self.fullname)
        
        def fullnameC(self):
              return "%s-%s" %(self.collector_ID,self.fullname)
	

	def Age(self):
		if self.dateOfBirth:
	                 min_allowed_dob = datetime.datetime(1900,01,01)
	         	 max_allowed_dob = datetime.datetime.now()
			 if int(self.dateOfBirth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.dateOfBirth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G")) - int(self.dateOfBirth.strftime("%G")))
               			 return "%s" %(self.age)
                             
			 else:
			 	return "Invalid Date"
		elif self.age and int(self.age[0:3])<=120: #no need cos age field was not added for the doctor. would be added later
	        	self.dateOfBirth = None
		        return True
                 
	
	
	def save(self,*args,**kwargs):
                self.collectorID()
                self.Age()
		super(Collector,self).save(*args, **kwargs)
                return True  


#CUSTOMER MODEL
class Customer(models.Model):
	customerID = models.CharField(max_length = 9, null = True)
	account_number = models.CharField(max_length =14, unique = True)
	fullname = models.CharField(max_length=20)
	telephone = models.CharField(max_length=10)
	address = models.TextField(max_length=100)
	dateOfBirth  = models.DateField()
        age          = models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
        gender = models.CharField(max_length=6, choices = (("Male", "Male"), 
                                                    ("Female", "Female")
                                                   ))
	#pensionAmount =  models.FloatField(null = True,default=0.0)
	#savingsAmount = models.FloatField(null = True,default=0.0)
        #loanAmount =  models.FloatField(null = True,default=0.0)
	Nationality      =  models.ForeignKey(Country,default = "GH")
        
	residential_address = models.TextField(max_length=100)
	contact_Of_Next_Of_Kin = models.TextField("Contact-N.O.K",help_text ="Please enter contact details of Next of Kin",max_length = 60,blank =True,null = True)
	
	#loanBalance = models.FloatField(null = True,default=loanAmount)
        date_added = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)	
	

	def customer_ID(self):
		if self.customerID == None:
			id_gen = random.randint(100,800)
                	id_gen1 = random.randint(900,999) 
                	self.customerID = "%s%s%s" %(self.fullname[:3].upper(),id_gen,id_gen1)
                else:
                     return self.customerID
           

	def __unicode__(self):
              return "%s-%s" %(self.account_number,self.fullname)
        
        def fullnameC(self):
              return "%s-%s" %(self.customerID,self.fullname)
	      
             


	def Age(self):
		if self.dateOfBirth:
	                 min_allowed_dob = datetime.datetime(1900,01,01)
	         	 max_allowed_dob = datetime.datetime.now()
			 if int(self.dateOfBirth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.dateOfBirth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.dateOfBirth.strftime("%G")))
               			 return "%s" %(self.age)
                             
			 else:
			 	return "Invalid Date"
		elif self.age and int(self.age[0:3])<=120: #no need cos age field was not added for the doctor. would be added later
	        	self.dateOfBirth = None
		        return True
                 
	
	
	def save(self,*args,**kwargs):
                self.customer_ID()
                self.Age()
		super(Customer,self).save(*args, **kwargs)
                return True

#TRANSACTION MODEL
class Savings(models.Model):
	savingID = models.CharField(max_length = 12,null = True)
	customer_name = models.ForeignKey(Customer, max_length=30,related_name="Scustomer")
	savingsAmount = models.FloatField(null = True,default=0.0)	
	date_created = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)
	
	def saving_ID(self):
		if self.savingID == None:
			id_gen = random.randint(100,800)
                	id_gen1 = random.randint(900,999) 
                	self.savingID = "S%s%s" %(id_gen,id_gen1)
                else:
                     return self.savingID
           

	def __unicode__(self):
              return "%s" %(self.savingID)
	
	def save(self,*args,**kwargs):
                self.saving_ID()
                
		super(Savings,self).save(*args, **kwargs)
                return True

class Loans(models.Model):
	loanID = models.CharField(max_length = 12,null = True)
	customer_name = models.ForeignKey(Customer, max_length=30,related_name="Lcustomer", help_text="check if customer is not having an outstanding loan")
	loanAmount = models.FloatField(null = True,default=0.0)
	amountToPay = models.FloatField(null = True,default=0.0)
	amountPaid = models.FloatField(null = True,default=0.0)
	amtLeftToPay = models.FloatField(null = True,default=0.0)
	status = models.CharField(max_length = 7,default=None)
	date_created = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)

	def loan_ID(self):
		if self.loanID == None:
			id_gen = random.randint(100,800)
                	id_gen1 = random.randint(900,999) 
                	self.loanID = "L%s%s" %(id_gen,id_gen1)
                else:
                     return self.loanID

	def loanStatus(self):
		if self.loanAmount != 0.0:
			self.amtLeftToPay = float(self.amountToPay) - float(self.amountPaid)
			if self.amtLeftToPay <= 0.0:
				self.status = "PAID"
			else:
				self.status = "PENDING"
		return True
			 

	def __unicode__(self):
              return "%s" %(self.loanID)
	
	def save(self,*args,**kwargs):
                self.loan_ID()
                self.loanStatus()
                '''
                try:
			loan = Loans.objects.get(customer_name = self.customer_name,amtLeftToPay__gt=0.0,status="PENDING")
			print loan
		except Loans.DoesNotExist:
			super(Loans,self).save(*args, **kwargs)	
		'''
		super(Loans,self).save(*args, **kwargs)	
                return True

	

class Transaction(models.Model):
	transaction_id = models.CharField(max_length = 12)
	transaction_type=models.CharField(max_length=7)
	paymentAmount = models.FloatField(null = True,default=0.0)
	#customer = models.ForeignKey(Customer,related_name='transactions')
	collector_name = models.ForeignKey(Collector,max_length=30,related_name="collector")
        #terminal_id = models.CharField(max_length = 6)
	customer_name = models.ForeignKey(Customer, max_length=30,related_name="Tcustomer")
	date_created = models.DateTimeField(auto_now_add=True)
      	date_updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.transaction_id






class PoweredByAdmin(admin.ModelAdmin):
	list_display = ('poweredByName','date_added','date_updated')
	list_filter = ('date_added','poweredByName')
	search_fields = ('poweredByName',)
	#inlines = [TransactionInline]
        ordering = ('-date_added',)




class CollectorAdmin(admin.ModelAdmin):
	list_display = ('collector_ID','fullname','terminalID','phone_number','age','gender','residential_address','Nationality',
			'contact_Of_Next_Of_Kin','date_added','date_updated')
	list_filter = ('date_added','gender')
	search_fields = ('fullname','^terminalID__terminal_serial_no','contact_Of_Next_Of_Kin')
	#inlines = [TransactionInline]
        ordering = ('-date_added',)
	readonly_fields  = ('collector_ID','age')






class CustomerAdmin(admin.ModelAdmin):
	list_display =('customerID','account_number','fullname','telephone','address','age','gender','Nationality','residential_address','contact_Of_Next_Of_Kin','date_added','date_updated',)
	list_filter = ('date_added','gender')
	search_fields = ('account_number','fullname','contact_Of_Next_Of_Kin')
	
	#inlines = [TransactionInline]
	ordering = ('-date_added',)
	readonly_fields    = ('customerID','age')


	
class SavingAdmin(admin.ModelAdmin):
	list_display =('savingID','customer_name','savingsAmount','date_created','date_updated',)
	list_filter = ('date_created',)
	search_fields = ('savingID','^customer_name__fullname')
	
	#inlines = [TransactionInline]
	ordering = ('-date_created',)
	readonly_fields    = ('savingID',)


class LoanAdmin(admin.ModelAdmin):
	list_display =('loanID','customer_name','loanAmount','amountToPay','amountPaid','amtLeftToPay','status','date_created','date_updated',)
	list_filter = ('date_created','status')
	search_fields = ('loanID','^customer_name__fullname','status')
	
	#inlines = [TransactionInline]
	ordering = ('-date_created',)
	readonly_fields    = ('loanID','status')


class TransactionAdmin(admin.ModelAdmin):
	list_display=('transaction_type','transaction_id','customer_name','paymentAmount',
			'collector_name','date_created','date_updated')
	list_filter = ('date_created','transaction_type')
	search_fields = ('transaction_type','^customer_name__fullname','^collector_name__fullname','company')
	list_filter = ('date_created','transaction_type')
	search_fields = ('transaction_type','^customer_name__fullname','^collector_name__fullname')
	ordering = ('-date_created',)
	readonly_fields    = ('transaction_type','transaction_id','customer_name','paymentAmount',
			'collector_name','date_created','date_updated')


class TerminalAdmin(admin.ModelAdmin):
	list_display = ('terminal_serial_no','terminal_id','date_added','date_updated')
	list_filter = ('terminal_id','terminal_serial_no')
	search_fields = ('terminal_id','terminal_serial_no')
	ordering = ('-date_added',)	
	readonly_fields  = ('terminal_id',)

admin.site.register(Supervisor)
admin.site.register(PoweredBy,PoweredByAdmin)
admin.site.register(Terminal,TerminalAdmin)
admin.site.register(Collector,CollectorAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Loans,LoanAdmin)
admin.site.register(Savings,SavingAdmin)

