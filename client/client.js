function modifyText() {
    var tweet_search = document.getElementById("search").value;
    document.getElementById("tweet").innerHTML = tweet_search;
    const tweet = String(tweet_search).split(" ");
    for (i=0; i<tweet.length; i++){

    }
    var value1 = encodeURIComponent(String(tweet_search));
    var xhr = new XMLHttpRequest();
    xhr.open('GE T', 'localhost?param1=' + value1, true);
    xhr.send(null);
    xhr.addEventListener('readystatechange', function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

        }
    });
}

/**
 * exemple : url = localhost:80/test , values ={name : t; age : 12}
 * return : localhost:80/test?name=t&age=12
 */
class Routes {
    constructor(url, values) {
        this.url = url;
        this.values = values;
    }

    get_route(){
        var route = this.url;
        var bool = true;
        for(const param in this.values){
            if (bool){
                let x =  param.concat('=', this.values[param]);
                route = route.concat('?', x);
                bool = false;
            }
            else{
                let x =  param.concat('=', this.values[param]);
                route = route.concat('&', x);
            }
        }
        return route;
    }
}






/**with GET
var value1 = encodeURIComponent('value1');
xhr.open('GET', 'serverUrl/ajax.php?param1=' + value1 + '&param2=' + value2);
 **/

/**with POST
xhr.open('POST', 'http://mon_site_web.com/ajax.php');
xhr.send('param1=' + value1 + '&param2=' + value2);
 **/

/** pour l'asynchrone une fois que la réponse du serveur est prete
xhr.addEventListener('readystatechange', function() {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

    }
});
 **/
