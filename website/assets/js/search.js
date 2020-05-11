
/**
 * Perform a search of images and display the resulting thumbnails
 */
function filter_emails() {

    // Find all email elements
    var emails = document.getElementsByClassName("email-card");
//    console.log(emails)
    // var n_proposals = document.getElementsByClassName("proposal").length;

    // Determine the current search values
    var from_search = document.getElementById("from_search_box").value;
    var to_search = document.getElementById("to_search_box").value;
    var cc_search = document.getElementById("cc_search_box").value;
    var body_search = document.getElementById("body_search_box").value;
    var datetime_start_search = moment(document.querySelector('input[id="start_search_box"]').value);
    var datetime_end_search = moment(document.querySelector('input[id="end_search_box"]').value);

    // Determine whether or not to display each thumbnail
    var num_emails_displayed = 0;
    for (i = 1; i <= emails.length; i++) {
        var email  = document.getElementById("email" + i)

        if (!email) {
            console.error("We've got an issue with email", i)
        }

        // Evaluate if the "from" text matches the search
        var email_from = email.getAttribute('from').toLowerCase()
        var from_match = email_from.includes(from_search.toLowerCase())

        // Evaluate if the "to" text matches the search
        var email_to = email.getAttribute('to').toLowerCase()
        var to_match = email_to.includes(to_search.toLowerCase())

        // Evaluate if the "CC" text matches the search
        var email_cc = email.getAttribute('cc').toLowerCase()
        var cc_match = email_cc.includes(cc_search.toLowerCase())

        // Evaluate if the "body" text matches the search
        var email_body = email.getAttribute('body').toLowerCase()
        var body_match = email_body.includes(body_search.toLowerCase())

        // Evaluate if the date matches the search
        var email_str = email.getAttribute('date')
        var email_date = moment(email_str);
        var date_match = (email_date >= datetime_start_search) & (email_date <= datetime_end_search);

        if (from_match & to_match & cc_match && body_match & date_match) {
            document.getElementById("row" + i).style.display = "inline-block";
            num_emails_displayed++;
        } else {
            document.getElementById("row" + i).style.display = "none";
        }
    };

    // If there are no proposals to display, tell the user
    if (num_emails_displayed == 0) {
        document.getElementById('no_proposals_msg').style.display = 'block';
    } else {
        document.getElementById('no_proposals_msg').style.display = 'none';
    };

    // Update the count of how many emails are being shown
    document.getElementById('n_emails_showing').innerHTML = num_emails_displayed;
};


function get_n_emails_loaded() {
    console.log("COUNTING EMAILS")
    // Find all email elements
    var emails = document.getElementsByClassName("email-card");
    console.log("number of emails: ", emails.length)

    // Update the count of how many emails are being shown
    document.getElementById('n_emails_showing').innerHTML = emails.length;
};

function end_loading_animation() {
    console.log("SWITCHING DIVS")
    document.getElementById('email_container').style.display = 'inline-block';
    document.getElementById('loading_anim').style.display = 'none';
};

function onload() {
    console.log("LOADED!")
    get_n_emails_loaded();
    end_loading_animation();
};
