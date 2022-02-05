myDiv = document.getElementById("editor").addEventListener("input", function() {
    myDiv = document.getElementById("editor");
    let contents = myDiv.innerHTML.split(" ");
    let last = contents[contents.length-1]
    last = strip(last)
    if(last!=="") {
        httpRequest = new XMLHttpRequest();
        httpRequest.open('POST', 'http://127.0.0.1:5000/', true);
        httpRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        httpRequest.onreadystatechange = function(){
            if(httpRequest.readyState === httpRequest.DONE) {
                if(httpRequest.status === 200) {
                    console.log(httpRequest.responseText)
                    let content = document.createTextNode(httpRequest.responseText)
                    let container = document.createElement("span");
                    container.appendChild(content);
                    container.style.color = "grey"
                    myDiv.appendChild(container)

                    myDiv.addEventListener("keydown", function(event) {
                        if (event.keyCode == 9) {
                            event.preventDefault();
                            container.style.color = "black";
                            setCaret(myDiv, container);
                        }
                        else if(container.style.color === "grey") {
                            container.remove();
                        }
                    })
                    let brvar = myDiv.getElementsByTagName('br')
                    for(let i = brvar.length; i--;) {
                        brvar[i].parentNode.removeChild(brvar[i]);
                    }
                    console.log(myDiv.innerHTML.split(" "))
                }
            }
        };
        httpRequest.send(last);
    }
}, false);

function strip(html){
    let doc = new DOMParser().parseFromString(html, 'text/html');
    return doc.body.textContent || "";
 }

function setCaret(node, element) {
    var range = document.createRange();
    range.setStart(node.childNodes[node.childNodes.length-1], 1);
    var sel = window.getSelection();
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);
    element.focus();    
 }