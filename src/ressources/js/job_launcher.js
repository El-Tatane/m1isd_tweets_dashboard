let serve = new Orchestrator();

function fill_tweet_count() {
    serve.get_data('job/tweet_count', get_filter_data(), function(data) {
         document.getElementById("nb_total_tweet").innerHTML = data;
         document.getElementById("span_tweet_navigate_max").innerHTML = (Math.floor(parseInt(data) / 10)).toString();
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
        if (data === "."){
             document.getElementById("span_ts_start").innerHTML = ".";
        }else{
             document.getElementById("span_ts_start").innerHTML = ts_to_datetime(data);
        }
    })
}

function fill_ts_end() {
    serve.get_data('job/ts_end', get_filter_data(), function(data) {
        if (data === "."){
            document.getElementById("span_ts_end").innerHTML = ".";
        }else{
            document.getElementById("span_ts_end").innerHTML = ts_to_datetime(data);
        }
    })
}

function fill_tweet_contain(ten_number_action= "start"){
    // first tweets => "start", before ten tweets => "before", next ten tweets => "next",  last tweets => "end"

        let ten_number = get_correct_ten_number(ten_number_action);
        serve.get_data('job/tweet_contain', Object.assign({}, get_filter_data(), {"ten_number": ten_number}), function(data) {
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
            if (ten_number === -1){
                ten_number = document.getElementById("span_tweet_navigate_max").innerHTML
            }
            document.getElementById("span_tweet_navigate_start").innerHTML = ten_number.toString();
    })
}

function get_correct_ten_number(ten_number_action){
    if (ten_number_action === "start") {
        return 0;
    } else {
        let actual_pos = parseInt(document.getElementById("span_tweet_navigate_start").innerHTML);
        let max_pos = parseInt(document.getElementById("span_tweet_navigate_max").innerHTML);

        switch (ten_number_action) {
            case "before":
                return Math.max(0, actual_pos - 1) ;
            case "next":
                return Math.min(max_pos, actual_pos + 1);
            case "last":
                return -1;
        }
    }
}

function fill_country_repartition() {
    serve.get_data('job/country_repartition', get_filter_data(), function(data) {
         // data [(longitude, latitude, count), ...]
        map(data, "canvas_map");
    })
}

function fill_lang_repartition() {
    serve.get_data('job/lang_repartition', get_filter_data(), function(data) {
         // data {lang: count}
        pie(data, "canvas_pie");
    })
}

function fill_hastag_repartition() {
    serve.get_data('job/hashtag_repartition', get_filter_data(), function(data) {
         // data {hashtag: count}
        hist(data, "canvas_hist", "tweet hashtag", "tweet percentage", "Best 6 tweets percentage", 6);
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
    fill_country_repartition();
    fill_lang_repartition();
    fill_hastag_repartition();
 }
