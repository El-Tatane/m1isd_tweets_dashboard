class Routes {
    constructor(url, values=undefined) {
        this.url = url;
        this.values = values;
    }

    get_route() {
        let route = this.url;
        let bool = true;
        if (typeof this.values !== 'undefined'){
            for (const param in this.values) {
                if (bool) {
                    let x = param.concat('=', this.values[param]);
                    route = route.concat('?', x);
                    bool = false;
                } else {
                    let x = param.concat('=', this.values[param]);
                    route = route.concat('&', x);
                }
            }
         }
        console.log("ROUTE JAVASCRIPT :")
        console.log(route)
        return route;
    }
}