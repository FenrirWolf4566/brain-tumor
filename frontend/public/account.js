function estConnecte(){
    let token =  localStorage.getItem(SESSION_TOKEN);
    return token !== null && token.length > 0;
}
async function whoami(){
    const url = ROOT_URL+'account/me/';
    const token = localStorage.getItem(SESSION_TOKEN);
   return  fetch(url, {method: 'GET',headers: {'Accept': 'application/json','Authorization': `Bearer `+token}}).then(response => response.json())
}

function triggerConnectedEvent(){
    const event = new Event("connected");
    document.dispatchEvent(event);
}

function triggerDisconnectedEvent(){
    const event = new Event("disconnected");
    document.dispatchEvent(event);
}

function seDeconnecter(){
    localStorage.removeItem(SESSION_TOKEN);
    triggerDisconnectedEvent();
}

function guard(){
    if(!estConnecte()){
        location.href='/';
    }
}