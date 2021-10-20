// Filen: static/admin.js


// Function to run on loading the webpage
function main() {

  // Defining constants for all buttons for selecting 
  // type of notification and their respective sections
  const butn1 = document.querySelector("#score");
  const butn2 = document.querySelector("#status");
  const butn3 = document.querySelector("#time");
  const butn4 = document.querySelector("#event");
  const butn5 = document.querySelector("#role");
  const form1 = document.querySelector(".block1");
  const form2 = document.querySelector(".block2");
  const form3 = document.querySelector(".block3");
  const form4 = document.querySelector(".block4");
  const form5 = document.querySelector(".block5");


  // Adding event listener on button 1
  butn1.addEventListener("click", () => {

    // Changing all other button colours to White
    // and button 1 colour to blue
    butn1.style.backgroundColor = "#3B82F6"
    butn1.style.color = 'white'
    butn2.style.backgroundColor = "white"
    butn2.style.color = '#1E3A8A'
    butn3.style.backgroundColor = "white"
    butn3.style.color = '#1E3A8A'
    butn4.style.backgroundColor = "white"
    butn4.style.color = '#1E3A8A'
    butn5.style.backgroundColor = "white"
    butn5.style.color = '#1E3A8A'

    // Hiding other notifications' sections and
    // Showing the one associated with the button
    form1.style.display = "block";
    form2.style.display = "none";
    form3.style.display = "none";
    form4.style.display = "none";
    form5.style.display = "none";

  });

  // Adding event listener on button 2
  butn2.addEventListener("click", () => {

    // Changing all other button colours to White
    // and button 2 colour to blue
    butn2.style.backgroundColor = "#3B82F6"
    butn2.style.color = 'white'
    butn1.style.backgroundColor = "white"
    butn1.style.color = '#1E3A8A'
    butn3.style.backgroundColor = "white"
    butn3.style.color = '#1E3A8A'
    butn4.style.backgroundColor = "white"
    butn4.style.color = '#1E3A8A'
    butn5.style.backgroundColor = "white"
    butn5.style.color = '#1E3A8A'

    // Hiding other notifications' sections and
    // Showing the one associated with the button
    form1.style.display = "none";
    form2.style.display = "block";
    form3.style.display = "none";
    form4.style.display = "none";
    form5.style.display = "none";

  });

  // Adding event listener on button 3
  butn3.addEventListener("click", () => {

    // Changing all other button colours to White
    // and button 3 colour to blue
    butn1.style.backgroundColor = "white"
    butn1.style.color = '#1E3A8A'
    butn2.style.backgroundColor = "white"
    butn2.style.color = '#1E3A8A'
    butn3.style.backgroundColor = "#3B82F6"
    butn3.style.color = 'white'
    butn4.style.backgroundColor = "white"
    butn4.style.color = '#1E3A8A'
    butn5.style.backgroundColor = "white"
    butn5.style.color = '#1E3A8A'

    // Hiding other notifications' sections and
    // Showing the one associated with the button
    form1.style.display = "none";
    form2.style.display = "none";
    form3.style.display = "block";
    form4.style.display = "none";
    form5.style.display = "none";

  });

  // Adding event listener on button 4
  butn4.addEventListener("click", () => {

    // Changing all other button colours to White
    // and button 4 colour to blue
    butn1.style.backgroundColor = "white"
    butn1.style.color = '#1E3A8A'
    butn3.style.backgroundColor = "white"
    butn3.style.color = '#1E3A8A'
    butn2.style.backgroundColor = "white"
    butn2.style.color = '#1E3A8A'
    butn4.style.backgroundColor = "#3B82F6"
    butn4.style.color = 'white'
    butn5.style.backgroundColor = "white"
    butn5.style.color = '#1E3A8A'

    // Hiding other notifications' sections and
    // Showing the one associated with the button
    form1.style.display = "none";
    form2.style.display = "none";
    form3.style.display = "none";
    form4.style.display = "block";
    form5.style.display = "none";
  });

  // Adding event listener on button 5
  butn5.addEventListener("click", () => {

    // Changing all other button colours to White
    // and button 5 colour to blue
    butn1.style.backgroundColor = "white"
    butn1.style.color = '#1E3A8A'
    butn2.style.backgroundColor = "white"
    butn2.style.color = '#1E3A8A'
    butn3.style.backgroundColor = "white"
    butn3.style.color = '#1E3A8A'
    butn4.style.backgroundColor = "white"
    butn4.style.color = '#1E3A8A'
    butn5.style.backgroundColor = "#3B82F6"
    butn5.style.color = 'white'

    // Hiding other notifications' sections and
    // Showing the one associated with the button
    form1.style.display = "none";
    form2.style.display = "none";
    form3.style.display = "none";
    form4.style.display = "none";
    form5.style.display = "block";

  });
}