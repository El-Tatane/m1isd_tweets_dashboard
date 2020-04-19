function fill_result(data) {
    console.log("fill result");
    console.log(data);
    document.getElementById("res").innerHTML = data;
}

function search() {
    let serve = new Orchestrator();
    serve.get_data('job/tweet_count', undefined, fill_result);
 }
