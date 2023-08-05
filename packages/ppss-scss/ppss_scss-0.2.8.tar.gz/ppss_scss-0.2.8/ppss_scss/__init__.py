sourcedir = 'scss/'
routepath = '/css'
workingfolder = '/tmp'
import logging
l = logging.getLogger(__name__)


def includeme(config):
    global sourcedir,routepath,workingfolder
    settings = config.get_settings()
    sourcedir = settings.get('ppss_scss.srcdir','scss/')
    routepath = settings.get('ppss_scss.routepath','/css/*fizzle')
    workingfolder = settings.get('ppss_scss.workingfolder','/tmp/css/')
    
    l.info("ppss_scss.sorucedir={src} ppss_scss.routepath = {route}".format(src=sourcedir,route=routepath))
    config.add_route('ppss_scss_compile', routepath)
    config.scan()