class Orchestrator {
    constructor() {
        this.serverUrl = "http://localhost:80";
    }

    makeAjaxCall(url, methodType) {
        let promiseObj = new Promise(function (resolve, reject) {
            let xhr = new XMLHttpRequest();
            xhr.open(methodType, url, true);
            xhr.send();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        console.log("xhr done successfully");
                        let resp = xhr.responseText;
                        let respJson = JSON.parse(resp);
                        resolve(respJson);
                    } else {
                        reject(xhr.status);
                        console.log("xhr failed");
                    }
                } else {
                    console.log("xhr processing going on");
                }
            }
            console.log("request sent succesfully");
        });
        return promiseObj;
    }

    get_data(route, params) {
        const complete_route = new Routes(this.serverUrl.concat('/', route), params).get_route();
        this.makeAjaxCall(complete_route, "GET").then(this.get_job_result());

        //GET ID_JOB
        //check result is ready
        //
    }

    get_job_result(id_job) {
        const complete_route = new Routes(this.serverUrl.concat('?id=', id_job)).get_route();
        return this.makeAjaxCall(complete_route, "GET").then(function (result) {

        })
    }

    action() {
        let data = {};
        return promise
            .then(function () {

            })
            .then(function (sum) {
                console.log('sum =', sum);
            })
            .then(function printXandY() {
                // now use x and y
                console.log('x =', data.x, 'y =', data.y);
            });
    }
}