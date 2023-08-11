document.querySelectorAll('.form-outline').forEach((formOutline) => {
  new mdb.Input(formOutline).init();
});
document.querySelectorAll('.form-outline').forEach((formOutline) => {
  new mdb.Input(formOutline).update();
});
/*
var question = document.getElementById("question");
question.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
  }
});
 */
window.counter = 0;
window.button_spawned = false;
function spawnAnswer(num = 0) {
  const place = document.getElementById('place');
  if (num !== window.counter) {
    return;
  }
  if (window.counter === 0) {
    let elem = document.createElement('div');
    elem.className = "popup d-flex justify-content-center row";
    elem.style.height = "2rem";
    elem.innerHTML = "<p class=\"text-center fs-4 fw-light pt-2\">Put your answers here and mark right:</p>";
    place.appendChild(elem);
    let qbutton = document.getElementById('expandAnswer');
    qbutton.style.display = 'none';
  }
  if (window.counter > 0 && !window.button_spawned) {
    let elem = document.createElement('div');
    let frm = document.getElementById('form');
    elem.className = "popup d-flex justify-content-center row pt-3";
    elem.style.height = "3rem";
    elem.innerHTML = "                    <button type=\"submit\" class=\"popup btn btn-light btn-rounded pt-2\" style=\"height: 100%; width: auto;\" data-mdb-ripple-color=\"dark\">\n" +
        "                        <i class=\"fas fa-arrow-right-long\">\n" +
        "                        Next question\n" +
        "                        </i>\n" +
        "                    </button>";
    frm.appendChild(elem);
    window.button_spawned = true;
  }
    if (window.counter > 4) {
      let el = document.getElementById('expand' + window.counter);
      el.style.display = 'none';
      return;
    }
      let ans = document.createElement('div');
      ans.classList.add('answer');
      ans.classList.add('pt-4');
      window.counter = window.counter + 1;
      let code = "              <div class=\"d-flex justify-content-center row\">\n" +
          "                  <div class=\"form-white form-outline w-100\">\n" +
          "                      <div class=\"input-group\">\n" +
          "                      <div class=\"input-group-text\">\n" +
          "                        <input class=\"form-check-input mt-0\" name=\"check"+ window.counter + "\" value=\"true\" type=\"checkbox\" />\n" +
          "                    </div>\n" +
          "                    <input name=\"answer" + window.counter + "\" type=\"text\" placeholder=\"Answer\" aria-describedby=\"check1\" class=\"border form-control form-icon-trailing\" required />\n" +
          "                          <button type=\"button\" id=\"expand" + window.counter + "\" onclick=\"spawnAnswer(" + window.counter + ")\" class=\"btn btn-light\">\n" +
          "                      <i class=\"fas fa-arrow-down-long\"></i>\n" +
          "                    </button>\n" +
          "                      </div>\n" +
          "                  </div>\n" +
          "              </div>\n" +
          "                    </div>"
      ans.innerHTML = code
      place.appendChild(ans);
      let prev = document.getElementById('expand' + (window.counter - 1));
      prev.style.display = 'none';
}