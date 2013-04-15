$('document').ready(function() {
    queryParameters = getQueryParameters();
    curPage = parseInt(queryParameters['p']);
    if (isNaN(curPage)) {
        curPage = 1;
    }

    if (curPage-1 < 1) {
        // disable prev page link
        $('#prevpage').addClass('disabled');
    }
    if (curPage+1 > numPages) {
        // disable next page link
        $('#nextpage').addClass('disabled');
    }

    // highlight current page link
    cur_page = "#page_" + curPage;
    $(cur_page).addClass('active');
});

function getQueryParameters() {
    /*
     * queryParameters -> handles the query string parameters
     * queryString -> the query string without the fist '?' character
     * re -> the regular expression
     * m -> holds the string matching the regular expression
     * code excerpt from http://www.samaxes.com/2011/09/change-url-parameters-with-jquery/
     */
    var queryParameters = {}, queryString = location.search.substring(1),
        re = /([^&=]+)=([^&]*)/g, m;
     
    // Creates a map with the query string parameters
    while (m = re.exec(queryString)) {
        queryParameters[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
    }

    return queryParameters;
}

function updatePage(page) {
    queryParameters = getQueryParameters();

    // Add new parameters or update existing ones
    queryParameters['p'] = page;
     
    location.search = $.param(queryParameters); // Causes page to reload
}

function prevPage() {
    queryParameters = getQueryParameters();

    // Add new parameters or update existing ones
    pagenum = parseInt(queryParameters['p']);
    if (isNaN(pagenum)) {
        pagenum = 1;
    }

    if (pagenum-1 < 1) {
        return;
    }
    else {
        queryParameters['p'] = pagenum-1;
    }
     
    location.search = $.param(queryParameters); // Causes page to reload
}

function nextPage(numpages) {
    queryParameters = getQueryParameters();

    // Add new parameters or update existing ones
    pagenum = parseInt(queryParameters['p']);
    if (isNaN(pagenum)) {
        pagenum = 1;
    }

    if (pagenum+1 > numpages) {
        return;
    }
    else {
        queryParameters['p'] = pagenum+1;
    }

    location.search = $.param(queryParameters); // Causes page to reload
}
