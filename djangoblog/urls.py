"""djangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include

from djangoblog.admin_site import admin_site
from djangoblog.feeds import DjangoBlogFeed
from djangoblog import views
from djangoblog.sitemap import StaticViewSitemap, ArticleSiteMap, CategorySiteMap, TagSiteMap, UserSiteMap

sitemaps = {

    'blog': ArticleSiteMap,
    'Category': CategorySiteMap,
    'Tag': TagSiteMap,
    'User': UserSiteMap,
    'static': StaticViewSitemap
}

handler404 = 'blog.views.page_not_found_view'
handler500 = 'blog.views.server_error_view'
handle403 = 'blog.views.permission_denied_view'
urlpatterns = [
                  re_path(r'^admin/', admin_site.urls),
                  re_path(r'', include('blog.urls', namespace='blog')),
                  re_path(r'mdeditor/', include('mdeditor.urls')),
                  re_path(r'', include('comments.urls', namespace='comment')),
                  re_path(r'', include('accounts.urls', namespace='account')),
                  re_path(r'', include('oauth.urls', namespace='oauth')),
                  re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                      name='django.contrib.sitemaps.views.sitemap'),
                  re_path(r'^feed/$', DjangoBlogFeed()),
                  re_path(r'^rss/$', DjangoBlogFeed()),
                  re_path(r'^search', include('haystack.urls'), name='search'),
                  re_path(r'', include('servermanager.urls', namespace='servermanager')),
                  re_path(r'', include('owntracks.urls', namespace='owntracks')),
                  re_path(r'^id_decode', views.id_decode),
                  re_path(r'^id_encode', views.id_encode),
                  re_path(r'^decode', views.decode),
                  re_path(r'^encode', views.encode),
                  re_path(r'^wssdecode', views.wssdecode),
                  re_path(r'^sms', views.sms),
                  re_path(r'^save_json', views.save_json),
                  re_path(r'^get_json', views.get_json),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
