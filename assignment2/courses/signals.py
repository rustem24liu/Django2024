
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment
import logging
from django.core.cache import cache
# Get the logger for course activity
logger = logging.getLogger('course_activity')

@receiver(post_save, sender=Enrollment)
def log_course_enrollment(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Student {instance.student.user.username} enrolled in course: {instance.course.name}")


logger = logging.getLogger('cache_activity')

def cache_with_logging(key, timeout=60*15):
    cached_value = cache.get(key)
    if cached_value:
        logger.debug(f"Cache hit for key: {key}")
        return cached_value
    else:
        logger.debug(f"Cache miss for key: {key}")
        result = "some expensive computation"
        cache.set(key, result, timeout)
        return result
