#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'buzzmonclick_com'
SITE_NAME = 'buzzmonclick.com'
SITE_DESC = 'Film Streaming & Serie Streaming: Regardez films et series de qualité entièrement gratuit. Tout les meilleurs streaming en illimité.'
 
URL_MAIN = 'http://buzzmonclick.com/category/replay-tv/'
 
REPLAYTV_REPLAYTV = ('http://buzzmonclick.com/category/replay-tv/', 'showMovies')
DOC_DOCS = ('http://buzzmonclick.com/category/replay-tv/documentaires/', 'showMovies')

 
 
URL_SEARCH = ('http://buzzmonclick.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Films Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautes', 'films.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showMoviesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://buzzmonclick.com/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   
 
 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
	
    liste.append( ['divertissement','http://buzzmonclick.com/category/replay-tv/divertissement/'] )
    liste.append( ['infos','http://buzzmonclick.com/category/replay-tv/infos-magazine/page/2/'] )
    liste.append( ['series','http://buzzmonclick.com/category/replay-tv/series-tv/'] )
    liste.append( ['tele realite','http://buzzmonclick.com/category/replay-tv/tele-realite/'] )
   
 
    for sTitle,sUrl in liste:
 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    sPattern = 'data-id="[0-9]+" title="([^<]+)" href="([^<]+)"><span class="clip"><img src="([^<]+)" alt="'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = unicode(aEntry[0], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            #sTitle = unescape(str(sTitle))
            sTitle = sTitle.encode( "utf-8")
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
           
            print aEntry[2]
           
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[2], aEntry[2], oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl
 
    return False
 
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = 'iframe src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    #print aResult
 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sHosterUrl = str(aEntry)
 
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
 
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
