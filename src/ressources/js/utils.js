function get_filter_data() {
    let list_filter_id = ["user_name", "place_country", "user_followers_count", "lang", "ts_start", "ts_end",
                          "hashtag"];
    let filters = {};

    for (const filter_id of list_filter_id) {
        let value = document.getElementById(filter_id).value;
        if (value !== "") {
            filters[filter_id] = value;
        }
    }
    return filters;
}

function fill_result(data) {
    document.getElementById("res").innerHTML = data;
}

function search() {
    let serve = new Orchestrator();
    serve.get_data('job/tweet_count', get_filter_data(), fill_result);

 }
