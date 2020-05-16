function fill_result(data) {
    // document.getElementById("res").innerHTML = JSON.stringify(data);
    // circle();

    let tweet_data = JSON.parse(data)
    let tweet_country = tweet_data["place_country"]
    let tweet_country_count = tweet_categorical_count(tweet_country)
    pie(tweet_country_count, "canvas");
    hist(tweet_country_count, "canvas2", "Countries", "tweet percentage %", "test title")
    let map_values = [[-8.143229, 52.479842], [2.340193, 48.858139]]
    map(map_values)
    console.log(tweet_data)
    console.log(tweet_country)
    console.log(tweet_country_count)
}

function search() {
    let serve = new Orchestrator();
    let dict_values = new Object();

    let filter_values = ["user_name", "place_country", "user_followers_count", "lang", "hashtag", "text"]

    // we get the values from the modal
    for(let i=0; i<filter_values.length; i++){
        let value = document.getElementById(filter_values[i]).value.split(", ");
        if (value != ""){
            dict_values[filter_values[i]] = value;
        }
    }
    let ts_start = date_to_timestamp(document.getElementById("ts_start").value);
    let ts_end = date_to_timestamp(document.getElementById("ts_start").value);
    if(ts_start != undefined) {dict_values["ts_start"] = ts_start}
    if(ts_end != undefined) {dict_values["ts_end"] = ts_end}
    console.log("DICT VALUES :")
    console.log(dict_values)

    serve.get_data('job/tweet_count', dict_values, fill_result);
 }

 function date_to_timestamp(date){
    let s = date.split("/")
    if(s.length>1) return (new Date(Date.UTC(s[2],(s[0]*1-1),s[1]*1+1,0,0,0)).getTime()/1000.0);
 }

function tweet_categorical_count(dict){
    let tweet_country_count = {}
    for (let [key, value] of Object.entries(dict)){
        tweet_country_count[value]=(tweet_country_count[value] || 0) + 1;
    }
    return tweet_country_count;
}


function canvas_data(dict_values){
    let datalist= new Array();
    let labels = new Array();
    let colist = new Array();
    for (let [key, value] of Object.entries(dict_values)){
        datalist.push(value);
        labels.push(key);
        let color ;
        do{
          color = "#"+Math.floor(Math.random()*16777215).toString(16);
        }while(color === "#000000")
        colist.push(color);
    }
    return [datalist, labels, colist]
}

function pie(dict_values, html_canvas_id){
  let data =  canvas_data(dict_values)
  let datalist= data[0]
  let labels = data[1]
  let colist = data[2]
  let canvas = document.getElementById(html_canvas_id);
  let ctx = canvas.getContext('2d');
  let w = canvas.width
  let h = canvas.height
  let radius = h / 3 ;
  let centerx = w / 2;
  let centery = h / 2;
  let lastend = 0;
  let labels_rec_x = centerx + radius + 10
  let labels_rec_y = 10

  let offset = Math.PI / 2;
  let labelxy = new Array();

  let fontSize = Math.floor(h / 33);
  ctx.textAlign = 'center';
  ctx.font = fontSize + "px Arial";
  let total = 0;
  for(let x=0; x < datalist.length; x++) { total += datalist[x]; };

  for(let x=0; x < datalist.length; x++)
  {
    let thispart = datalist[x];
    ctx.beginPath();
    ctx.fillStyle = colist[x];
    ctx.moveTo(centerx,centery);
    let percentage = (thispart * 100) / total;
    let arcsector = Math.PI * (2 * thispart / total);
    ctx.arc(centerx, centery, radius, lastend - offset, lastend + arcsector - offset, false);
    ctx.lineTo(centerx, centery);
    ctx.fill();
    ctx.closePath();
    if(thispart > (total / 20))
       labelxy.push(lastend + arcsector / 2 + Math.PI + offset);
    lastend += arcsector;
    ctx.beginPath();
    ctx.rect(labels_rec_x, labels_rec_y, 10, 10)
    ctx.fill();
    ctx.stroke();
    ctx.strokeStyle = "rgb(0,0,0)";
    ctx.fillStyle = "rgb(0,0,0)";
    ctx.textAlign = "left"
    ctx.fillText(labels[x] + '(' + percentage.toFixed(2) + '%)', labels_rec_x + 15, labels_rec_y + 10 )
    ctx.closePath();
    labels_rec_y += 20
  }
}

function hist(dict_values, html_canvas_id, x_label, y_label, title){
  let data =  canvas_data(dict_values)
  let datalist= data[0];
  let labels = data[1];
  let colist = data[2];
  let canvas = document.getElementById(html_canvas_id);
  let total = 0;
  for(let x=0; x < datalist.length; x++) { total += datalist[x]; };
  let x_marge_value = canvas.width * 0.15
  let y_marge_value = canvas.height * 0.15
  let ctx = canvas.getContext('2d');
  ctx.beginPath();
  ctx.moveTo(x_marge_value,canvas.height - y_marge_value);
  ctx.lineTo(x_marge_value,y_marge_value);
  ctx.moveTo(x_marge_value,canvas.height - y_marge_value);
  ctx.lineTo(canvas.width - x_marge_value,canvas.height - y_marge_value);
  ctx.stroke();
  let graph_y = (canvas.height - 2*y_marge_value)/11
  let y_pos = canvas.height - y_marge_value - graph_y

  for(let i=1; i<11; i++){
      ctx.beginPath();
      ctx.strokeStyle = "rgb(0,0,0)";
      ctx.fillStyle = "rgb(0,0,0)";
      ctx.textAlign = "right"
      let y_value = i*10
      ctx.fillText(y_value.toString(), x_marge_value - 10, y_pos)
      ctx.closePath();
      y_pos = y_pos - graph_y
  }
  ctx.font = "25px Arial";
  ctx.fillText(title, x_marge_value + (canvas.width - 2*x_marge_value)/2, y_pos)
  ctx.font = "15px Arial";
  ctx.fillText(y_label, x_marge_value - 10, y_pos)


  let rec_x = x_marge_value + 5
  let rec_y = canvas.height - y_marge_value
  let rect_width = (canvas.width - 2*x_marge_value)/datalist.length - 5*datalist.length
  let rect_height = graph_y*10 + 5
  for(let i=0; i <datalist.length; i++){
     let data_percentage = (datalist[i] * 100) / total
     let rect_data_height = data_percentage * rect_height / 100
     ctx.beginPath();
     ctx.fillStyle = colist[i]
     ctx.rect(rec_x, rec_y, rect_width, -rect_data_height)
     ctx.fill();
     ctx.closePath()
     ctx.textAlign = "center"
     ctx.fillText(labels[i], rec_x + (rect_width/2), rec_y + 20)
     rec_x = rec_x + 5 + rect_width
  }
  ctx.strokeStyle = "rgb(0,0,0)";
  ctx.fillStyle = "rgb(0,0,0)";
  ctx.font = "15px Arial";
  ctx.fillText(x_label, x_marge_value + (canvas.width - 2*x_marge_value)/2, canvas.height - y_marge_value + 40)
}

function map(list_values){
    let canvas = document.getElementById("canvas3")
    let ctx  = canvas.getContext("2d")
    let img = document.getElementById("source");
    // let img = new Image()
    // img.onload = function(){
    //     ctx.drawImage(this, 0, 0);
    // }
    // img.src = document.getElementById("map").src;
    ctx.drawImage(img, 0, 0, canvas.clientWidth, canvas.clientHeight);
    for (let i=0; i<list_values.length; i++){
        let longitude = list_values[i][0]
        let latitude = list_values[i][1]
        let latRad = latitude*Math.PI/180

        let x = (canvas.clientWidth * (longitude + 180 - 10)/360) // -10 is a correction, because the image was not correctly centred
        let y = canvas.clientHeight/2 - (canvas.clientWidth/(2*Math.PI) * Math.log(Math.tan((Math.PI/4) + (latRad/2))))
        ctx.beginPath();
        ctx.fillStyle="#FF4422"
        ctx.arc(x, y, 2, 0, 2 * Math.PI);
        ctx.fill()
    }
}



