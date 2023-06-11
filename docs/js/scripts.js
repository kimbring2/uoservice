

function generate_row_header(array) {
    var row = document.createElement("tr");
    for (var i = 0; i < 3; i++){
        var cell = document.createElement("th");
        cell.setAttribute("scope", "col");
        var cell_text = document.createTextNode(array[i]);
        cell.appendChild(cell_text);
        row.append(cell);
    }

    return row;
}


function generate_row(array) {
    var row = document.createElement("tr");
    for (var i = 0; i < 3; i++) {
        var cell;
        if (i == 0) {
            cell = document.createElement("th");
            cell.setAttribute("scope", "row");
        } else{
            cell = document.createElement("td");
        }
        
        var cell_text = document.createTextNode(array[i]);
        cell.appendChild(cell_text);
        row.append(cell);
    }

    return row;
}


function generate_table(container, inputs, outputs, parameters = []) {
    var container = document.getElementById(container);
    
    var tbl = document.createElement("table");
    tbl.className = "table table-sm";

    var tblThead = document.createElement("thead");
    tblThead.className = "thead-light";
    var header_row = generate_row_header(["Name", "Type", "Description"]);
    tblThead.appendChild(header_row);
    tbl.appendChild(tblThead);

    var tblInBody = document.createElement("tbody");
    for(var i = 0; i < inputs.length; i++) {
        var row = generate_row([inputs[i][0], inputs[i][1], inputs[i][2]]);
        tblInBody.appendChild(row);
    }

    tbl.appendChild(tblInBody);
    
    container.appendChild(tbl);
}


function createHeader(container, type, module, name, params="") {
    var obj = document.getElementById(container);
    var obj_container = document.createElement("div");
    obj_container.className = "container";

    var header_obj = document.createElement("div");
    header_obj.className = "p-1 mb-4 bg-dark text-white";
    var text_obj = document.createElement("P");
    text_obj.className = "h4";
    
    var type_obj = document.createElement("EM");
    //type_obj.className = "text-muted";
    var type_text = document.createTextNode(type + ' ');
    type_obj.appendChild(type_text);
    
    var module_obj = document.createElement('EM');
    var module_text = document.createTextNode(module + '');
    module_obj.appendChild(module_text);
    
    var class_obj = document.createElement('B');
    var class_text = document.createTextNode(name);
    class_obj.appendChild(class_text);

    header_obj.appendChild(type_obj);
    header_obj.appendChild(module_obj);
    //header_obj.appendChild(class_obj);

    //if(params.length>0){
    //    var params_text = document.createTextNode(params);
    //    header_obj.appendChild(params_text);    
    //}
    
    text_obj.appendChild(header_obj);
    obj_container.appendChild(text_obj);
    obj.appendChild(obj_container);
}