let serve = new Orchestrator();

function fill_tweet_count() {
    serve.get_data('job/tweet_count', get_filter_data(), function(data) {
         document.getElementById("nb_total_tweet").innerHTML = data;
    })
}

function fill_country_count() {
    serve.get_data('job/country_count', get_filter_data(), function(data) {
         document.getElementById("nb_total_country").innerHTML = data;
    })
}

function fill_user_name_count() {
    serve.get_data('job/user_name_count', get_filter_data(), function(data) {
         document.getElementById("nb_total_user_name").innerHTML = data;
    })
}

function fill_lang_count() {
    serve.get_data('job/lang_count', get_filter_data(), function(data) {
         document.getElementById("nb_total_lang").innerHTML = data;
    })
}

function fill_ts_start() {
    serve.get_data('job/ts_start', get_filter_data(), function(data) {
         document.getElementById("span_ts_start").innerHTML = ts_to_datetime(data);
    })
}

function fill_ts_end() {
    serve.get_data('job/ts_end', get_filter_data(), function(data) {
         document.getElementById("span_ts_end").innerHTML = ts_to_datetime(data);
    })
}

function fill_tweet_contain(){ // add ten_number
        serve.get_data('job/tweet_contain', Object.assign({}, get_filter_data(), {"ten_number": 0}), function(data) {
            console.log(data);
            let tbody = document.getElementById("table_list_tweet");
            tbody.innerHTML = "";
            for (const row_data of data){
                let row_html = document.createElement("tr");
                for (const col of ["user_name", "timestamp", "text"]) {
                    let cell = document.createElement("td");
                    if (col ==="timestamp"){
                        cell.innerHTML = ts_to_datetime(row_data[col]);
                    }else{
                        cell.innerHTML = row_data[col];
                    }
                    row_html.appendChild(cell);
                }
                tbody.appendChild(row_html)
            }
    })
}

function update_all() {

    fill_tweet_count();
    fill_country_count();
    fill_user_name_count();
    fill_lang_count();
    fill_ts_start();
    fill_ts_end();
    fill_tweet_contain();
 }
