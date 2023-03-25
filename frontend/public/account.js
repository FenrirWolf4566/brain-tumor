function estConnecte(){
    let token =  localStorage.getItem(SESSION_TOKEN);
    let item_end = localStorage.getItem(SESSION_END);
    if(token==null || item_end==null)return false;
    let end_session = +item_end;
    let remainingtime = end_session - Date.now();
    //console.log("Temps restant avant fin de session :"+(new Date(remainingtime).toUTCString()))
    return token.length > 0 && remainingtime>0;
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
    localStorage.clear()
    triggerDisconnectedEvent();
}

function guard(){
    if(!estConnecte()){
        location.href='/';
    }
}