document.getElementById ('fullnamec').style.display = 'none';
document.getElementById ('phonec').style.display = 'none';
document.getElementById ('emailc').style.display = 'none';
document.getElementById ('passwordc').style.display = 'none';
document.getElementById ('cpasswordc').style.display = 'none';

function clearMsg (elid) {
  document.getElementById (elid).style.display = 'none';
}
function fullName () {
  let fn = document.getElementById ('r_fullname').value;
  if (/^[a-zA-Z]+$/.test (fn)) {
    document.getElementById ('fullnamec').style.display = 'none';
    document.getElementById ('r_fullname').style.borderColor = 'green';
    return true;
  } else {
    document.getElementById ('fullnamec').style.display = 'block';
    document.getElementById ('r_fullname').style.borderColor = 'red';
    return false;
  }
}

function phone () {
  let ph = document.getElementById ('r_phone').value;
  if (ph.length != 10) {
    document.getElementById ('phonec').style.display = 'block';
    document.getElementById ('r_phone').style.borderColor = 'red';
    return false;
  } else {
    if (/^[0-9]*$/.test (ph)) {
      document.getElementById ('phonec').style.display = 'none';
      document.getElementById ('r_phone').style.borderColor = 'green';
      return true;
    } else {
      document.getElementById ('phonec').style.display = 'block';
      document.getElementById ('r_phone').style.borderColor = 'red';
      return false;
    }
  }
}

function email () {
  let em = document.getElementById ('r_email').value;
  if (/^([_\-\.0-9a-zA-Z]+)@([_\-\.0-9a-zA-Z]+)\.([a-zA-Z]){2,7}$/.test (em)) {
    document.getElementById ('emailc').style.display = 'none';
    document.getElementById ('r_email').style.borderColor = 'green';
    return true;
  } else {
    document.getElementById ('emailc').style.display = 'block';
    document.getElementById ('r_email').style.borderColor = 'red';
    return false;
  }
}

function password () {
  let p1 = document.getElementById ('r_password').value;
  let p2 = document.getElementById ('r_cpassword').value;

  if (p1 != p2) {
    document.getElementById ('passmsg').innerHTML = 'Password doesnt match';
    document.getElementById ('cpassordc').style.display = 'block';
    document.getElementById ('r_password').style.borderColor = 'red';
    document.getElementById ('r_cpassword').style.borderColor = 'red';
    return false;
  } else {
    return true;
  }
}

function validateRegister () {
  let fn = fullName ();
  let ph = phone ();
  let em = email ();
  let ps = password ();
  if (fn && ph && em && ps) {
    return true;
  } else {
    return false;
  }
}
