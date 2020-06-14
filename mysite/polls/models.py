from django.db import models
import datetime
from django.utils import timezone


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
	
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
		
class Emp(models.Model):
    gender = (('male', "男"),('female', "女"),)
    #emp_sys_id = models.CharField(max_length=36)
    #emp_no = models.CharField(max_length=20)
    emp_name = models.CharField(max_length=30)
    emp_sex_id = models.CharField(max_length=32, choices=gender, default="男")
    emp_dpt_id = models.CharField(max_length=30)
    emp_status_id = models.CharField(max_length=30)
    emp_birthday = models.DateTimeField('birthday date')
    emp_id_no = models.CharField(max_length=20,unique=True)
    emp_remark = models.CharField(max_length=100)
    emp_card_type = models.IntegerField(default=0)
    emp_pwd=models.CharField(max_length=256)
    is_delete = models.CharField(max_length=1,default="N")
    is_tmp = models.CharField(max_length=1,default="N")
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.emp_name
    class Meta:
        ordering = ["-create_time"]
		
class Dpt(models.Model):
    #dpt_sys_id=models.CharField(max_length=36)
    #dpt_no = models.CharField(max_length=20)
    dpt_name = models.CharField(max_length=30,unique=True)
    dpt_parent_sys_id=models.CharField(max_length=36)
    dpt_desc = models.CharField(max_length=100)
    is_delete = models.CharField(max_length=1,default="N")
    is_tmp = models.CharField(max_length=1,default="N")
    dpt_manager_id=models.CharField(max_length=36)
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.dpt_name


class Empcard(models.Model):
    #gu_id=models.CharField(max_length=36)
    #card_sys_id = models.CharField(max_length=36)
    card_serial_no = models.CharField(max_length=20,unique=True)
    card_fix_id = models.CharField(max_length=36,unique=True)
    card_onwer_no = models.CharField(max_length=20)
    card_due_day = models.DateTimeField('due date')
    #card_disp_no = models.CharField(max_length=36)
    card_type_id = models.CharField(max_length=20)
    card_status_id = models.CharField(max_length=20)
    card_remark = models.CharField(max_length=100) 
    card_pwd=models.CharField(max_length=256)
    is_tmp = models.CharField(max_length=1,default="N")
    is_delete = models.CharField(max_length=1,default="N")
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.card_disp_no

class Area(models.Model):
    area_name = models.CharField(max_length=30,unique=True)
    area_remark = models.CharField(max_length=100)
    is_delete = models.CharField(max_length=1,default="N")
    is_tmp = models.CharField(max_length=1,default="N")
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.area_name
