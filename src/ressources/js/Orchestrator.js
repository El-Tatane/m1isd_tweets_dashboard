class Orchestrator {
    constructor() {
        this.serverUrl = "http://localhost:80";
    }

    makeAjaxCall(url, methodType) {
        return new Promise(function (resolve, reject) {
            let xhr = new XMLHttpRequest();
            xhr.open(methodType, url, true);
            xhr.send();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        resolve(JSON.parse(xhr.responseText));
                    } else {
                        reject(xhr.status);
                        console.log("xhr failed");
                    }
                } else {
                    console.log("xhr processing going on");
                }
            };
            console.log("request sent succesfully");
        });
    }

    get_data(route, params, callback) {

        /* Pipeline :
            - Launch treatment and get id_job
                -> while result unavailable : retry get_job_result
            - Callback to write result
        */
        const complete_route = new Routes(this.serverUrl.concat('/', route), params).get_route();
        this.launch_treatment(complete_route)
            .then(result => this.check_result(result))
            .then(result => callback(result));
    }

    launch_treatment(url){
        return new Promise(function (resolve, reject) {
            this.makeAjaxCall(url, "GET").then( function (dict_result) {
                resolve(dict_result["id_job"]);
            });
        }.bind(this));
    }

    get_job_result(id_job) {
        const complete_route = new Routes(this.serverUrl.concat('/job/result?id=', id_job)).get_route();
        return new Promise(function (resolve, reject) {
            this.makeAjaxCall(complete_route, "GET").then(function (ajax_result) {
                resolve(ajax_result[id_job])
            })
        }.bind(this));
    }

    check_result(id_job) {
        return this.get_job_result(id_job).then(function(result) {
            if (result !== undefined){
                if (result === "Started") {
                    // job not finish
                    return this.later(1000).then( () => this.check_result(id_job))

                } else {
                    // job finish
                    return result;
                }
            }else{
                return("ERROR JOB NOT EXIST")
            }
        }.bind(this));
    }

    later(delay, value) {
    return new Promise(function(resolve) {
        setTimeout(resolve, delay);
    });
}

}
