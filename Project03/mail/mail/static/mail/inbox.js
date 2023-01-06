document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#emails-details-view').style.display = 'block';
      
      document.querySelector('#emails-details-view').innerHTML = `
      <ul class="list-group">
        <li class="list-group-item"><strong>Form: </strong>${email.sender}</li>
        <li class="list-group-item"><strong>To: </strong>${email.recipients}</li>
        <li class="list-group-item"><strong>Subject: </strong>${email.subject}</li>
        <li class="list-group-item"><strong>Timestamp: </strong>${email.timestamp}</li>
        <li class="list-group-item">${email.body}</li>
      </ul> 
      `;      
      
      //mail read
      if (!email.read){
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }


      //archivre / unarchive
      const btn_archive = document.createElement('button');
      if (email.archived === true){
        btn_archive.innerHTML = "unarchive";
        btn_archive.className = "btn btn-danger";
      }else{
        btn_archive.innerHTML = "archive";
        btn_archive.className = "btn btn-success";
      }

      btn_archive.addEventListener('click', function() {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(()=> {load_mailbox('archive')})
      });
      document.querySelector('#emails-details-view').append(btn_archive);

      //btn reply 
      const btn_reply = document.createElement('button');
      btn_reply.innerHTML = "reply"; 
      btn_reply.className = "btn btn-info";
      btn_reply.addEventListener('click', function(){
        compose_email()
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = `re: ${email.subject}`;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      })
      document.querySelector('#emails-details-view').append(btn_reply);
  });
}
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-details-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // show sent mailbox  
fetch(`/emails/${mailbox}`)
.then(response => response.json())
.then(emails => {
    //create a loop to display each mails
    emails.forEach(mail => {
      const new_email = document.createElement('div');
      new_email.className ="list-group-item";
      
      new_email.innerHTML = `
        <h6>sender: ${mail.sender} </h6>
        <h5>subject: ${mail.subject} </h5>
        <p> ${mail.timestamp}</p>
        `;
      //modify background color
      if (mail.read === true){
        new_email.style.backgroundColor = 'white';
      }else{
        new_email.style.backgroundColor = 'grey';
      }

      new_email.addEventListener('click', function () {
        view_email(mail.id)
      });
      document.querySelector('#emails-view').append(new_email);      
    });
});
}

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });

}

