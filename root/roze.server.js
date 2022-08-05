function returnXPath(element) {
    if (element.tagName == 'HTML')
        return '/HTML';
    if (element===document.body)
        return '/HTML/BODY';

    var num = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i<siblings.length; i++) {
        var sibling = siblings[i];
        if (sibling === element)
            if (num === 0) {
                return returnXPath(element.parentNode) + '/' + element.tagName;
            }
            else {
                return returnXPath(element.parentNode) + '/' + element.tagName + '[' + (num + 1) + ']';
            }
        if (sibling.nodeType===1 && sibling.tagName===element.tagName)
            num++;
    }
}

function OnEvent(event) {
    message['softpath'] = document.location.pathname.toString();
    message["path"] = returnXPath(this);
    message["event"] = event.type;
    message["type"] = 'update';
    if (event.type == "input") {
        message['vars'][message['path']] = this.value;
    }
    console.log(message);
    socket.send(JSON.stringify(message));
}

function Init() {
    socket.onopen = function (event) {
        message = {
            "type": "info",
            "softpath": document.location.pathname.toString(),
            "vars": {},
            "event": "",
            "path": "",
            "paths": {},
            "insert": {},
        };
        console.log(message);
        socket.send(JSON.stringify(message));
    };
}

var message; var elements; var socket;
socket = new WebSocket(("ws://" + window.location.hostname + "/_roze"));
socket.onmessage = function (event) {
    message = JSON.parse(event.data);
    console.log(event.data);
    const keys = Object.keys(message['insert']);
    for (x = 0; x < keys.length; x++) {
        document.evaluate(keys[x], document).iterateNext().innerHTML = message['insert'][keys[x]];
    }
    const keysPaths = Object.keys(message['paths']);
    for (x = 0; x < keysPaths.length; x++) {
        for (var y = 0; y < message['paths'][keysPaths[x]].length; y++) {
            document.evaluate(keysPaths[x], document).iterateNext().addEventListener(message['paths'][keysPaths[x]][y], OnEvent, false);
        }
    }
    message['insert'] = {};
    message['paths'] = {};
};
window.addEventListener('load', Init);

// identify an element to observe
const elementToObserve = document.querySelector("app");

// create a new instance of `MutationObserver` named `observer`,
// passing it a callback function
const observer = new MutationObserver(function () {
    var elems = document.querySelectorAll("[href]");
    for (var i = 0; i < elems.length; i++) {
        var currElem = elems[i];
        if (currElem.hostname != document.location.hostname)
            continue;
        currElem.onclick = function (e) {
            e = e || window.event;
            var element = e.target || e.srcElement;
            //document.location.pathname = element.pathname;
            window.history.pushState('test', 'Title', element.pathname);
            message['softpath'] = element.pathname;
            message["path"] = "";
            message["event"] = "";
            message["type"] = 'info';
            console.log(message);
            socket.send(JSON.stringify(message));
            return false;
        }
    }
});

// call `observe()` on that MutationObserver instance,
// passing it the element to observe, and the options object
observer.observe(elementToObserve, { subtree: true, childList: true });
