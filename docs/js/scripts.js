

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


function generate_row_header_action(array) {
    var row = document.createElement("tr");
    for (var i = 0; i < 7; i++){
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


function generate_row_action(array) {
    var row = document.createElement("tr");
    for (var i = 0; i < 7; i++) {
        var cell;
        if (i == 0) {
            cell = document.createElement("th");
            cell.setAttribute("scope", "row");
        } else{
            cell = document.createElement("th");
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

/*
uint32 actionType = 1;
uint32 itemSerial = 2;
uint32 mobileSerial = 3;
uint32 walkDirection = 4;
uint32 index = 5;
uint32 amount = 6;
bool run = 7;
*/

function generate_action_table(container, inputs, outputs, parameters = []) {
    var container = document.getElementById(container);

    var tbl = document.createElement("table");
    tbl.className = "table table-sm";

    var tblThead = document.createElement("thead");
    tblThead.className = "thead-light";

    var header_row = generate_row_header_action(["actionType", "sourceSerial", "targetSerial", "walkDirection", "index", "amount", "run"]);
    tblThead.appendChild(header_row);
    tbl.appendChild(tblThead);

    var tblInBody = document.createElement("tbody");
    for(var i = 0; i < inputs.length; i++) {
        var row = generate_row_action([inputs[i][0], inputs[i][1], inputs[i][2], inputs[i][3], inputs[i][4], inputs[i][5], inputs[i][6]]);
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

    text_obj.appendChild(header_obj);
    obj_container.appendChild(text_obj);
    obj.appendChild(obj_container);
}


function createHeaderAction(container, type, description) {
    var obj = document.getElementById(container);
    obj.style.display = 'flex';
    obj.style.justifyContent = 'left';
    obj.style.alignItems = 'left';
    //vertical-align: top; /* here */

    var obj_container = document.createElement("div");
    obj_container.className = "container";

    var header_obj = document.createElement("div");
    header_obj.className = "p-1 mb-1";

    var text_obj = document.createElement("P");
    text_obj.className = "h4";
    
    var type_obj = document.createElement("div");
    var type_text = document.createTextNode(type + ' ');
    type_obj.className = "p-1 mb-1 bg-dark";
    type_obj.style.color = 'white';
    type_obj.appendChild(type_text);

    var module_obj = document.createElement('H');
    var module_text = document.createTextNode(description + '');
    module_obj.style.color = 'black';
    module_obj.style.backgroundColor = 'None';
    module_obj.style.fontSize = '20px';
    module_obj.appendChild(module_text);

    header_obj.appendChild(type_obj);
    header_obj.appendChild(module_obj);

    text_obj.appendChild(header_obj);
    obj_container.appendChild(text_obj);
    obj.appendChild(obj_container);
}