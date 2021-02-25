
/**
 * Perform a search of emails and display the resulting cards
 */
function filter_emails() {

    // Find all email elements
    var emails = document.getElementsByClassName("card_div");

    // Determine the current search values
    var from_search = document.getElementById("from_search_box").value;
    var to_search = document.getElementById("to_search_box").value;
    var cc_search = document.getElementById("cc_search_box").value;
    var subj_body_search = document.getElementById("body_search_box").value;
    var date_start_search = Date.parse(document.getElementById("start_search_box").value);
    var date_end_search = Date.parse(document.getElementById("end_search_box").value);

    // Determine whether or not to display each thumbnail
    var num_emails_displayed = 0;

    for (i = 1; i <= emails.length; i++) {
        var email  = document.getElementById("card" + i)

        if (!email) {
            console.error("We've got an issue with card", i)
        }

        // Evaluate if the "from" text matches the search
        let email_from = email.getAttribute('from').toLowerCase()
        let from_match = from_search == "" | email_from.includes(from_search.toLowerCase())

        // Evaluate if the "to" text matches the search
        let email_to = email.getAttribute('to').toLowerCase()
        let to_match = to_search == "" | email_to.includes(to_search.toLowerCase())

        // Evaluate if the "cc" text matches the search
        let email_cc = email.getAttribute('cc').toLowerCase()
        let cc_match = cc_search == "" | email_cc.includes(cc_search.toLowerCase())

        // Evaluate if the "subject/body" text matches the search
        let email_subj_body = email.getAttribute('subj_body').toLowerCase()
        let subj_body_match = subj_body_search == "" | email_subj_body.includes(subj_body_search.toLowerCase())

        // Evaluate if the "date" text matches the search
        let email_date = Date.parse(email.getAttribute('date'))

        // if (email.getAttribute('date').length < 5) {
        //     console.log(email.getAttribute('date'))
        //     console.log(email_date)
        //     console.log(isNaN(email_date))
        // }
        
        let date_match = isNaN(email_date) | (email_date <= date_end_search & email_date >= date_start_search)

        // console.log(email, from_match, to_match, cc_match, subj_body_match)

        if (from_match & to_match & cc_match & subj_body_match & date_match) {
            email.style.display = "inline-block";
            num_emails_displayed++;
        } else {
            email.style.display = "none";
        }
    };

    // If there are no proposals to display, tell the user
    if (num_emails_displayed == 0) {
        document.getElementById("no_emails_msg").style.display = 'block';
    } else {
        document.getElementById("no_emails_msg").style.display = 'none';
    };

    // Update the count of how many emails are being shown
    document.getElementById('n_emails_showing').innerHTML = num_emails_displayed;
};


// function get_n_emails_loaded() {
//     // Find all email elements
//     var incidents = document.getElementsByClassName("card_div");
//     console.log("number of incidents: ", incidents.length)

//     // Update the count of how many emails are being shown
//     document.getElementById('n_incidents_showing').innerHTML = incidents.length;
// };


