async function fetchRequestWithError() {
    try {
      const url = `http://15.164.102.226:8080/pastebin/api/pastes/`;
      const response = await fetch(url);
      if (response.status >= 200 && response.status < 400) {
        const data = await response.json();
        for (var key in data) {
          ndiv = document.createElement('div');
          ndiv.innerHTML = `<h3> ${data[key]['title']} </h3><p> ${data[key]['content']}</p><hr>`;
          pdiv = document.getElementById('pastes');
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
  