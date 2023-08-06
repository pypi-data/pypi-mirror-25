# -*- coding: utf-8 -*-
from .routers import router
from ..autodiscover import autodiscover


autodiscover()

urlpatterns = router.urls
