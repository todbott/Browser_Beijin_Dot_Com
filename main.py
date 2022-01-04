# -*- coding: utf-8 -*-

# ---------------------------------------- Imports FLASK and some utilities -----------------------------------------------------
from flask import Flask, request, redirect, render_template, session, send_from_directory
import os
import sys
import random
from google.cloud import storage
sys.path.insert(1, 'C:\\Users\\QRG_02\\Desktop\\mk_standard_env(2.7)\\lib\\')







def pickakey(keys):
    
    key_list = keys.split(",")
    this_key = key_list[random.randint(1,10000)]
    
    return this_key



def GCWGpickakey():
    
    client = storage.Client()

    bucket = client.get_bucket('sdl_glossaries')

    blob = bucket.get_blob('GCWG_keys.txt')
    
    key_list_string = blob.download_as_string() # here it is "key,key,key"
    key_list = key_list_string.split(",")       # split into ['key', 'key', 'key']
    this_key = key_list[0]                      # get the 1st one
    del key_list[0]                             # delete the 1st one
    key_list_string = ",".join(key_list)        # rejoin into "key,key"
    blob.upload_from_string(key_list_string)    # upload
    
    return this_key






# ---------------------------------------- Imports STRIPE ---------------------------------------------------------------
import stripe


stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']















# ---------------------------------------- Flask setup ---------------------------------------------------------------
app = Flask(__name__, static_folder='static')  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



           







#-------------------------------------------------- Start of webpage hierarchy -----------------------------------------#
@app.before_request
def force_https():
    if request.endpoint in app.view_functions and request.headers.get('X-Forwarded-Proto', None) == 'http':
        return redirect(request.url.replace('http://', 'https://'))
    
@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *\nDisallow:"







@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    
@app.route('/tmx_to_chart', methods=['GET', 'POST'])
def tmx_to_chart():
    return render_template('tmx_to_chart.html')  

@app.route('/tbtm_align', methods=['GET', 'POST'])
def tbtm_align():
    return render_template('tbtm_align.html')

@app.route('/otf_glossary', methods=['GET', 'POST'])
def otf_glossary():
    return render_template('otf_glossary.html')

@app.route('/iem', methods=['GET', 'POST'])
def iem():
    return render_template('iem.html')

@app.route('/gcwg', methods=['GET', 'POST'])
def gcwg():    
    return render_template('gcwg.html')
    
@app.route('/ppsg', methods=['GET', 'POST'])
def ppsg():    
    return render_template('ppsg.html')
    
@app.route('/blog', methods=['GET', 'POST'])
def blog():    
    return render_template('blog.html')
    
@app.route('/sitemap.xml', methods=['GET', 'POST'])
def sitemap():    
    return "<?xml version='1.0' encoding='UTF-8'?><urlset      xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'      xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'      xsi:schemaLocation='http://www.sitemaps.org/schemas/sitemap/0.9            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'><!-- created with Free Online Sitemap Generator www.xml-sitemaps.com --><url>  <loc>http://www.browser-beijin.com/</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>1.00</priority></url><url>  <loc>http://www.browser-beijin.com/blog</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>0.80</priority></url><url>  <loc>http://www.browser-beijin.com/tbtm_align</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>0.80</priority></url><url>  <loc>http://www.browser-beijin.com/otf_glossary</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>0.80</priority></url><url>  <loc>http://www.browser-beijin.com/iem</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>0.80</priority></url><url>  <loc>http://www.browser-beijin.com/gcwg</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>0.80</priority></url><url>  <loc>http://www.browser-beijin.com/ppsg</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>0.80</priority></url><url>  <loc>http://www.browser-beijin.com/tmx_to_chart</loc>  <lastmod>2020-03-12T23:23:35+00:00</lastmod>  <priority>0.80</priority></url></urlset>"







@app.route('/charge', methods=['GET', 'POST'])
def charge(): 
    
    language = session['language']
    key_type = session['type']
        
    if request.method == 'POST':
    
        customer = stripe.Customer.create(
            email=request.form['stripeEmail']
        )
        
        customer.sources.create(source=request.form['stripeToken'])
    
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=2500,
            currency='usd',
            description='Browser-beijin Plugins Product Key'
        )
        

        if (key_type == 'gcwg'):
            your_key = GCWGpickakey()
            
        return render_template('key_page.html', language = language, key = your_key, key_type = key_type, stripe_key=stripe_keys['publishable_key'])
            





    
@app.route('/en/TBTM_Align_key', methods=['GET', 'POST'])
def entbtm_align_key():
    
    session['language'] = 'en'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "en", key = "", key_type = 'tbtm', stripe_key=stripe_keys['publishable_key'])

@app.route('/jp/TBTM_Align_key', methods=['GET', 'POST'])
def jptbtm_align_key():
    
    session['language'] = 'jp'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "jp", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ru/TBTM_Align_key', methods=['GET', 'POST'])
def rutbtm_align_key():
    
    session['language'] = 'ru'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "ru", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ko/TBTM_Align_key', methods=['GET', 'POST'])
def kotbtm_align_key():
    
    session['language'] = 'ko'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "ko", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])

@app.route('/zh/TBTM_Align_key', methods=['GET', 'POST'])
def zhtbtm_align_key():
    
    session['language'] = 'zh'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "zh", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])

@app.route('/es/TBTM_Align_key', methods=['GET', 'POST'])
def estbtm_align_key():
    
    session['language'] = 'es'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "es", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])

@app.route('/fr/TBTM_Align_key', methods=['GET', 'POST'])
def frtbtm_align_key():
    
    session['language'] = 'fr'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "fr", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])

@app.route('/de/TBTM_Align_key', methods=['GET', 'POST'])
def detbtm_align_key():
    
    session['language'] = 'de'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "de", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])

@app.route('/it/TBTM_Align_key', methods=['GET', 'POST'])
def ittbtm_align_key():
    
    session['language'] = 'it'
    session['type'] = 'tbtm'
    
    return render_template('key_page.html', language = "it", key = "", key_type = 'tbtm',  stripe_key=stripe_keys['publishable_key'])








@app.route('/en/OTF_Glossary_key', methods=['GET', 'POST'])
def enOTF_Glossary_key():
    
    session['language'] = 'en'
    session['type'] = 'otf'
        
    return render_template('key_page.html', language = "en", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/jp/OTF_Glossary_key', methods=['GET', 'POST'])
def jpOTF_Glossary_key():
    
    session['language'] = 'jp'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "jp", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ru/OTF_Glossary_key', methods=['GET', 'POST'])
def ruOTF_Glossary_key():
    
    session['language'] = 'ru'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "ru", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ko/OTF_Glossary_key', methods=['GET', 'POST'])
def koOTF_Glossary_key():
    
    session['language'] = 'ko'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "ko", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/zh/OTF_Glossary_key', methods=['GET', 'POST'])
def zhOTF_Glossary_key():
    
    session['language'] = 'zh'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "zh", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/es/OTF_Glossary_key', methods=['GET', 'POST'])
def esOTF_Glossary_key():
    
    session['language'] = 'es'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "es", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/fr/OTF_Glossary_key', methods=['GET', 'POST'])
def frOTF_Glossary_key():
    
    session['language'] = 'fr'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "fr", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/de/OTF_Glossary_key', methods=['GET', 'POST'])
def deOTF_Glossary_key():
    
    session['language'] = 'de'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "de", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])

@app.route('/it/OTF_Glossary_key', methods=['GET', 'POST'])
def itOTF_Glossary_key():
    
    session['language'] = 'it'
    session['type'] = 'otf'
    
    return render_template('key_page.html', language = "it", key = "", key_type = 'otf',  stripe_key=stripe_keys['publishable_key'])











@app.route('/en/Crawl_n_Search_key', methods=['GET', 'POST'])
def enCrawl_n_Search_key():
    
    session['language'] = 'en'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "en", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/jp/Crawl_n_Search_key', methods=['GET', 'POST'])
def jpCrawl_n_Search_key():
    
    session['language'] = 'jp'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "jp", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ru/Crawl_n_Search_key', methods=['GET', 'POST'])
def ruCrawl_n_Search_key():
    
    session['language'] = 'ru'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "ru", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ko/Crawl_n_Search_key', methods=['GET', 'POST'])
def koCrawl_n_Search_key():
    
    session['language'] = 'ko'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "ko", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/zh/Crawl_n_Search_key', methods=['GET', 'POST'])
def zhCrawl_n_Search_key():
    
    session['language'] = 'zh'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "zh", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/es/Crawl_n_Search_key', methods=['GET', 'POST'])
def esCrawl_n_Search_key():
    
    session['language'] = 'es'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "es", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/fr/Crawl_n_Search_key', methods=['GET', 'POST'])
def frCrawl_n_Search_key():
    
    session['language'] = 'fr'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "fr", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/de/Crawl_n_Search_key', methods=['GET', 'POST'])
def deCrawl_n_Search_key():
    
    session['language'] = 'de'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "de", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])

@app.route('/it/Crawl_n_Search_key', methods=['GET', 'POST'])
def itCrawl_n_Search_key():
    
    session['language'] = 'it'
    session['type'] = 'iem'
    
    return render_template('key_page.html', language = "it", key = "", key_type = 'iem',  stripe_key=stripe_keys['publishable_key'])









@app.route('/en/GCWG_key', methods=['GET', 'POST'])
def enGCWG_key():
    
    session['language'] = 'en'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "en", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/jp/GCWG_key', methods=['GET', 'POST'])
def jpGCWG_key():
    
    session['language'] = 'jp'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "jp", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ru/GCWG_key', methods=['GET', 'POST'])
def ruGCWG_key():
    
    session['language'] = 'ru'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "ru", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/ko/GCWG_key', methods=['GET', 'POST'])
def koGCWG_key():
    
    session['language'] = 'ko'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "ko", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/zh/GCWG_key', methods=['GET', 'POST'])
def zhGCWG_key():
    
    session['language'] = 'zh'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "zh", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/es/GCWG_key', methods=['GET', 'POST'])
def esGCWG_key():
    
    session['language'] = 'es'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "es", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/fr/GCWG_key', methods=['GET', 'POST'])
def frGCWG_key():
    
    session['language'] = 'fr'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "fr", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/de/GCWG_key', methods=['GET', 'POST'])
def deGCWG_key():
    
    session['language'] = 'de'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "de", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])

@app.route('/it/GCWG_key', methods=['GET', 'POST'])
def itGCWG_key():
    
    session['language'] = 'it'
    session['type'] = 'gcwg'
    
    return render_template('key_page.html', language = "it", key = "", key_type = 'gcwg',  stripe_key=stripe_keys['publishable_key'])


    
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)