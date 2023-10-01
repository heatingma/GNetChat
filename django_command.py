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
# username: adminsjtu
# password: nis-3368
# os.system("python manage.py createsuperuser")


########################################
#             collectstatic            #
########################################
# os.system("python manage.py collectstatic")