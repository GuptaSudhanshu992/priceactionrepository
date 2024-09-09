function handleCredentialResponse(response){alert("response caught");const jwt_token=response.credential;console.log("ID Token: "+jwt_token);const button=document.getElementById('gloginbtn');const referrer=isReferrerFromCurrentDomain(document.referrer)?document.referrer:window.location.origin;const response_message=document.getElementById('response_messages')
const id_token=jwt_token;const auth_method="Google";response_message.innerHTML="";response_message.style.display="none";response_message.classList.remove('alert-success');response_message.classList.remove('alert-danger');button.disabled=true;button.className='btn btn-success btn-block';button.innerHTML='<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';try{const response=await fetch("/members/socialaccountlogin/",{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded',},body:new URLSearchParams({id_token:id_token,auth_method:auth_method,referrer:referrer})});const data=await response.json();if(data.success){response_message.innerHTML=data.message;response_message.style.display="block";response_message.classList.add('alert-success');setTimeout(()=>{window.location.href=data.redirect_url;},3000);}else{console.log('Login attempt failed!');button.disabled=false;button.innerHTML='Login';response_message.innerHTML=data.message;response_message.style.display="block";response_message.classList.add('alert-danger');}}catch(error){console.error('Request error:',error);button.disabled=false;button.innerHTML='Login';response_message.innerHTML='Unexpected error has occurred, please refresh the page and try again...';response_message.style.display="block";response_message.classList.add('alert-danger');}}
function togglePasswordVisibility(passwordID,togglebuttonID){const passwordField=document.getElementById(passwordID);const toggleIcon=document.getElementById(togglebuttonID);if(passwordField.type==='password'){passwordField.type='text';toggleIcon.classList.remove('fa-eye');toggleIcon.classList.add('fa-eye-slash');}else{passwordField.type='password';toggleIcon.classList.remove('fa-eye-slash');toggleIcon.classList.add('fa-eye');}}
function toggleAlert(elementID,alertMsgId){const alertElement=document.getElementById(alertMsgId);if(elementID=='password1'){alertElement.style.display='block';alertElement.classList.add('show');}else{alertElement.classList.remove('show');alertElement.style.display='none';}}
async function handleLogout(){const button=document.getElementById('logout_btn');const csrfToken=document.querySelector('input[name="csrfmiddlewaretoken"]').value;const referrer=window.location.href;const response_message=document.getElementById('response_messages');response_message.innerHTML="";response_message.style.display="none";response_message.classList.remove('alert-success','alert-danger');button.disabled=true;button.innerHTML='<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';try{const response=await fetch("/members/logout/",{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded','X-CSRFToken':csrfToken},body:new URLSearchParams({'referrer':referrer,})});const data=await response.json();if(data.success){response_message.innerHTML=data.message;response_message.style.display="block";response_message.classList.add('alert-success');setTimeout(()=>{window.location.href=data.redirect_url;console.log("Redirection url : ",data.redirect_url);},1000);}else{console.log('Logout attempt failed!');button.disabled=false;button.innerHTML='SIGN OUT';response_message.innerHTML=data.message;response_message.style.display="block";response_message.classList.add('alert-danger');}}catch(error){console.error('Request error:',error);button.disabled=false;button.innerHTML='SIGN OUT';response_message.innerHTML='Unexpected error has occurred, please refresh the page and try again...';response_message.style.display="block";response_message.classList.add('alert-danger');}}
function isReferrerFromCurrentDomain(referrer){try{const currentDomain=window.location.hostname;const referrerDomain=new URL(referrer).hostname;return currentDomain===referrerDomain;}catch(error){return false;}};