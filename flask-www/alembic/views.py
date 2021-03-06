from alembic import app
from flask import request, redirect, render_template
from alembicconfig import API_KEY
from util.pagination import Pagination
import urllib

from fbopen import fbopen

def search(searchterm, advanced={}):
    fbos = fbopen.FBOpen

    fbos.init(API_KEY)
    results = fbos.Opp.search(searchterm, advanced)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/', defaults={'page': 1})
@app.route('/search/page/<int:page>')
def searchpage(page):
    items_per_page = 10
    if request.args and request.args['search']:
        searchterm = request.args['search']
        advanced = {field:value for field, value in request.args.items()
                    if value and field is not 'search'}
    else:
        return render_template(
        'search.html', searchterm = False,
        results = False, docs = False, pagination = False)

    #to save having to construct this in the template
    searchparams = "?"+urllib.parse.urlencode(advanced)

    start = page * items_per_page
    advanced['start'] = start

    results = search(searchterm, advanced)

    try:
        docs = results.opps
    except:
        docs = False

    if docs:
        count = results.numFound
        pagination = Pagination(page, items_per_page, count)
    else: pagination = False

    return render_template('search.html', searchterm = searchterm,
                            searchparams = searchparams, results = results,
                            docs = docs, pagination = pagination) 