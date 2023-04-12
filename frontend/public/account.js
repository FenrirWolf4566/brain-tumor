function estConnecte(){
    let token =  localStorage.getItem(SESSION_TOKEN);
    let item_end = localStorage.getItem(SESSION_END);
    if(token==null || item_end==null)return false;
    let end_session = +item_end;
    const localDate = new Date(Date.now());
    let utc_now = new Date(localDate.getTime() + (localDate.getTimezoneOffset() * 60 * 1000))
    let remainingtime = end_session - utc_now.getTime();
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

async function seDeconnecter(){
    const token = localStorage.getItem(SESSION_TOKEN);
    const url = ROOT_URL+'account/disconnect/';
    await fetch(url, {method: 'GET',headers: {'Accept': 'application/json','Authorization': `Bearer `+token}})
    localStorage.clear();
    triggerDisconnectedEvent();
}

function guard(){
    if(!estConnecte()){
        location.href='/';
    }
}

async function updateConnectedState(){
    let who = await whoami()
    if(who['res_status']=='error')seDeconnecter();
}