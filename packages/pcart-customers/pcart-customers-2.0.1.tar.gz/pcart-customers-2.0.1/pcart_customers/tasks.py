from celery import task


# Run this task automatically every 12 hour
@task.periodic_task(run_every=60*60*12)
def clean_old_anonymous_customers():
    from .utils import clean_old_anonymous_customers
    clean_old_anonymous_customers()
