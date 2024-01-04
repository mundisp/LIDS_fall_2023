from django.apps import AppConfig
from threading import Thread


class ServerThread(Thread):
    def run(self):
        print("Thread running")

class StackConfig(AppConfig):

    def ready(self):
        from DJANGO.LIDS_D.dashboard.backend.lidsd_connect import serverMain
        ServerThread().start()
    name = 'stack'

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
