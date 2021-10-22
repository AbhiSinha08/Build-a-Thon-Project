// File: static/employee.js


// Function to show new notifications on page on recieving them from server
function show(data) {
  let noti = " ";

  // If the notification is of type 'Reward'
  if (data.type == "rwd") {
    noti =
        `<div class="bg-white rounded-3xl p-5 border-4 border-green-600 shadow-2xl font-sans flex flex-col-2">` +
            
          // SVG Icon to show
          `<svg class="h-10 w-10 fill-current text-green-600" xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                    d="M5 5a3 3 0 015-2.236A3 3 0 0114.83 6H16a2 2 0 110 4h-5V9a1 1 0 10-2 0v1H4a2 2 0 110-4h1.17C5.06 5.687 5 5.35 5 5zm4 1V5a1 1 0 10-1 1h1zm3 0a1 1 0 10-1-1v1h1z"
                    clip-rule="evenodd" />
                <path d="M9 11H3v5a2 2 0 002 2h4v-7zM11 18h4a2 2 0 002-2v-5h-6v7z" />
            </svg>
            <span class="pl-3 w-full">
                <h4 class=" text-green-600 font-bold">`

        // Notification Content
        + data.content +

                `</h4>
            </span>
        </div>
      <br>`;

  }

  // If the notification is of type 'Reminder'
  else if (data.type == "rmd") {
    noti =
        `<div class="bg-white rounded-3xl p-5 border-4 border-yellow-400 shadow-2xl font-sans flex flex-col-2">` +
            
          // SVG Icon to show
          `<svg class="h-10 w-10 fill-current text-yellow-400" xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd" />
            </svg>
            <span class="pl-3 w-full">
                <h4 class="text-yellow-400 font-bold">`

        // Notification Content
        + data.content +

                `</h4>
            </span>
        </div>
      <br>`;

  }

  // If the notification is of type 'Alert'
  else if (data.type == "alr") {
    noti =
        `<div class="bg-white rounded-3xl p-5 border-4 border-red-500 shadow-2xl font-sans flex flex-col-2">` +
            
          // SVG Icon to show
          `<svg class="h-10 w-10 fill-current text-red-500" xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd" />
          </svg>
          <span class="pl-3 w-full">
              <h4 class="text-red-500 font-bold">`

        // Notification Content
        + data.content +

              `</h4>
          </span>
        </div>
      <br>`;

  }

  // Adding notification content in HTML form
  // in the 'notifications' section for user to recieve
  document.getElementById("notifications").innerHTML += noti;
}


// Async function to Listen for Server sent event
async function getapi(url) {

  // Getting response from the server
  const response = await fetch(url);
  var data = await response.json();
  // console.log(data);

  // Checking if a new notification is recieved
  if (data.type != "NULL") {
    show(data);  // Updating notification on page

    // Sending Web Push notification to employee's device

    // Icon for notification
    if (data.type == "rwd") {
      var img = '../static/reward.png';
    }

    else if (data.type == "rmd") {
      var img = '../static/reminder.png';
    }
    
    else if (data.type == "alr") {
      var img = '../static/alert.png';
    }
    
    var head = 'Notification' // Notification Heading
    var text = data.content; // Notification Content

    // Generating new Web Push Notification
    var notification = new Notification(head, { body: text, icon: img });
  }
}


// Source: developer.mozilla.org

// Function to ask for permission for
// sending web push notifications to user's device
function askNotificationPermission() {
  // function to ask the permissions
  function handlePermission(permission) {
    ;
  }

  // checking if browser supports notifications
  if (!('Notification' in window)) {
    console.log("This browser does not support notifications.");
  } else {
    if (checkNotificationPromise()) {
      Notification.requestPermission()
        .then((permission) => {
          handlePermission(permission);
        })
    } else {
      // requesting permission
      Notification.requestPermission(function (permission) {
        handlePermission(permission);
      });
    }
  }
}

function checkNotificationPromise() {
  try {
    Notification.requestPermission().then();
  } catch (e) {
    return false;
  }

  return true;
}


// Function to run on loading the webpage
function loadNotis() {

  // Asking for notifications permission
  askNotificationPermission()

  // Listening for SSEs
  setInterval(() => {
    getapi(url)
  }, 2500)
}

