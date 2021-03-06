function get_filter_data() {
    let list_filter_id = ["user_name", "place_country", "user_followers_count", "lang", "ts_start", "ts_end",
                          "hashtag", "text"];
    let filters = {};

    for (const filter_id of list_filter_id) {
        let value = document.getElementById(filter_id).value;
        if (value !== "") {
            if (filter_id === "ts_start" || filter_id === "ts_end"){
                filters[filter_id] = datetime_to_ts(value)
            }else{
                filters[filter_id] = value;
            }
        }
    }
    console.log("filters :", filters);
    return filters;
}

function ts_to_datetime(ts) {
    let date = new Date(ts * 1000);

    return ('0' + date.getDate()).slice(-2) + "/" + ('0' + (date.getMonth()+1)).slice(-2) + "/" + date.getFullYear() + " "
    + ('0' + date.getHours()).slice(-2) + ":" + ('0' + date.getMinutes()).slice(-2);
}

function datetime_to_ts(dateString) {
    // format dd/mm/YYYY HH:MM
    let dateTimeParts = dateString.split(' ');
    let timeParts = dateTimeParts[1].split(':');
    let dateParts = dateTimeParts[0].split('/');

    let date = new Date(dateParts[2], parseInt(dateParts[1], 10) - 1, dateParts[0], timeParts[0], timeParts[1]);

    return Math.floor(date.getTime() / 1000);
}