function fill_result(data) {
    document.getElementById("res").innerHTML = data;
}

function search() {
    let serve = new Orchestrator();
    serve.get_data('job/tweet_count', undefined, fill_result);
    t = document.getElementById("username").value
    console.log(t)
 }
