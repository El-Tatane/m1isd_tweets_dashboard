function sortProperties(dict, best_values_number) {
    // Create items array
    let items = Object.keys(dict).map(function(key) {
         return [key, dict[key]];
    });

    // Sort the array based on the second element
    items.sort(function(first, second) {
        return second[1] - first[1];
    });

    // Create a new array with only the first best_values_number items
    let best_values = items.slice(0, best_values_number);
    let dict_best_values = {};
    for(let i=0; i<best_values.length; i++){
        dict_best_values[best_values[i][0]] = best_values[i][1]
    }
    return dict_best_values
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
        }while(color === "#000000");
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
  ctx.clearRect(0, 0, canvas.width, canvas.height);
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

function hist(dict_values, html_canvas_id, x_label, y_label, title, best_values_number = 3, best_value = true){
  if(best_value){
      dict_values = sortProperties(dict_values, best_values_number)
  }

  let data = canvas_data(dict_values);
  let datalist= data[0];
  let labels = data[1];
  let colist = data[2];
  let canvas = document.getElementById(html_canvas_id);
  let total = 0;
  for(let x=0; x < datalist.length; x++) { total += datalist[x]; }
  let x_marge_value = canvas.width * 0.15;
  let y_marge_value = canvas.height * 0.15;
  let ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.moveTo(x_marge_value,canvas.height - y_marge_value);
  ctx.lineTo(x_marge_value,y_marge_value);
  ctx.moveTo(x_marge_value,canvas.height - y_marge_value);
  ctx.lineTo(canvas.width - x_marge_value,canvas.height - y_marge_value);
  ctx.stroke();
  let graph_y = (canvas.height - 2*y_marge_value)/11;
  let y_pos = canvas.height - y_marge_value - graph_y;

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
  ctx.font = "30px bold Arial";
  ctx.textAlign = "center"
  ctx.fillText(title, x_marge_value + (canvas.width - 2*x_marge_value)/2, y_pos)
  ctx.textAlign = "right"
  ctx.font = "15px Arial";
  ctx.fillText(y_label, x_marge_value - 10, y_pos)

  let rec_x = x_marge_value + 5
  let rec_y = canvas.height - y_marge_value
  let rect_width = (canvas.width - 2*x_marge_value)/datalist.length - 5
  let rect_height = graph_y*10 + 5
  for(let i=0; i <datalist.length; i++){
     let data_percentage = (datalist[i] * 100) / total
     let rect_data_height = data_percentage * rect_height / 100
     ctx.beginPath();
     ctx.fillStyle = colist[i]
     ctx.rect(rec_x, rec_y, rect_width, -rect_data_height)
     ctx.fill();
     ctx.closePath()
     ctx.font = "15px Arial";
     ctx.textAlign = "center"
     ctx.fillText(labels[i], rec_x + (rect_width/2), rec_y + 20)
     rec_x = rec_x + 5 + rect_width
  }
  ctx.strokeStyle = "rgb(0,0,0)";
  ctx.fillStyle = "rgb(0,0,0)";
  ctx.font = "15px Arial";
  ctx.fillText(x_label, x_marge_value + (canvas.width - 2*x_marge_value)/2, canvas.height - y_marge_value + 40)
}

function map(list_values, html_canvas_id){
    let canvas = document.getElementById(html_canvas_id);
    let ctx  = canvas.getContext("2d");
    console.log(canvas.clientWidth, canvas.clientHeight)
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let img = document.getElementById("source");
    canvas.addEventListener('mousedown', onDown, false);
    ctx.drawImage(img, 0, 0, canvas.clientWidth, canvas.clientHeight);
    for (let i=0; i<list_values.length; i++){
        let longitude = list_values[i][0];
        let latitude = list_values[i][1];
        let latRad = latitude*Math.PI/180;

        let x = (canvas.clientWidth * (longitude + 180 - 10)/360);
        let mercy = Math.log(Math.tan((Math.PI/4) + (latRad/2)));
        let y =  canvas.clientHeight /2 - canvas.clientWidth*mercy/(2*Math.PI);


        ctx.beginPath();
        ctx.fillStyle="#FF4422";
        ctx.arc(x, y, 1, 0, 2 * Math.PI);
        ctx.fill()
    }
}

function onDown(event){
    let cx = event.pageX
    let cy = event.pageY
}