// Populate the HTML database with emails

var all_data;
var i_email = 1;
var email_pages;

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
    })

// var years = [];
// var cities = [];

// function addPaginate() {

//     $(document).ready(function() {
//           $('.cards-container').before('<div id="nav" class="text-center"></div>');
//           var rowsShown = 50;
//           var rowsTotal = $('.card_div').length;
//           var numPages = rowsTotal / rowsShown;
//           for (i = 0; i < numPages; i++) {
//             var pageNum = i + 1;
//             $('#nav').append('<a href="#" class="btn-outline-info" rel="' + i + '">&emsp;' + pageNum + '&emsp;</a> ');
//           }
//           $('.card_div').hide();
//           $('.card_div').slice(0, rowsShown).show();
//           $('#nav a:first').addClass('active');
//           $('#nav a').bind('click', function(e) {
//             e.preventDefault();
//             $('#nav a').removeClass('active');
//             $(this).addClass('active');
//             var currPage = $(this).attr('rel');
//             var startItem = currPage * rowsShown;
//             var endItem = startItem + rowsShown;
//             $('.card_div').css('opacity', '0').hide().slice(startItem, endItem).
//             css('display', 'flex').animate({
//               opacity: 1
//             }, 300);
//           });
//         });
// }

function createCards(all_data) {

    console.log("set up load listener")
    window.addEventListener('load', (event) => {
      console.log('page is fully loaded');
    });

    console.log("number of emails?", all_data.length)

    card_container = document.getElementsByClassName("cards-container")[0]

    // Add cards for all emails
    for (email in all_data) {
        // console.log(email)

        email_data = all_data[email]

        let id = email_data.mailId

        // years.push(year)

        // cities.push(incident_data.City)

        // console.log(incident_data.IncidentDate.slice(incident_data.IncidentDate.length - 4))

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

        // card_div.setAttribute("year", incident_data.IncidentDate.slice(id.length - 4))

        all_data[email]['card_html'] = card_div

        // card_container.appendChild(card_div)
        i_email += 1


    }

    console.log("out of loop")

    // // Do years now	
    // years.sort();
    // years = ["All"].concat(years)
    // years_set = new Set(years)

    // years_set.forEach(function(y) {
    //     o = document.createElement("option")
    //     o.innerHTML = y
    //     document.getElementById("year_select").appendChild(o)
    // })

    // // And cities
    // cities.sort();
    // cities = ["All"].concat(cities)
    // cities_set = new Set(cities)

    // cities_set.forEach(function(c) {
    //     o = document.createElement("option")
    //     o.innerHTML = c
    //     document.getElementById("city_select").appendChild(o)
    // })

    // Count all incidents// Find all email elements
    let emails = document.getElementsByClassName("card_div");
    console.log("total number of emails: ", emails.length)
    document.getElementById('total_n_emails').innerHTML = emails.length;
    document.getElementById('n_emails_showing').innerHTML = emails.length;

    // console.log("adding paginate")
    // addPaginate()

}