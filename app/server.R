library(shiny)
library(jsonlite)
library(dplyr)
library(stringr)

shinyServer(function(input, output) {
    
    all_nodups_df <- fromJSON("../data/nodupsMail.json")
    n_total_emails <- all_nodups_df %>%
        nrow()
    
    
    card <- function(subject, sender, recipient, date, body) {
        div(class="card",
            div(class="header",
                h4(subject),
                p(recipient),
                p(sender),
                p(date)
                ),
            p(body)
        )
    }
    
    # df_to_disp <- eventReactive(input$apply_filters_button, {
    #     
    #     all_nodups_df %>%
    #         filter(str_detect(from, input$From))
    # })
    
    
    output$emails <- renderUI({
        input$apply_filters_button
        
        isolate({
            print(input$From)
            
            df_to_disp <- all_nodups_df %>%
                filter(str_detect(from, input$From))
        })
        
        output$n_emails <- renderText({
            paste0("Showing ",
                   df_to_disp %>% nrow() %>% as.character(),
                   "/",
                   n_total_emails, 
                   " emails")
        })
        
        # First make the cards
        args <- apply( df_to_disp, 1, function(.x) card(subject = .x['subject'],
                                                      sender = .x['from'],
                                                      recipient = .x['to'],
                                                      date = .x['date'],
                                                      body = .x['body']))

        # Make sure to add other arguments to the list:
        args$cellArgs <- list(
            style = "
        width: auto;
        height: auto;
        margin: 5px;
        ")

        # basically the same as flowLayout(cards[[1]], cards[[2]],...)
        do.call(shiny::flowLayout, args)
        
        # tagList(apply(df_to_disp, 2, card_from_df))

    }) #%>%
        # bindCache(input$From)

})
