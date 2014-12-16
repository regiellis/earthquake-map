/**
 * Earthquakes - Data Worker
 */

data_fetch = function _data_fetch(url, type, params, func, undefined) {
    var params = params || undefined;
    if (typeof XMLHttpRequest !== undefined) {
        xhr = new XMLHttpRequest();
    }
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            func.apply(this, xhr);
        }
    }
    if (type == 'get')  {
        xhr.open('GET', url, true)
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(null);
    }
    if (type == 'post') {
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(params);
    }
}

onmessage = function _postMessage(evt) {
    data_fetch(evt.data[0], evt.data[1], evt.data[2], function() {
        postMessage(JSON.parse(this.response));
    });
}



