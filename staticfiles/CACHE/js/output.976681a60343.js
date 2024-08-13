function togglePasswordVisibility(passwordID,togglebuttonID){const passwordField=document.getElementById(passwordID);const toggleIcon=document.getElementById(togglebuttonID);if(passwordField.type==='password'){passwordField.type='text';toggleIcon.classList.remove('fa-eye');toggleIcon.classList.add('fa-eye-slash');}else{passwordField.type='password';toggleIcon.classList.remove('fa-eye-slash');toggleIcon.classList.add('fa-eye');}}
function toggleAlert(elementID,alertMsgId){const alertElement=document.getElementById(alertMsgId);if(elementID=='password1'){alertElement.style.display='block';alertElement.classList.add('show');}else{alertElement.classList.remove('show');alertElement.style.display='none';}};async function handleLogout(){const button=document.getElementById('logout_btn');const csrfToken=document.querySelector('input[name="csrfmiddlewaretoken"]').value;const referrer=window.location.href;const response_message=document.getElementById('response_messages');response_message.innerHTML="";response_message.style.display="none";response_message.classList.remove('alert-success','alert-danger');button.disabled=true;button.innerHTML='<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';try{const response=await fetch("/members/logout/",{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded','X-CSRFToken':csrfToken},body:new URLSearchParams({'referrer':referrer,})});const data=await response.json();if(data.success){response_message.innerHTML=data.message;response_message.style.display="block";response_message.classList.add('alert-success');setTimeout(()=>{window.location.href=data.redirect_url;console.log("Redirection url : ",data.redirect_url);},1000);}else{console.log('Logout attempt failed!');button.disabled=false;button.innerHTML='SIGN OUT';response_message.innerHTML=data.message;response_message.style.display="block";response_message.classList.add('alert-danger');}}catch(error){console.error('Request error:',error);button.disabled=false;button.innerHTML='SIGN OUT';response_message.innerHTML='Unexpected error has occurred, please refresh the page and try again...';response_message.style.display="block";response_message.classList.add('alert-danger');}}
function isReferrerFromCurrentDomain(referrer){try{const currentDomain=window.location.hostname;const referrerDomain=new URL(referrer).hostname;return currentDomain===referrerDomain;}catch(error){return false;}};async function handleforgotpassword(){const button=document.getElementById('send_reset_link');const csrfToken=document.querySelector('input[name="csrfmiddlewaretoken"]').value;const response_message=document.getElementById('response_messages');const email=document.getElementById('email').value;const referrer="/members/login/";response_message.innerHTML="";response_message.style.display="none";response_message.classList.remove('alert-success','alert-danger');button.disabled=true;button.innerHTML='Sending link...<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';try{const response=await fetch("/members/forgotpassword/",{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded','X-CSRFToken':csrfToken},body:new URLSearchParams({'email':email,'referrer':referrer,})});const data=await response.json();if(data.success){window.location.href=data.redirect_url;}else{console.log('Reset Password attempt failed!');button.disabled=false;button.innerHTML='Send Reset Link';response_message.innerHTML=data.message;response_message.style.display="block";response_message.classList.add('alert-danger');}}catch(error){console.error('Request error:',error);button.disabled=false;button.innerHTML='Send Reset Link';response_message.innerHTML='Unexpected error has occurred, please refresh the page and try again...';response_message.style.display="block";response_message.classList.add('alert-danger');}};