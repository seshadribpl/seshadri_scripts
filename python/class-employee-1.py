class employee:
	raise_amt = 1.3
	def __init__(self,first,last,pay):
		self.first = first
		self.last = last
		self.pay = pay
		self.email = first + '.' + last + '@company.com'
		print 'the name is: %s %s' %(self.first, self.last)
		print 'the email ID is: %s' %self.email
		print 'the pay is: %s' %self.pay
		print 'the new pay is %s x' %employee.raise_amt

	#	employee.num_of_emps += 1
		# print 'the total number of employees: %s' %employee.emp_count

	def fullname(self):
		return '{} {}'.format(self.first, self.last)

	def income(self):
		print 'the current pay is %s' %self.pay
		# return self.pay

	def email(self):
		print 'Email ID is: %s' %self.email
		# return self.email

	def apply_raise(self):
		new_pay = int(self.pay) * self.raise_amt
		print 'the new pay is %s '  %self.new_pay
		return '{}'.format(self.pay)

	@classmethod
	def from_string(cls, emp_str):
		first, last, pay = emp_str.split('-')
		return cls(first,last,pay)


# emp1 = employee('raju', 'gentleman', 50000)
# emp2 = employee('munna', 'bhai', 40000)

# print emp1.fullname()
# print emp1.income()
# print emp1.apply_raise()
# print(employee.num_of_emps)

# print emp2.fullname()
# print emp2.income()
# print emp2.apply_raise()
emp3_str = 'John-Doe-90000'

first, last, pay = emp3_str.split('-')
emp3 = employee(first,last,pay)
# print emp3.apply_raise()
print emp3.fullname()
print emp3.apply_raise()