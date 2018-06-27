from django.utils import timezone
from datetime import datetime, date, time, timedelta

def days_ago(days):
  return timezone.now() - timedelta(hours=24*days)