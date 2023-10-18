import os

########################################
#               runserver              #
########################################
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py runserver")


########################################
#               startapp               #
########################################
# os.system("python manage.py startapp users")
# os.system("python manage.py startapp chat")


########################################
#           create superuser           #
########################################
# email: heatingma@sjtu.edu.cn
# username: heatingma
# password: see in the super_psw.docx
# os.system("python manage.py createsuperuser")


########################################
#             collectstatic            #
########################################
# os.system("python manage.py collectstatic")