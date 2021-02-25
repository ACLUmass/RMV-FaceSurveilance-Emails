// Populate the HTML database with emails

var all_data;
var i_email = 1;
var email_pages;

var card_container = document.getElementsByClassName("cards-container")[0]

function load_data() {
    // return $.getJSON("nodupsMail.json", function(json) {
    return $.getJSON("allMails.json", function(json) {    
        all_data = json;
    });
}

load_data()
    .then(() => {
        console.log("data loaded", all_data)
        createCards(all_data)
        showCards(init=true)
    })

function createCards(all_data) {

    console.log("set up load listener")
    window.addEventListener('load', (event) => {
      console.log('page is fully loaded');
    });

    console.log("number of emails?", all_data.length)

    // Add cards for all emails
    for (email in all_data) {

        email_data = all_data[email]

        let id = email_data.mailId

        let to = (email_data.to?email_data.to:'')
        let from = (email_data.from?email_data.from:'')
        let subject = (email_data.subject?email_data.subject:' ')
        let cc = (email_data.cc?email_data.cc:'')
        let body = (email_data.body?email_data.body:'')
        body = body.replace(/(?:\r\n|\r|\n)/g, '<br>')

        let card_div = document.createElement("div");

        card_div.className = "col-lg-6 card_div"
        card_div.id = "card" + i_email
        card_div.setAttribute("to", to.toLowerCase())
        card_div.setAttribute("from", from.toLowerCase())
        card_div.setAttribute("cc", cc.toLowerCase())
        card_div.setAttribute("subj_body", [subject.toLowerCase(), body.toLowerCase()].join(" "))
        card_div.setAttribute("date", email_data.date)

        card_div.innerHTML = `
		        	<div class="card">
		        	<div class="card-header">
					    ${subject}
					  </div>
				  <div class="card-body">
				  <div class="card-text">
			    	        <div><b>To:</b> ${to}</div>
			    	        <div><b>From:</b> ${from}</div>
			    	        <div><b>CC:</b> ${cc}</div>
			    	        <div><b>Date:</b> ${email_data.date}</div>
			            <p class="email-description">
			            	${body}
			            </p>

			            <div style="text-align:right;"><a class="btn btn-dark" href="${email_data.mailURL}" target="blank" role="button">View PDF</a></div>
				  </div>
				  </div>
				`

        // Add card HTML to all_data list
        all_data[email]['card_html'] = card_div
        i_email += 1
    }

}

function showCards(init=false) {
    console.log("running showCards")

    if (init) {
        total_pages = 221;

        email_data = {};
        for(i = 0; i < total_pages; i++) {

            email_data[i] = [];

            for(j = i * 50; j < Math.min(((i * 50) + 50), all_data.length); j++) {
                email_data[i].push(j);
            }
        }

        // current_page = 1;
        $('#pagination-nav').pagination({
            pages: total_pages,
            displayedPages: 7,
            ellipsePageSet: false,
            cssStyle: '',
            prevText: '<span aria-hidden="true">&laquo;</span>',
            nextText: '<span aria-hidden="true">&raquo;</span>',
            onPageClick: function (page, evt) {
                showCards();
            }
        });
    }

    var current_page = parseInt($(".pagination .active.page-item span")[0].innerHTML) - 1;

    // Remove all existing cards
    card_container.innerHTML = '';

    // Add new cards
    email_data[current_page].forEach( function(email) {
        card_container.appendChild(all_data[email]["card_html"])
    });

    // Count all email elements
    var total_n_emails = 0;
    Object.keys(email_data).map(function(prop) {
        total_n_emails+= email_data[prop].length;
    });
    document.getElementById('total_n_emails').innerHTML = total_n_emails.toLocaleString();
    document.getElementById('n_emails_showing').innerHTML = email_data[current_page].length;

}


function reset_filters() {
    document.getElementById("search_form").reset();
    filter_emails();
};


function reset_dates() {
    $('input[id="start_search_box"]').val('2014-01-01T00:00')
    $('input[id="end_search_box"]').val('2019-12-31T00:00')
    // filter_emails();
};