function getUserNameFromPath() {
    return window.location.pathname.split('/')[3];
}

function validateUserName(username) {
    if (!username) {
        console.log("username not found in path");
        return;
    }
}

async function fetchRequestWithError() {
    try {
      const username = getUserNameFromPath();
      validateUserName(username);
      const url = `https://pastebin.mydomain.aws:8443/pastebin/api/users/` + username + `/pastes?skip=0&limit=10`;
      const response = await fetch(url);
      if (response.status >= 200 && response.status < 400) {
        const data = await response.json();
        pdiv = document.getElementById('pastes');
        while (pdiv.firstChild) {
          pdiv.removeChild(pdiv.firstChild);
        }
        for (var key in data) {
          ndiv = document.createElement('div');
          ndiv.innerHTML = `<h3> ${data[key]['title']} </h3><p> ${data[key]['content']}</p><hr>`;
          pdiv.appendChild(ndiv);
        }
      } else {
        console.log(`${response.statusText}: ${response.status} error`);
      }
    } catch (error) {
      console.log(error);
    }
  }
  
  fetchint = setInterval(fetchRequestWithError, 10*1000);
  