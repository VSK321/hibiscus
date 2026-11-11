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
        message['vars'] = {};
        message['vars'][message['path']] = this.value;
    }
    socket.send(JSON.stringify(message));
}

function Init() {
    socket.onopen = function (event) {
        message = {
            "type": "info",
            "priorSoftPath": document.location.pathname.toString(),
            "softpath": document.location.pathname.toString(),
            "vars": {},
            "event": "",
            "path": "",
            "paths": {},
            "insert": {},
        };
        socket.send(JSON.stringify(message));
    };
}

var message; var elements; var socket;
socket = new WebSocket(("ws://" + window.location.hostname + ":" + window.location.port + "/_hibiscus"));
socket.onmessage = function (event) {
    message = JSON.parse(event.data);
    const keys = Object.keys(message['insert']);
    for (x = 0; x < keys.length; x++) {
        try {
            if (message['insert'][keys[x]][1] === 0) {
                document.evaluate(keys[x], document).iterateNext().remove();
            }
            else if (message['insert'][keys[x]][1] === 2) {
                document.evaluate(keys[x], document).iterateNext().innerHTML = message['insert'][keys[x]][0];
            }
            else {
                for (y = 0; y < message['insert'][keys[x]][0].length; y++) {
                    var wrapper = document.createElement('div');
                    wrapper.innerHTML = message['insert'][keys[x]][0][y][0];
                    var elem = wrapper.firstChild;
                    if (elem.innerHTML != message['insert'][keys[x]][0][y][0]) {
                        var wrapper = document.createElement('tbody');
                        wrapper.innerHTML = message['insert'][keys[x]][0][y][0];
                        var elem = wrapper.firstChild;
                    }
                    //Previous Element XPath
                    if (!message['insert'][keys[x]][0][y][1]) {
                        document.evaluate(keys[x], document).iterateNext().appendChild(elem);
                    }
                    //Next Element XPath
                    else {
                        var next_elem = document.evaluate(message['insert'][keys[x]][0][y][1], document).iterateNext();
                        document.evaluate(keys[x], document).iterateNext().insertBefore(elem, next_elem);
                    }
                }
            }
        }
        catch (e) {
            console.log(e);
        }
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

const app = document.querySelector("app");

const observer = new MutationObserver(function () {
    var elems = document.querySelectorAll("[href]");
    for (var i = 0; i < elems.length; i++) {
        var currElem = elems[i];
        if (currElem.hostname != document.location.hostname)
            continue;
        currElem.onclick = function (e) {
            e = e || window.event;
            var element = e.target || e.srcElement;
            if (element.pathname.substring(0, 2) == "/_") {
                window.location.replace("/" + element.pathname.substring(2, element.pathname.length));
            }
            //document.location.pathname = element.pathname;
            window.history.pushState('', '', element.pathname);
            message['softpath'] = element.pathname;
            message["path"] = "";
            message["event"] = "";
            message["type"] = 'info';
            console.log(message);
            socket.send(JSON.stringify(message));
            message.priorSoftPath = element.pathname;
            return false;
        }
    }
});

observer.observe(app, { subtree: true, childList: true });
