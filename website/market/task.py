from celery.utils.log import get_task_logger
from django.db.models import F, Q


from market.models import Product
from website.celery import app

logger = get_task_logger(__name__)


@app.task
def make_5_percent_discount():
    print('123')
    Product.objects.filter(Q(available=True) & Q(stock__lte=10)).update(price=F('price') * 0.95)
    logger.info(Product.objects.filter(Q(available=True) & Q(stock__lte=10)).update(price=F('price') * 0.95).query)
    return 'asd'
